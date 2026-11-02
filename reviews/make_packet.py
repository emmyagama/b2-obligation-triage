#!/usr/bin/env python3
"""Produce blinded, deterministic reviewer packets from a released full-run DB."""
import argparse,csv,json,random,sqlite3,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def choose(db,seed=20261102,limit=20):
    ids=[r[0] for r in db.execute('SELECT id FROM escalations ORDER BY id')]
    return sorted(random.Random(seed).sample(ids,min(limit,len(ids))))

def packet(db,ids,reviewer,seed):
    rng=random.Random(f'{seed}:{reviewer}'); ids=list(ids);rng.shuffle(ids)
    lines=['# Escalation review packet','',f'Reviewer: {reviewer}','','Review only the evidence below. Return your completed verdict CSV. Do not infer missing facts.','']
    for eid in ids:
        e=db.execute('SELECT e.id,e.reason_code,e.queue,d.id AS decision_id,d.run_id FROM escalations e JOIN decisions d ON d.id=e.decision_id WHERE e.id=?',(eid,)).fetchone()
        if e is None: raise ValueError('escalation not found')
        obligations=db.execute('SELECT o.*,d.deadline_kind,d.raw_text,d.resolved_date,d.anchor_event,d.offset_days,d.recurring_rule FROM obligations o LEFT JOIN obligation_deadlines d ON d.obligation_id=o.id WHERE o.decision_id=? ORDER BY o.id',(e['decision_id'],)).fetchall()
        lines += [f'## Escalation {eid}', '',f"Reason: {e['reason_code']}",f"Queue: {e['queue']}",'','### Extracted obligations and cited text','']
        for o in obligations:
            lines += [f"- Type: {o['obligation_type']}; owed by: {o['owed_by']}",f"  - Description: {o['description']}",f"  - Deadline: {o['deadline_kind']}; raw: {o['raw_text']}; resolved: {o['resolved_date']}",f"  - Consequence: {o['consequence']}",f"  - Cited clause: {o['clause_quote']}"]
        if not obligations: lines.append('No obligations recorded.')
        lines += ['', '### Retrieved evidence excerpts','']
        traces=db.execute("SELECT result_json FROM tool_calls WHERE run_id=? AND tool_name IN ('retrieval_precheck','search_corpus','get_clause') ORDER BY seq",(e['run_id'],)).fetchall()
        excerpts=[]
        for t in traces:
            try: obj=json.loads(t[0] or '{}')
            except json.JSONDecodeError: continue
            items=obj.get('evidence',[]) if isinstance(obj,dict) else obj if isinstance(obj,list) else []
            for item in items:
                if isinstance(item,dict):
                    text=item.get('text') or item.get('answer_text')
                    if isinstance(text,str) and text.strip() and text not in excerpts: excerpts.append(text)
        for text in excerpts: lines += ['> '+text.replace('\n','\n> '),'']
        if not excerpts: lines += ['No retrieval excerpt was recorded.','']
        lines += ['Verdict: agree / disagree / insufficient_information. Explain any disagreement in one line.','']
    return '\n'.join(lines)+'\n'

def main(run,out,seed):
    meta=json.loads((run/'run_metadata.json').read_text())
    if meta.get('split')!='all' or meta.get('cases')!=50: raise ValueError('review packets require a frozen full dev + test run')
    subprocess.run([sys.executable,str(ROOT/'scripts/freeze_check.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    testhash=(ROOT/'cases/FROZEN.sha256').read_text().split()[0]
    log=ROOT/'eval_results/test_run_log.jsonl'
    if not log.exists() or not any((lambda x:x.get('status')=='completed' and x.get('valid') is True and x.get('mode')=='live' and x.get('case_sha256')==testhash)(json.loads(line)) for line in log.read_text().splitlines() if line.strip()): raise ValueError('valid frozen live test run is required')
    hashes=meta.get('case_sha256','').split(';')
    if testhash not in hashes: raise ValueError('full run does not match frozen test commitment')
    db=sqlite3.connect(run/'run.sqlite');db.row_factory=sqlite3.Row;ids=choose(db,seed)
    if not ids: raise ValueError('no escalations available for review')
    out.mkdir(parents=True,exist_ok=True)
    for i in range(1,4):
        reviewer=f'reviewer-{i}';(out/f'{reviewer}.md').write_text(packet(db,ids,reviewer,seed),encoding='utf-8')
        with (out/f'{reviewer}-verdicts.csv').open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=['escalation_id','reviewer_id','reviewer_role','verdict','note','human_obligation_count']);w.writeheader()
            for eid in ids: w.writerow({'escalation_id':eid,'reviewer_id':reviewer})
    (out/'manifest.json').write_text(json.dumps({'run_database':str((run/'run.sqlite').resolve()),'seed':seed,'escalation_ids':ids},indent=2,sort_keys=True)+'\n')
    db.close(); print(f'prepared {len(ids)} escalations for each of three reviewers')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path);p.add_argument('--out',type=Path,default=ROOT/'reviews/packets');p.add_argument('--seed',type=int,default=20261102);a=p.parse_args()
    try:
        paths=sorted((ROOT/'eval_results').glob('run_all_*')) if a.run is None else []
        if a.run is None and not paths: raise ValueError('no frozen full run found; pass --run')
        main(a.run or paths[-1],a.out,a.seed)
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
