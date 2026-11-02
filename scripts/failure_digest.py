#!/usr/bin/env python3
import argparse,csv,json,sqlite3,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def permitted(run,post):
    m=json.loads((run/'run_metadata.json').read_text()); split=m['split']
    if split=='dev': return m
    if split!='test' or not post: raise ValueError('per-case digest refuses non-dev runs before post-freeze')
    subprocess.run([sys.executable,str(ROOT/'scripts/freeze_check.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    log=ROOT/'eval_results/test_run_log.jsonl'
    if not log.exists(): raise ValueError('valid live test run not recorded')
    entries=[json.loads(x) for x in log.read_text().splitlines() if x.strip()]
    if not any(x.get('status')=='completed' and x.get('valid') is True and x.get('mode')=='live' and x.get('case_sha256')==m.get('case_sha256') for x in entries): raise ValueError('valid live test run not recorded for these cases')
    return m

def main(run,out,post):
    meta=permitted(run,post); metrics=json.loads((run/'metrics.json').read_text()); details=json.loads((run/'details.json').read_text())
    db=sqlite3.connect(run/'run.sqlite'); db.row_factory=sqlite3.Row
    lines=['# Failure digest','',f"Split: {meta['split']}; mode: {meta['mode']}; cases: {len(details)}",'', '## Aggregate metrics','', '```json',json.dumps(metrics,indent=2,sort_keys=True),'```','', '## Class breakdown','']
    sys.path.insert(0,str(ROOT))
    from agent.metrics import aggregate_csv
    with (run/'cases.csv').open(newline='') as f: case_rows=list(csv.DictReader(f))
    for cls in sorted({d['case']['class'] for d in details}):
        subset=[x for x in case_rows if x['class']==cls]
        lines += [f'### {cls}', '```json',json.dumps(aggregate_csv(subset),indent=2,sort_keys=True),'```']
    lines+=['','## Cases','']
    for d in details:
        c=d['case']; checks=d['checks']; fail=[k for k,v in checks.items() if (k!='exception' and not v)]
        if not checks['exception']:
            lines.append(f"- {c['id']} ({c['class']}): pass"); continue
        lines += [f"### {c['id']} — {c['class']}, difficulty {c.get('difficulty')}",f"Failed: {', '.join(fail) or 'execution error'}",'Gold: '+json.dumps({'obligations':c['gold_obligations'],'escalation':c['gold_escalation_codes']},ensure_ascii=False),'Got: '+json.dumps(d['output'],ensure_ascii=False)]
        lines.append('Ungrounded quotes: '+json.dumps(d.get('ungrounded_quotes',[]),ensure_ascii=False))
        lines.append('Trace:')
        for r in db.execute('SELECT seq,tool_name,args_json,error_class,retry_count FROM tool_calls WHERE run_id=? ORDER BY seq',(d['run_id'],)):
            lines.append(f"- {r['seq']} {r['tool_name']}: {(r['args_json'] or '')[:200]} | {r['error_class']} | retries={r['retry_count']}")
        lines.append('Terminal args: '+json.dumps(d['result'].get('args'),ensure_ascii=False)[:1500]); lines.append('')
    text='\n'.join(lines); cap=100000
    if len(text)>cap: text=text[:cap]+'\n\n[Truncated at 100,000 characters.]\n'
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text+'\n');db.close();print('digest written')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--post-freeze',action='store_true');a=p.parse_args()
    try: main(a.run,a.out,a.post_freeze)
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
