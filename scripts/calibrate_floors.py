#!/usr/bin/env python3
import argparse,hashlib,json,math,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def load_run(path):
    meta=json.loads((path/'run_metadata.json').read_text())
    if meta['split']!='dev': raise ValueError('calibration refuses non-dev runs')
    rows=json.loads((path/'details.json').read_text())
    expected=sum(yaml.safe_load((ROOT/'config/splits.yaml').read_text())['dev'].values())
    if len(rows)!=expected: raise ValueError(f'calibration requires the full {expected}-case dev split')
    return rows

def stats(labels,preds):
    pos=sum(labels); neg=len(labels)-pos
    if not pos or not neg: raise ValueError('calibration requires both positive and negative examples')
    return sum(a and b for a,b in zip(labels,preds))/pos, sum((not a) and b for a,b in zip(labels,preds))/neg

def main(run):
    log=ROOT/'eval_results/test_run_log.jsonl'
    if log.exists() and any(json.loads(line).get('valid') is True and json.loads(line).get('status')=='completed' for line in log.read_text().splitlines() if line.strip()): raise ValueError('calibration forbidden after frozen test results; use v1.1')
    rows=load_run(run)
    e1labels=['E1_NO_OBLIGATION' in x['case']['gold_escalation_codes'] for x in rows]
    scores=[x['result']['retrieval_score'] for x in rows]
    if any(x is None for x in scores): raise ValueError('retrieval score missing')
    candidates=sorted(set([min(scores)-1.0]+[math.nextafter(x,math.inf) for x in scores]))
    e1s=[]
    for floor in candidates:
        rec,fp=stats(e1labels,[x<floor for x in scores]); e1s.append((floor,rec,fp))
    possible=[x for x in e1s if x[2]<=.2]
    if not possible: raise ValueError('no E1 floor satisfies false escalation constraint')
    e1=sorted(possible,key=lambda x:(-x[1],x[2],x[0]))[0][0]
    labels=[bool(x['case']['gold_should_escalate']) for x in rows]; e5s=[]
    for floor in (.5,.6,.7,.8):
        preds=[]
        for x in rows:
            d=x['result']; args=d.get('args',{}); codes=set(d['decision'].get('escalation_codes',[]))-{'E1_NO_OBLIGATION','E5_LOW_CONFIDENCE'}
            conf=[args.get('confidence',1)]+[o.get('confidence',1) for o in args.get('obligations',[])]
            preds.append(scores[len(preds)]<e1 or bool(codes) or min(conf)<floor)
        rec,fp=stats(labels,preds); e5s.append((floor,rec,fp))
    possible=[x for x in e5s if x[2]<=.2]
    e5=sorted(possible,key=lambda x:(-x[1],x[2],x[0]))[0][0] if possible else .65
    provenance='dev-sweep' if possible else 'uncalibrated-fallback'
    lines=['# Threshold calibration','', f'Dev only; n={len(rows)} is noisy. E1 uses gold E1 labels; E5 uses gold escalation and other retained codes. Ties: higher recall, then lower false escalation, then lower floor.','', '## E1','', '| Floor | Recall | False escalation |','|---:|---:|---:|']
    lines += [f'| {f:.8g} | {r:.3f} | {fp:.3f} |' for f,r,fp in e1s]
    lines += ['',f'Selected E1: {e1:.12g}.','','## E5','','| Floor | Recall | False escalation |','|---:|---:|---:|']
    lines += [f'| {f:.2f} | {r:.3f} | {fp:.3f} |' for f,r,fp in e5s]
    lines += ['',f'Selected E5: {e5:.2f} ({provenance}).','']
    report=ROOT/'eval_results/threshold_calibration.md'; report.write_text('\n'.join(lines))
    digest=hashlib.sha256(report.read_bytes()).hexdigest()
    (ROOT/'config/thresholds.yaml').write_text(yaml.safe_dump({'e1':{'value':e1,'provenance':'dev-sweep'},'e5':{'value':e5,'provenance':provenance},'calibration_sha256':digest},sort_keys=False))
    print('calibration written')
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--run',type=Path,required=True); a=p.parse_args()
    try: main(a.run)
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
