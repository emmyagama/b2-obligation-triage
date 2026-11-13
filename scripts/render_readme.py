#!/usr/bin/env python3
import csv,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.evalio import fmt
from agent.metrics import aggregate_csv
from agent.config import ROOT

def fmt_cost(cost):
    if not cost or not cost['n'] or cost['mean_usd'] is None: return 'not measurable (0 denominator)'
    return f"${cost['mean_usd']:.4f} per transaction, n={cost['n']}"

def point(rate):
    if not rate or not rate['denominator']: return 'not measurable (0 denominator)'
    return f"{rate['value']:.1%} ({rate['numerator']}/{rate['denominator']})"

def render():
    root=ROOT/'eval_results'; files=sorted(root.glob('run_test_*.csv'))
    if not files: raise ValueError('README needs held-out results CSV')
    with files[-1].open(newline='') as f: rows=list(csv.DictReader(f))
    if len(rows)!=30: raise ValueError('README requires exactly 30 held-out rows')
    metrics=aggregate_csv(rows); template=(ROOT/'README.template.md').read_text(encoding='utf-8')
    l=metrics['latency'];c=metrics['cost']
    log=root/'test_run_log.jsonl'; n=sum(1 for line in log.read_text(encoding='utf-8').splitlines() if line.strip() and json.loads(line).get('mode')=='live' and json.loads(line).get('status')=='started') if log.exists() else 0
    v={k:fmt(metrics[k]) for k in ('exception_rate','deadline_absolute','deadline_relative','obligation_recall','escalation_recall','false_escalation','grounded_rate')}
    for k in ('exception_rate','deadline_relative','obligation_recall','escalation_recall','false_escalation','grounded_rate'):
        v[k+'_point']=point(metrics[k])
    v.update(constructed_e2_cases=metrics['constructed_e2_cases'],constructed_e2_exception_rate=fmt(metrics['constructed_e2_exception_rate']),constructed_e2_recall=fmt(metrics['constructed_e2_recall']))
    v.update(constructed_e2_exception_rate_point=point(metrics['constructed_e2_exception_rate']),constructed_e2_recall_point=point(metrics['constructed_e2_recall']))
    v.update(latency=f"{l['p50_ms']} / {l['p95_ms']} ms (n={l['n']})",latency_short=f"{l['p50_ms']/1000:.1f} / {l['p95_ms']/1000:.1f} s (n={l['n']})",cost=fmt_cost(c),cuts='none instructed',test_run_count=str(n))
    def cases(path):
        data=json.loads(path.read_text(encoding='utf-8')); return data if isinstance(data,list) else data['cases']
    def sources(c): return c.get('source_document_ids') or [c.get('source_document_id') or c['document_id']]
    dev=ROOT/'cases/dev.json'; test=ROOT/'cases/test.json'
    if not dev.exists() or not test.exists(): raise ValueError('case files required to rederive document overlap')
    v['document_overlap']=str(len({s for c in cases(dev) for s in sources(c)} & {s for c in cases(test) for s in sources(c)}))
    rounds=sorted((root/'rounds').glob('*.json')) if (root/'rounds').exists() else []
    history=[]
    for p in rounds:
        info=json.loads(p.read_text(encoding='utf-8')); run=(root/info['run_dir']).resolve()
        if root.resolve() not in run.parents: raise ValueError('tuning run must be under eval_results')
        if json.loads((run/'run_metadata.json').read_text(encoding='utf-8'))['split']!='dev': raise ValueError('tuning history must be dev only')
        with (run/'cases.csv').open(newline='') as f: rm=aggregate_csv(list(csv.DictReader(f)))
        history.append(f'{p.stem}: {fmt(rm["exception_rate"])}')
    v['tuning_history']='; '.join(history) or 'not yet recorded'
    er=metrics['exception_rate']['value']; rel=metrics['deadline_relative']['value']
    if er is None or rel is None: v['falsification']='Falsification cannot be fully assessed because a required denominator is zero.'
    elif er>.35 or rel<.55: v['falsification']='The design is wrong, not the model. A suspected cause is missing or ambiguous effective-date labels in contracts with relative deadlines; this requires investigation.'
    else: v['falsification']='The prespecified falsification rule was not triggered.'
    taxonomy=root/'failure_taxonomy.md';v['failure_taxonomy']=taxonomy.read_text(encoding='utf-8').strip() if taxonomy.exists() else 'Pending post-freeze documentation.'
    if re.search(r'\d',re.sub(r'\bE[1-6](?:_[A-Z_]+)?\b','',v['failure_taxonomy'])): raise ValueError('manual failure taxonomy must not contain unverifiable numeric claims')
    v['offline_reproduction']='Run `python run_eval.py --split test` with the released cache; then run `python check_readme.py`. No API key or network is required. For the versioned compressed cache artifact and clean-clone verification, see `CACHE-ARTIFACT.md`.'
    missing=set(re.findall(r'{{\s*(\w+)\s*}}',template))-v.keys()
    if missing: raise ValueError('unresolved README placeholders: '+', '.join(sorted(missing)))
    return re.sub(r'{{\s*(\w+)\s*}}',lambda m:str(v[m.group(1)]),template)
if __name__=='__main__':
    try: (ROOT/'README.md').write_text(render(),encoding='utf-8');print('README rendered')
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
