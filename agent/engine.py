"""Deterministic message construction and validated tool-calling execution."""
import json, time
from datetime import datetime, timezone
from jsonschema.exceptions import ValidationError
from jsonschema import Draft202012Validator
from .cache import CacheMiss
from .llm import complete, request_object
from .tool_schemas import schemas
from .tools import get_clause,get_document_dates,search_corpus,record_obligations,ClauseNotFound
from .loop import failure
from .retry import retry
from .escalation import conflict_candidates


def now(): return datetime.now(timezone.utc).isoformat()
def compact(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def initial_messages(prompt, party, context):
    return [{'role':'system','content':prompt},{'role':'user','content':compact({'intake_party':party,'business_context':context})}]

def run_agent(db, run_id, document_id, party, context, document, chunks, embed_query, llm_cache, config, descriptions, prompt, *, live=False, resume=False, case_id=None, precomputed_scores=None, throttle=None):
    types=[dict(r) for r in db.execute('SELECT * FROM obligation_types ORDER BY code')]
    if not types: raise ValueError('no human-authored obligation types loaded')
    if config.get('e1_floor') is None or config.get('e5_floor') is None: raise ValueError('E1 and E5 floors must be set before a run')
    tooldefs=schemas([t['code'] for t in types],descriptions)
    messages=initial_messages(prompt,party,context); seq=0; metadata=[]; drift=[]; invalid=0
    def log(name,args,result,error=None,retries=0,cache_hit=0,latency=0):
        nonlocal seq
        seq+=1
        with db:
            db.execute('INSERT INTO tool_calls(run_id,seq,tool_name,args_json,result_json,latency_ms,retry_count,error_class,cache_hit) VALUES(?,?,?,?,?,?,?,?,?)',(run_id,seq,name,compact(args),compact(result),latency,retries,error,int(cache_hit)))
    # Category queries come exclusively from the frozen human taxonomy.
    category_queries=sorted({(t['cuad_category'],t['name']) for t in types if t['cuad_category']})
    precheck=[]
    try:
        for category,query in category_queries:
            hits,_retries=retry(lambda:search_corpus(chunks,embed_query(query,seq+1),document_id,8),retryable=lambda e:isinstance(e,(OSError,TimeoutError)) and not isinstance(e,CacheMiss))
            eligible=[h for h in hits if h.get('clause_category')==category]
            precheck.extend(eligible)
    except CacheMiss: raise
    except Exception as e:
        log('retrieval_precheck',{}, {'error':str(e)},type(e).__name__,getattr(e,'retry_count',0))
        result=failure(db,run_id,'E6_TOOL_FAILURE',type(e).__name__,str(e))
        return {'decision':result,'metadata':metadata,'drift':drift,'retrieval_score':None}
    score=max((c['score'] for c in precheck),default=-1.0) if precomputed_scores is None else precomputed_scores
    evidence=sorted(precheck,key=lambda c:(-c['score'],str(c['chunk_id'])))[:8]
    log('retrieval_precheck',{'categories':[q[0] for q in category_queries]}, {'max_score':score,'evidence':evidence})
    if score < config['e1_floor']:
        result=record_obligations(db,run_id,{'obligations':[],'confidence':1.0,'escalate':True,'escalation_codes':['E1_NO_OBLIGATION']},{},config['e5_floor'])
        return {'decision':result,'args':{'obligations':[],'confidence':1.0,'escalate':True,'escalation_codes':['E1_NO_OBLIGATION']},'metadata':metadata,'drift':drift,'retrieval_score':score}
    for turn in range(config.get('max_turns',8)):
        req=request_object(config['model'],messages,tooldefs,'auto',config['temperature'],config['max_tokens'],config['corpus_version'],config.get('synthetic_document_sha256'))
        try:
            entry,hit,changed=complete(req,llm_cache,live=live,resume=resume,case_id=case_id,seq=seq+1,throttle=throttle,pricing=config.get('pricing'))
        except CacheMiss:
            with db: db.execute("UPDATE runs SET status='failed',finished_at=? WHERE id=?",(now(),run_id))
            raise
        except Exception as e:
            log('llm_response',{'turn':turn+1},{'error':str(e)},type(e).__name__,getattr(e,'retry_count',0))
            result=failure(db,run_id,'E6_TOOL_FAILURE',type(e).__name__,str(e),payload=req)
            return {'decision':result,'metadata':metadata,'drift':drift,'retrieval_score':score}
        meta=entry['metadata']; metadata.append(meta)
        if changed: drift.append({'request_hash':__import__('agent.cache',fromlist=['key_for']).key_for(req),'case_id':case_id,'seq':seq+1})
        try:
            message=entry['response']['choices'][0]['message']; calls=message.get('tool_calls') or []
        except (KeyError, IndexError, TypeError) as e:
            result=failure(db,run_id,'E6_TOOL_FAILURE','BAD_MODEL_RESPONSE',str(e)); return {'decision':result,'metadata':metadata,'drift':drift,'retrieval_score':score}
        # Record raw model responses, but request messages remain free of clocks and ids.
        log('llm_response',{'turn':turn+1},message,cache_hit=hit,latency=meta.get('latency_ms',0),retries=max(0,meta.get('attempts',1)-1))
        # Provider-generated IDs are not deterministic inputs. Normalize both
        # assistant and tool messages while retaining the raw response in trace.
        import copy
        calls=copy.deepcopy(calls)
        for i,call in enumerate(calls): call['id']=f'call_{turn+1}_{i+1}'
        assistant={'role':'assistant','content':message.get('content')}
        if calls: assistant['tool_calls']=calls
        messages.append(assistant)
        if not calls:
            messages.append({'role':'user','content':'Use a tool; finish with the terminal tool.'}); continue
        for call in calls:
            name=call.get('function',{}).get('name',''); raw=call.get('function',{}).get('arguments','{}'); call_id=call.get('id','')
            try:
                args=json.loads(raw)
                if not isinstance(args,dict): raise ValueError('tool arguments must be an object')
            except Exception:
                args={}; result={'error':'invalid JSON arguments'}; log(name,{'raw':raw},result,'INVALID_ARGUMENTS'); invalid += int(name=='record_obligations')
                messages.append({'role':'tool','tool_call_id':call_id,'content':compact(result)})
                if invalid>=2:
                    res=failure(db,run_id,'E4_SCHEMA_FAIL','SCHEMA_FAIL','invalid terminal arguments twice'); return {'decision':res,'metadata':metadata,'drift':drift,'retrieval_score':score}
                continue
            start=time.monotonic()
            try:
                spec=next((t['function']['parameters'] for t in tooldefs if t['function']['name']==name),None)
                if spec is None: raise ValueError('unknown tool')
                Draft202012Validator(spec).validate(args)
                if name=='record_obligations':
                    from .validate import validate_terminal
                    validate_terminal(args,[t['code'] for t in types])
                    if set(args['escalation_codes']) - {'E2_CONFLICTING_CLAUSES','E3_CONDITIONAL_OR_AMBIGUOUS'}: raise ValueError('system-owned escalation codes cannot be set by model')
                    # Whitespace-only normalization, identical to the scorer.
                    from .scoring import normal_ws
                    if any(not normal_ws(o['clause_quote']) or normal_ws(o['clause_quote']) not in normal_ws(document) for o in args['obligations']): raise ValueError('clause quote is not grounded')
                    from .dateparse import explicit_dates
                    for ob in args['obligations']:
                        deadline=ob['deadline']; raw=deadline.get('raw_text')
                        if deadline['kind']!='none' and (not raw or normal_ws(raw) not in normal_ws(document)): raise ValueError('deadline text is absent or not verbatim')
                        if deadline['kind']=='recurring' and (not deadline.get('recurring_rule') or normal_ws(deadline['recurring_rule']) not in normal_ws(document)): raise ValueError('recurrence rule is absent or not verbatim')
                        if deadline['kind']=='absolute':
                            dates_found=explicit_dates(raw)
                            if len(dates_found)!=1 or deadline.get('resolved_date') not in dates_found: raise ValueError('absolute deadline cannot be verified against verbatim text')
                    if 'E2_CONFLICTING_CLAUSES' in args['escalation_codes']:
                        # Require two distinct evidence excerpts before routing a conflict.
                        evidence_keys={(o['clause_category'],normal_ws(o['clause_quote'])) for o in args['obligations']}
                        for tr in db.execute("SELECT tool_name,args_json,result_json FROM tool_calls WHERE run_id=? AND tool_name IN ('retrieval_precheck','search_corpus','get_clause') ORDER BY seq",(run_id,)):
                            targs=json.loads(tr['args_json'] or '{}'); obj=json.loads(tr['result_json'] or '{}')
                            items=obj.get('evidence',[]) if isinstance(obj,dict) else obj if isinstance(obj,list) else []
                            for item in items:
                                if isinstance(item,dict):
                                    quote=item.get('text') or item.get('answer_text');cat=item.get('clause_category') or targs.get('category')
                                    if quote and cat: evidence_keys.add((cat,normal_ws(quote)))
                        if len(evidence_keys)<2: raise ValueError('conflict escalation requires two recorded clause excerpts')
                    dates=get_document_dates(db,document_id)
                    result=record_obligations(db,run_id,args,dates,config['e5_floor'])
                    categories=[o['clause_category'] for o in args['obligations']]
                    default_codes={t['code'] for t in types if t['escalates_by_default']}
                    result['conflict_crosscheck']={'candidate_pairs':conflict_candidates(categories),'default_types':[o['type'] for o in args['obligations'] if o['type'] in default_codes], 'model_flagged':'E2_CONFLICTING_CLAUSES' in args['escalation_codes']}
                    log(name,args,result,latency=round((time.monotonic()-start)*1000))
                    return {'decision':result,'args':args,'metadata':metadata,'drift':drift,'retrieval_score':score}
                else:
                    def invoke():
                        if name=='search_corpus':
                            if set(args)-{'query','top_k'} or not isinstance(args.get('query'),str) or not args['query'].strip() or type(args.get('top_k',8)) is not int or args.get('top_k',8)<1: raise ValueError('invalid search arguments')
                            return search_corpus(chunks,embed_query(args['query'],seq+1),document_id,args.get('top_k',8))
                        if name=='get_clause':
                            if set(args)!={'document_id','category'} or args['document_id']!=document_id: raise ValueError('document access denied or invalid arguments')
                            return get_clause(db,document_id,args['category'])
                        if name=='get_document_dates':
                            if set(args)!={'document_id'} or args['document_id']!=document_id: raise ValueError('document access denied or invalid arguments')
                            return get_document_dates(db,document_id)
                        raise ValueError('unknown tool')
                    result,retries=retry(invoke,retryable=lambda e:isinstance(e,(OSError,TimeoutError)) and not isinstance(e,CacheMiss))
                    log(name,args,result,retries=retries,latency=round((time.monotonic()-start)*1000))
            except ClauseNotFound as e:
                result={'error':'ClauseNotFound','category':str(e)}
                log(name,args,result,'ClauseNotFound',latency=round((time.monotonic()-start)*1000))
            except CacheMiss: raise
            except (ValidationError, ValueError, TypeError) as e:
                invalid += int(name=='record_obligations'); result={'error':str(e)}
                log(name,args,result,'VALIDATION_ERROR',latency=round((time.monotonic()-start)*1000))
                if invalid>=2:
                    res=failure(db,run_id,'E4_SCHEMA_FAIL','SCHEMA_FAIL',str(e)); return {'decision':res,'metadata':metadata,'drift':drift,'retrieval_score':score}
            except Exception as e:
                result={'error':str(e)}; log(name,args,result,type(e).__name__,retries=getattr(e,'retry_count',0),latency=round((time.monotonic()-start)*1000))
                res=failure(db,run_id,'E6_TOOL_FAILURE',type(e).__name__,str(e),payload={'tool':name,'args':args}); return {'decision':res,'metadata':metadata,'drift':drift,'retrieval_score':score}
            messages.append({'role':'tool','tool_call_id':call_id,'content':compact(result)})
    res=failure(db,run_id,'E4_SCHEMA_FAIL','LOOP_EXHAUSTED','no terminal call in max_turns')
    return {'decision':res,'metadata':metadata,'drift':drift,'retrieval_score':score}
