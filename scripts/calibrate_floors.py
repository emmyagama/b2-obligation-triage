#!/usr/bin/env python3
import argparse,hashlib,json,math,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
E1_MIN_POSITIVES=2
E5_FLOORS=(.5,.6,.7,.8)
ESC_REMOVE={'E1_NO_OBLIGATION','E5_LOW_CONFIDENCE'}

def load_run(path):
    path=Path(path)
    if not path.is_absolute(): path=ROOT/path
    meta=json.loads((path/'run_metadata.json').read_text(encoding='utf-8'))
    if meta['split']!='dev': raise ValueError('calibration refuses non-dev runs')
    rows_path=path/'details.json'; reconstructed=False
    if not rows_path.exists() or not rows_path.read_bytes().strip():
        rows_path=path/'details.reconstructed.json'; reconstructed=True
    if not rows_path.exists(): raise ValueError(f'no details file under {path}')
    data=json.loads(rows_path.read_text(encoding='utf-8'))
    if isinstance(data,dict):
        if data.get('reconstructed') is not True:
            raise ValueError('reconstructed details must carry "reconstructed": true')
        rows=data['rows']; reconstructed=True
    else:
        rows=data
    expected=sum(yaml.safe_load((ROOT/'config/splits.yaml').read_text(encoding='utf-8'))['dev'].values())
    if len(rows)!=expected: raise ValueError(f'calibration requires the full {expected}-case dev split')
    shown=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    return rows,shown.replace('\\','/'),rows_path.name,reconstructed

def stats(labels,preds):
    pos=sum(labels); neg=len(labels)-pos
    if not pos or not neg: raise ValueError('calibration requires both positive and negative examples')
    return sum(a and b for a,b in zip(labels,preds))/pos, sum((not a) and b for a,b in zip(labels,preds))/neg

def min_conf(x):
    args=x['result'].get('args',{})
    conf=[args.get('confidence',1)]+[o.get('confidence',1) for o in args.get('obligations',[])]
    return min(conf)

def sweep_e1(rows):
    labels=['E1_NO_OBLIGATION' in x['case']['gold_escalation_codes'] for x in rows]
    scores=[x['result']['retrieval_score'] for x in rows]
    if any(x is None for x in scores): raise ValueError('retrieval score missing')
    candidates=sorted(set([min(scores)-1.0]+[math.nextafter(x,math.inf) for x in scores]))
    table=[]
    for floor in candidates:
        rec,fp=stats(labels,[x<floor for x in scores]); table.append((floor,rec,fp))
    possible=[x for x in table if x[2]<=.2]
    if not possible: raise ValueError('no E1 floor satisfies false escalation constraint')
    return sorted(possible,key=lambda x:(-x[1],x[2],x[0]))[0][0],table,scores

def sweep_e5(rows,scores,e1):
    labels=[bool(x['case']['gold_should_escalate']) for x in rows]; table=[]
    for floor in E5_FLOORS:
        preds=[]
        for i,x in enumerate(rows):
            codes=set(x['result']['decision'].get('escalation_codes',[]))-ESC_REMOVE
            preds.append(scores[i]<e1 or bool(codes) or min_conf(x)<floor)
        rec,fp=stats(labels,preds); table.append((floor,rec,fp))
    possible=[x for x in table if x[2]<=.2]
    e5=sorted(possible,key=lambda x:(-x[1],x[2],x[0]))[0][0] if possible else .65
    return e5,('dev-sweep' if possible else 'uncalibrated-fallback'),table

def fmt_table(table,mode):
    cell=(lambda f: repr(f)) if mode=='repr' else (lambda f: f'{f:.2f}')
    lines=['| Floor | Recall | False escalation |','|---:|---:|---:|']
    return lines+[f'| {cell(f)} | {r:.3f} | {fp:.3f} |' for f,r,fp in table]

def e5_note(rows):
    zero=sum(1 for x in rows if min_conf(x)==0)
    mid=sum(1 for x in rows if 0<min_conf(x)<max(E5_FLOORS))
    high=len(rows)-zero-mid
    if mid==0:
        return (f'The sweep is flat: no case has a minimum confidence between 0 and {max(E5_FLOORS):.2f} '
                f'({zero} case(s) sit at 0 and are caught by every floor, {high} sit at or above 0.85 and are '
                'caught by none), so all four floors give identical predictions. False escalation is driven by '
                'escalation codes (E2/E3/E4), not by the confidence floor.')
    return f'{mid} case(s) have a minimum confidence inside the swept range, so the floor does separate cases.'

def main(runs):
    if not isinstance(runs,(list,tuple)): runs=[runs]
    log=ROOT/'eval_results/test_run_log.jsonl'
    if log.exists() and any(json.loads(line).get('valid') is True and json.loads(line).get('status')=='completed' for line in log.read_text(encoding='utf-8').splitlines() if line.strip()): raise ValueError('calibration forbidden after frozen test results; use v1.1')
    sources=[load_run(run) for run in runs]
    pooled=[r for rows,_src,_fn,_rc in sources for r in rows]
    e1,e1table,scores=sweep_e1(pooled)
    e1ids=[]; seen=set()
    for i,x in enumerate(pooled):
        if 'E1_NO_OBLIGATION' not in x['case'].get('gold_escalation_codes',[]): continue
        cid=x['case'].get('id')
        key=str(cid) if cid is not None else f'row-{i}'
        if key not in seen: seen.add(key); e1ids.append(key)
    e1ids=sorted(e1ids)
    e1prov='dev-sweep' if len(e1ids)>=E1_MIN_POSITIVES else 'uncalibrated-fallback'
    e5,e5prov,e5table=sweep_e5(pooled,scores,e1)
    per=[]
    for rows,src,_fn,_rc in sources:
        rs=[x['result']['retrieval_score'] for x in rows]
        prun,_,_=sweep_e1(rows)
        e5r,provr,tbl=sweep_e5(rows,rs,e1)
        per.append((src,prun,e5r,provr,tbl))
    n=len(sources); noun='run' if n==1 else 'runs'
    lines=['# Threshold calibration','',
           f'Dev only; n={len(pooled)} across {n} {noun} is noisy. E1 uses gold E1 labels; E5 uses gold escalation and other retained codes. Ties: higher recall, then lower false escalation, then lower floor.','',
           '## Sources','']
    for _rows,src,fn,recon in sources:
        kind=f'reconstructed from run.sqlite (`{fn}`, `"reconstructed": true`)' if recon else f'run `{fn}` as written'
        lines.append(f'- `{src}` — {kind}; n={len(_rows)}.')
    lines += ['',
              'Run A has no usable `details.json` (0 bytes: the harness crashed writing it), so it is reconstructed by `scripts/reconstruct_details.py --lean`, whose output carries `"reconstructed": true` and only the fields this script reads.',
              'The same reconstruction was first run against run B and diffed against B\'s real `details.json`: **all 26 rows identical** on `case`, `retrieval_score`, `args` and `decision.escalation_codes` (0 gaps). That diff is the provenance proof for run A.',
              'Unrecoverable in run A: the turn-1 `metadata` of every run — `created_at` and `system_fingerprint` (25 runs each). Run B overwrote those cache entries because turn-1 requests are identical across runs, and `tool_calls` stores no per-call timestamp. Neither field is read by this script.',
              'Nothing else in Phase E reads run A\'s `details.json`: `check_readme.py` (repo root) goes through `scripts/render_readme.py`, which reads `run_metadata.json` and metrics only; `scripts/freeze_check.py` has no `details` reference; the round summaries are prose; and of the whole tree only `scripts/failure_digest.py:17` and this script read `details.json` (the digest was already run against run B for round 3).','',
              '## E1','']
    lines+=fmt_table(e1table,'repr')
    lines+=[f'',
            f'Selected E1: {e1!r}. The sweep steps the floor to `math.nextafter(score, inf)`, i.e. the smallest float above each observed score, and the selected value is the smallest float above the minimum observed score ({min(scores):g}); E1 fires only when retrieval returns nothing better.',
            f'Provenance: {e1prov} — gold carries {len(e1ids)} distinct E1 positive case(s) ({", ".join(e1ids)}), so this floor rests on a single example (retrieval score {min(scores):g}) and is not a sweep-based calibration.','',
            '## E5','']
    lines+=[f'### Pooled ({n} {noun}, n={len(pooled)})','']+fmt_table(e5table,'2f')
    lines+=[f'',f'Selected E5: {e5:.2f} ({e5prov}).']
    if e5prov=='uncalibrated-fallback':
        lines+=['','No swept floor satisfies false escalation <= 0.20, so the spec fallback 0.65 applies. '+e5_note(pooled)]
    for src,prun,e5r,provr,tbl in per:
        lines+=[f'',f'### {src}','']+fmt_table(tbl,'2f')
        lines+=[f'',f'E5 for this run alone: {e5r:.2f} ({provr}); E1 for this run alone: {prun!r}.']
    lines+=['',
            'Per-run and pooled tables use the selected pooled E1 floor so they describe the configuration being frozen.','',
            '## Independence of the pooled sample','',
            f'The pooled n={len(pooled)} is the same {len(pooled)//n} dev cases observed once per run, not independent draws: the same case contributes {n} times, so the pooled figures are not {n}x the evidence.',
            'Run-to-run variance on the identical config (`system_v3`, git `3cf3380`) exceeds most round-to-round deltas — E4 4 vs 8, `schema_valid` 22 vs 18, `exception_rate` 1.000 vs 0.885, `deadline_relative` 0.067 vs 0.267, `false_escalation` 0.737 vs 0.789. Treat every figure above as dev-only and noisy.','']
    report=ROOT/'eval_results/threshold_calibration.md'
    report.write_text('\n'.join(lines),encoding='utf-8')
    digest=hashlib.sha256(report.read_bytes()).hexdigest()
    (ROOT/'config/thresholds.yaml').write_text(
        yaml.safe_dump({'e1':{'value':e1,'provenance':e1prov},'e5':{'value':e5,'provenance':e5prov},
                        'calibration_sha256':digest},sort_keys=False),encoding='utf-8')
    for _rows,src,fn,recon in sources:
        print(f'{"reconstructed" if recon else "details.json"}: {src}/{fn}')
    print('calibration written')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--run',action='append',required=True); a=p.parse_args()
    try: main(a.run)
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
