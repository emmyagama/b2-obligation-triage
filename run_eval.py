#!/usr/bin/env python3
"""Evaluate only user-authored cases, defaulting to cache-only replay."""
import argparse,csv,hashlib,importlib,json,os,shutil,sqlite3,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
from agent.cache import Cache,CacheMiss,canonical
from agent.config import ROOT,load
from agent.db import connect
from agent.embed import embed
from agent.engine import run_agent
from agent.evalio import csvwrite,jsonwrite,summary
from agent.intake import begin
from agent.metrics import aggregate
from agent.scoring import score

ACTIVE_TEST_ATTEMPT=None


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def gitsha():
    try: return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except Exception: return 'unversioned'
def parser():
    p=argparse.ArgumentParser(); p.add_argument('--split',choices=['dev','test','all'],required=True)
    p.add_argument('--live',action='store_true'); p.add_argument('--resume',action='store_true'); p.add_argument('--scratch',action='store_true')
    p.add_argument('--rpm',type=int); p.add_argument('--cases'); p.add_argument('--limit',type=int); p.add_argument('--cache-dir'); p.add_argument('--out'); return p

def main(a):
    if a.resume and not a.live: raise ValueError('--resume requires --live')
    log_path=ROOT/'eval_results/test_run_log.jsonl'
    if a.live and log_path.exists():
        for line in log_path.read_text().splitlines():
            item=json.loads(line)
            if item.get('status')=='completed' and item.get('valid') is True and item.get('mode')=='live':
                raise ValueError('live calls are prohibited after the completed frozen test run; changes require v1.1 re-baseline')
    if a.live:
        subprocess.run(['git','rev-parse','--verify','refs/tags/guide-v1.0'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if subprocess.run(['git','diff','--quiet','guide-v1.0','--','guide'],cwd=ROOT).returncode: raise ValueError('guide must match the frozen guide-v1.0 tag before live calls')
        untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','guide'],cwd=ROOT,text=True).strip()
        if untracked: raise ValueError('untracked guide file before live calls')
        commitment=ROOT/'cases/FROZEN.sha256'; heldout=ROOT/'cases/test.json'
        digest=hashlib.sha256(heldout.read_bytes()).hexdigest()
        if commitment.read_text().split()[0]!=digest: raise ValueError('held-out commitment mismatch before live calls')
        subprocess.run(['git','ls-files','--error-unmatch','cases/FROZEN.sha256'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        committed=subprocess.check_output(['git','show','HEAD:cases/FROZEN.sha256'],cwd=ROOT,text=True).split()[0]
        if committed!=digest: raise ValueError('held-out commitment must be committed before live calls')
        subprocess.run([sys.executable,str(ROOT/'scripts/validate_cases.py'),'--strict'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
    if a.rpm is not None and a.rpm<1: raise ValueError('--rpm must be positive')
    if a.scratch and (a.cache_dir or a.out): raise ValueError('--scratch cannot be combined with --cache-dir or --out')
    if a.split in ('test','all'):
        if a.cases or a.limit or a.scratch or (a.live and a.split!='test'): raise ValueError('live held-out run must be full test only, without filters or scratch')
        subprocess.run([sys.executable,str(ROOT/'scripts/freeze_check.py')],cwd=ROOT,check=True)
        if not a.live:
            if not log_path.exists(): raise ValueError('held-out replay requires a completed valid live test run')
            committed=(ROOT/'cases/FROZEN.sha256').read_text().split()[0]
            if not any((lambda x:x.get('status')=='completed' and x.get('valid') is True and x.get('mode')=='live' and x.get('cases')==30 and x.get('case_sha256')==committed)(json.loads(line)) for line in log_path.read_text().splitlines() if line.strip()):
                raise ValueError('held-out replay requires a completed valid live test run')
    cache=Cache(ROOT/('cache/scratch' if a.scratch else a.cache_dir or 'cache/llm'))
    out=Path('eval_results/scratch' if a.scratch else a.out or 'eval_results').resolve(); out.mkdir(parents=True,exist_ok=True)
    casefiles=[ROOT/'cases'/f'{s}.json' for s in (['dev','test'] if a.split=='all' else [a.split])]
    cases=[]
    for path in casefiles:
        data=json.loads(path.read_text()); cases.extend(data if isinstance(data,list) else data['cases'])
    if a.cases:
        ids=set(a.cases.split(',')); cases=[c for c in cases if str(c['id']) in ids]
        if len(cases)!=len(ids): raise ValueError('case filter did not match unique case ids')
    if a.limit is not None:
        if a.limit<1: raise ValueError('--limit must be positive')
        cases=cases[:a.limit]
    if not cases: raise ValueError('no cases selected')
    if a.split=='test' and len(cases)!=30: raise ValueError('held-out split must contain exactly 30 cases')
    if a.split=='all' and len(cases)!=50: raise ValueError('all split must contain exactly 50 cases')
    model=load('model.yaml'); floors=load('thresholds.yaml'); prices=load('pricing.yaml'); descriptions=load('tool_descriptions.yaml')
    if a.live and prices.get('model') and prices['model']!=model['model']: raise ValueError('pricing model does not match configured model')
    if a.live and (prices.get('input_per_million_usd') is None or prices.get('output_per_million_usd') is None): raise ValueError('verified model prices must be configured before live calls')
    config={**model,'e1_floor':floors['e1']['value'],'e5_floor':floors['e5']['value'],'pricing':prices}
    if config['e1_floor'] is None or config['e5_floor'] is None: raise ValueError('thresholds must be set; use labelled dev-only provisional floors before calibration')
    if a.split in ('test','all') and any(str(floors[k]['provenance']).startswith('provisional') or (k=='e1' and floors[k]['provenance']=='uncalibrated') for k in ('e1','e5')): raise ValueError('held-out run requires calibrated thresholds (or documented spec fallback)')
    prompt=(ROOT/'prompts'/f"{model['prompt_version']}.md").read_text()
    embed_manifest=ROOT/'corpus/embeddings/manifest.json'
    if embed_manifest.exists():
        from agent.chroma_store import load as load_chroma,digest as digest_chunks
        em=json.loads(embed_manifest.read_text());chunks=load_chroma(ROOT/'corpus/embeddings/chroma')
        if em.get('model_id')!=model.get('embedding_model') or em.get('chunks')!=len(chunks) or em.get('content_sha256')!=digest_chunks(chunks): raise ValueError('Chroma content or model differs from embedding manifest')
    else: chunks=json.loads((ROOT/'corpus/embeddings/chunks.json').read_text())
    if (ROOT/'corpus/selection.json').exists():
        from agent.corpus_version import version
        if model['corpus_version']!=version(ROOT): raise ValueError('corpus or embeddings changed; rebuild embeddings and freeze the new corpus version')
    source=ROOT/'db/b2.sqlite'; stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'); run_dir=out/f'run_{a.split}_{stamp}'; run_dir.mkdir()
    shutil.copy2(source,run_dir/'run.sqlite'); db=connect(run_dir/'run.sqlite')
    from agent.taxonomy import load_taxonomy
    types=load_taxonomy(db,ROOT/'guide/obligation_types.yaml')
    if {r[0] for r in db.execute('SELECT code FROM obligation_types')} != {r[0] for r in types}: raise ValueError('database taxonomy differs from human-authored guide')
    global ACTIVE_TEST_ATTEMPT
    if a.live and a.split=='dev':
        with (ROOT/'eval_results/dev_run_log.jsonl').open('a') as f: f.write(canonical({'status':'started','mode':'live','attempt_id':stamp,'git_sha':gitsha()})+'\n')
    if a.live and a.split=='test':
        ACTIVE_TEST_ATTEMPT={'attempt_id':stamp,'mode':'live','case_sha256':sha(casefiles[0]),'git_sha':gitsha()}
        with (ROOT/'eval_results/test_run_log.jsonl').open('a') as f: f.write(canonical({**ACTIVE_TEST_ATTEMPT,'status':'started'})+'\n')
    model_id=model.get('embedding_model'); adapter=None
    if a.live:
        if not model.get('embedding_adapter'): raise ValueError('embedding_adapter not configured')
        module,name=model['embedding_adapter'].rsplit(':',1); adapter=getattr(importlib.import_module(module),name)
    records=[]; rows=[]; drifts=[]; known={}; last_request=[0.0]
    def throttle():
        if a.rpm and last_request[0]:
            delay=60/a.rpm-(time.monotonic()-last_request[0])
            if delay>0: time.sleep(delay)
        last_request[0]=time.monotonic()
    def query(text,seq,case_id):
        return embed(text,model_id,cache,adapter,live=a.live,resume=a.resume,case_id=case_id,seq=seq,on_drift=lambda req:drifts.append({'case_id':case_id,'seq':seq,'request_hash':__import__('agent.cache',fromlist=['key_for']).key_for(req)}))
    for c in cases:
        cid=str(c['id']); docid=c['document_id']
        path=ROOT/'corpus/documents'/f'{docid}.txt'
        if path.resolve().parent!=(ROOT/'corpus/documents').resolve(): raise ValueError('unsafe document id')
        document=path.read_text(encoding='utf-8'); original=c.get('duplicate_of')
        if original is not None:
            if str(original) not in known: raise ValueError('duplicate_of must reference an earlier case in the same execution')
            base=known[str(original)]
            if document!=base['document'] or c['intake_party']!=base['case']['intake_party'] or c.get('business_context')!=base['case'].get('business_context'): raise ValueError('duplicate request content differs from original')
            # Reuse the original request, not the mutated document id.
            run_id,hit=begin(db,'eval:'+str(original),base['case']['document_id'],c['intake_party'],c.get('business_context'),'eval',model)
            result=base['result']; duplicate_ok=hit and run_id==base['run_id']
        else:
            run_id,hit=begin(db,'eval:'+cid,docid,c['intake_party'],c.get('business_context'),'eval',model)
            if hit: raise ValueError('unexpected duplicate case id')
            started=time.monotonic()
            result=run_agent(db,run_id,docid,c['intake_party'],c.get('business_context'),document,chunks,lambda text,seq:query(text,seq,cid),cache,config,descriptions,prompt,live=a.live,resume=a.resume,case_id=cid,throttle=throttle)
            elapsed=round((time.monotonic()-started)*1000)
            tr={'kind':'transaction','case_hash':hashlib.sha256(canonical(c).encode()).hexdigest(),'model':model['model'],'prompt_version':model['prompt_version'],'corpus_version':model['corpus_version'],'e1_floor':config['e1_floor']}
            if a.live:
                if a.resume:
                    try: timing=cache.get(tr,cid,'transaction')['response']['latency_ms']
                    except CacheMiss: timing=None  # partial resume cannot establish end-to-end latency
                else: timing=elapsed
                cache.put(tr,{'latency_ms':timing},{'provider':'local','model':model['model'],'created_at':datetime.now(timezone.utc).isoformat(),'latency_ms':timing,'tokens_in':0,'tokens_out':0,'attempts':1})
            else: timing=cache.get(tr,cid,'transaction')['response']['latency_ms']
            result['transaction_latency_ms']=timing
            duplicate_ok=True
        final=result.get('args',{}); decision=result['decision']; rawobs=final.get('obligations',[])
        # Read stored resolved deadlines rather than assuming the model supplied dates.
        obrows=db.execute('SELECT o.*,d.deadline_kind,d.raw_text,d.resolved_date,d.anchor_event,d.offset_days,d.recurring_rule FROM obligations o JOIN obligation_deadlines d ON d.obligation_id=o.id WHERE o.decision_id=? ORDER BY o.id',(decision['decision_id'],)).fetchall()
        obs=[]
        for ob in obrows:
            obs.append({'type':ob['obligation_type'],'owed_by':ob['owed_by'],'clause_quote':ob['clause_quote'],'deadline':{'kind':ob['deadline_kind'],'resolved_date':ob['resolved_date']}})
        output={'schema_valid':'args' in result,'obligations':obs,'escalated':decision['escalated'],'escalation_codes':decision['escalation_codes']}
        trace_error=db.execute('SELECT error_class FROM tool_calls WHERE run_id=? AND error_class IS NOT NULL LIMIT 1',(run_id,)).fetchone()
        checks,matches=score(c,output,document,decision.get('error_class') or (trace_error[0] if trace_error else None))
        if not duplicate_ok: checks['exception']=True
        meta=[] if original is not None else result['metadata']; tin=sum(m.get('tokens_in',0) for m in meta); tout=sum(m.get('tokens_out',0) for m in meta)
        # Cached response metadata, not current pricing or replay timing, is authoritative.
        cost=sum(m['cost_usd'] for m in meta) if meta and all(m.get('cost_usd') is not None for m in meta) else (0 if not meta and (original is not None or not decision.get('error_class')) else None)
        latency=0 if original is not None else result.get('transaction_latency_ms')
        if original is None:
            with db:
                llm_hits=db.execute("SELECT count(*),min(cache_hit) FROM tool_calls WHERE run_id=? AND tool_name='llm_response'",(run_id,)).fetchone()
                db.execute('UPDATE runs SET latency_ms=?,tokens_in=?,tokens_out=?,cost_usd=?,cache_hit=? WHERE id=?',(latency,tin,tout,cost,int(bool(llm_hits[0]) and bool(llm_hits[1])),run_id))
        r={'case':c,'output':output,'document':document,'checks':checks,'matches':matches,'latency_ms':latency,'cost_usd':0 if original is not None else cost, 'result':result,'run_id':run_id,'retrieval_score':result.get('retrieval_score')}
        records.append(r); known[cid]=r; drifts.extend(result.get('drift',[]) if original is None else [])
        from agent.scoring import deadline_match,normal_ws
        counts={'gold_count':len(c['gold_obligations']),'matched_count':len(matches),'quote_count':len(obs),'grounded_quote_count':sum(bool(normal_ws(o['clause_quote'])) and normal_ws(o['clause_quote']) in normal_ws(document) for o in obs)}
        for kind in ('absolute','relative','recurring','none'):
            counts['deadline_'+kind+'_total']=sum(g['deadline']['kind']==kind for g in c['gold_obligations'])
            counts['deadline_'+kind+'_correct']=sum(g['deadline']['kind']==kind and deadline_match(g['deadline'],p['deadline']) for g,p in matches)
        rows.append({**counts,'case_id':cid,'class':c['class'],'difficulty':c.get('difficulty'),**checks,'gold_escalate':c['gold_should_escalate'],'escalated':output['escalated'],'error_class':decision.get('error_class') or (trace_error[0] if trace_error else None),'retrieval_score':r['retrieval_score'],'latency_ms':latency,'tokens_in':tin,'tokens_out':tout,'cost_usd':r['cost_usd'],'git_sha':gitsha(),'prompt_version':model['prompt_version'],'model':model['model'],'case_sha256':sha(casefiles[0]) if len(casefiles)==1 else ';'.join(sha(p) for p in casefiles),'thresholds_sha256':sha(ROOT/'config/thresholds.yaml'),'cache_dir':str(cache.path),'mode':'live' if a.live else 'replay'})
    metrics=aggregate(records); metrics['split']=a.split; metrics['mode']='live' if a.live else 'replay'
    columns=list(rows[0]); csvwrite(out/f'run_{a.split}_{stamp}.csv',rows,columns); csvwrite(run_dir/'cases.csv',rows,columns)
    csvwrite(out/'cost_latency.csv',rows,['case_id','latency_ms','tokens_in','tokens_out','cost_usd'])
    csvwrite(out/'deadline_breakdown.csv',[{'kind':k,**metrics['deadline_'+k]} for k in ('absolute','relative','recurring','none')],['kind','numerator','denominator','value','wilson_95'])
    csvwrite(out/'drift.csv',drifts,['case_id','seq','request_hash'])
    jsonwrite(run_dir/'metrics.json',metrics); jsonwrite(out/f'metrics_{a.split}.json',metrics)
    jsonwrite(run_dir/'run_metadata.json',{'split':a.split,'mode':metrics['mode'],'cases':len(cases),'case_sha256':rows[0]['case_sha256'],'git_sha':gitsha(),'prompt_version':model['prompt_version'],'threshold_sha256':rows[0]['thresholds_sha256']})
    # Per-case detail is intentionally isolated in the run directory; do not publish test before the completed freeze run.
    jsonwrite(run_dir/'details.json',[{'case':r['case'],'output':r['output'],'checks':r['checks'],'result':r['result'],'run_id':r['run_id'],'ungrounded_quotes':[o['clause_quote'] for o in r['output']['obligations'] if not normal_ws(o['clause_quote']) or normal_ws(o['clause_quote']) not in normal_ws(r['document'])]} for r in records])
    (out/f'summary_{a.split}.md').write_text(summary(metrics,'Evaluation: '+a.split)); db.close()
    if a.live and a.split=='test':
        if len(cases)!=30 or any('E6_TOOL_FAILURE' in r['output'].get('escalation_codes',[]) for r in records): raise ValueError('test run incomplete or contains execution errors; not marked valid')
        with (ROOT/'eval_results/test_run_log.jsonl').open('a') as f:
            f.write(canonical({**ACTIVE_TEST_ATTEMPT,'status':'completed','valid':True,'timestamp':stamp,'cases':len(cases)})+'\n')
        ACTIVE_TEST_ATTEMPT=None
    print(f'completed {len(cases)} cases; output: {run_dir}')

if __name__=='__main__':
    try: main(parser().parse_args())
    except Exception as e:
        if ACTIVE_TEST_ATTEMPT is not None:
            try:
                with (ROOT/'eval_results/test_run_log.jsonl').open('a') as f: f.write(canonical({**ACTIVE_TEST_ATTEMPT,'status':'failed','valid':False,'error_class':type(e).__name__})+'\n')
            except OSError: pass
        print(str(e),file=sys.stderr); sys.exit(3 if isinstance(e,CacheMiss) else 1)
