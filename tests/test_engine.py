import json, socket, subprocess, sys, os
from pathlib import Path
import pytest
from agent.cache import Cache, CacheMiss
from agent.db import initialize
from agent.engine import run_agent, initial_messages
from agent.intake import begin
from agent.llm import request_object
from agent.tool_schemas import schemas
from agent.retry import retry
from agent.escalation import conflict_candidates
from agent.tools import get_document_dates

@pytest.fixture
def data(tmp_path):
    db=initialize(tmp_path/'db.sqlite')
    with db:
        db.execute("INSERT INTO corpus_documents(id,title) VALUES('x','fixture')")
        db.execute("INSERT INTO obligation_types(code,name,cuad_category,deadline_behaviour,escalates_by_default) VALUES('T','duty','category','none',0)")
    versions={'model':'mock','prompt_version':'system_v1','schema_version':'1','corpus_version':'fixture'}
    rid=begin(db,'ref','x','customer',None,'fixture',versions)[0]
    config={**versions,'e1_floor':0.,'e5_floor':.5,'temperature':0,'max_tokens':100,'max_turns':8}
    desc={n:n for n in ('search_corpus','get_clause','get_document_dates','record_obligations')}
    chunks=[{'chunk_id':'1','document_id':'x','clause_category':'category','text':'fixture evidence','embedding':[1.0]}]
    return db,rid,config,desc,chunks

def args():
    return {'obligations':[{'type':'T','description':'fixture','owed_by':'customer','clause_category':'category','clause_quote':'fixture evidence','consequence':None,'deadline':{'kind':'none','raw_text':None},'confidence':.9}], 'confidence':.9,'escalate':False,'escalation_codes':[]}

def cache_reply(cache,cfg,desc,arguments):
    req=request_object('mock',initial_messages('instructions','customer',None),schemas(['T'],desc),'auto',0,100,'fixture')
    response={'choices':[{'message':{'role':'assistant','content':None,'tool_calls':[{'id':'call-1','type':'function','function':{'name':'record_obligations','arguments':json.dumps(arguments)}}]}}]}
    cache.put(req,response,{'latency_ms':11,'tokens_in':12,'tokens_out':3,'attempts':1})
    return req

def test_replay_full_terminal_and_trace(data,tmp_path):
    db,rid,cfg,desc,chunks=data; cache=Cache(tmp_path/'cache');cache_reply(cache,cfg,desc,args())
    res=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],cache,cfg,desc,'instructions',case_id='synthetic')
    assert not res['decision']['escalated']
    assert [r[0] for r in db.execute('select tool_name from tool_calls order by seq')]==['retrieval_precheck','llm_response','record_obligations']
    assert db.execute('select clause_quote from obligations').fetchone()[0]=='fixture evidence'
    assert res['metadata'][0]['latency_ms']==11

def test_e1_skips_model(data,tmp_path):
    db,rid,cfg,desc,chunks=data;cfg['e1_floor']=1.1
    out=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],Cache(tmp_path),cfg,desc,'instructions')
    assert out['decision']['escalation_codes']==['E1_NO_OBLIGATION']
    assert db.execute('select count(*) from tool_calls where tool_name="llm_response"').fetchone()[0]==0

def test_cache_miss_no_live_fallback(data,tmp_path):
    db,rid,cfg,desc,chunks=data
    with pytest.raises(CacheMiss): run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],Cache(tmp_path),cfg,desc,'instructions')
    assert db.execute('select status from runs').fetchone()[0]=='failed'

def test_conflict_candidate_not_judgment():
    assert conflict_candidates(['Cap On Liability','Uncapped Liability'])==[['Cap On Liability','Uncapped Liability']]
    assert not conflict_candidates(['Cap On Liability'])

def test_retries_then_failure():
    calls=[]; waits=[]
    def f(): calls.append(1); raise TimeoutError('down')
    with pytest.raises(TimeoutError) as e: retry(f,3,sleeper=waits.append,jitter=lambda:0)
    assert len(calls)==3 and waits==[1,2] and e.value.retry_count==2

def test_date_label_parse_and_conflict(data):
    db,*_=data
    with db: db.execute("INSERT INTO clause_labels(document_id,category,answer_text,char_start) VALUES('x','Effective Date','effective March 1, 2025',0)")
    assert get_document_dates(db,'x')['effective_date']=='2025-03-01'
    with db: db.execute("INSERT INTO clause_labels(document_id,category,answer_text,char_start) VALUES('x','Effective Date','February 1, 2025',10)")
    assert get_document_dates(db,'x')['effective_date'] is None

def test_socket_network_prohibited():
    env={**os.environ,'B2_OFFLINE':'1'}
    code="import agent, socket; s=socket.socket(); s.connect(('127.0.0.1',9))"
    p=subprocess.run([sys.executable,'-c',code],env=env,capture_output=True,text=True)
    assert p.returncode and 'B2_OFFLINE prohibits' in p.stderr

def test_digest_test_guard(tmp_path):
    (tmp_path/'run_metadata.json').write_text('{"split":"test"}')
    p=subprocess.run([sys.executable,'scripts/failure_digest.py','--run',str(tmp_path),'--out',str(tmp_path/'out')],capture_output=True,text=True)
    assert p.returncode and 'refuses' in p.stderr and not (tmp_path/'out').exists()

def test_system_codes_not_in_model_schema():
    d={n:n for n in ('search_corpus','get_clause','get_document_dates','record_obligations')}
    allowed=schemas(['T'],d)[-1]['function']['parameters']['properties']['escalation_codes']['items']['enum']
    assert 'E5_LOW_CONFIDENCE' not in allowed

def test_end_to_end_replay_offline_and_cache_miss(tmp_path):
    import shutil, yaml, hashlib
    from agent.cache import canonical
    root=Path(__file__).resolve().parents[1]; project=tmp_path/'repo'
    shutil.copytree(root,project,ignore=shutil.ignore_patterns('.venv','__pycache__','.pytest_cache','b2.sqlite','.git'))
    # Hermetic fixture: ignore any real corpus built in the source tree (Phase B+).
    (project/'corpus/selection.json').unlink(missing_ok=True); shutil.rmtree(project/'corpus/embeddings',ignore_errors=True)
    db=initialize(project/'db/b2.sqlite')
    with db:
        db.execute("INSERT INTO corpus_documents(id,title) VALUES('fixture','Fixture')")
        db.execute("INSERT INTO obligation_types(code,name,cuad_category,deadline_behaviour) VALUES('T','duty','category','none')")
    db.close()
    (project/'guide/obligation_types.yaml').write_text(yaml.safe_dump({'categories':[{'category':'category','include':True,'code':'T','name':'duty','deadline_behaviour':'none','escalates_by_default':False}]}))
    config=yaml.safe_load((project/'config/model.yaml').read_text()); config.update(model='mock',corpus_version='fixture',max_tokens=100,embedding_model='fake')
    (project/'config/model.yaml').write_text(yaml.safe_dump(config)); (project/'config/thresholds.yaml').write_text('e1: {value: 0.0, provenance: provisional}\ne5: {value: 0.5, provenance: provisional}\n')
    (project/'corpus/documents/fixture.txt').write_text('fixture evidence')
    (project/'corpus/embeddings').mkdir(parents=True,exist_ok=True); (project/'cases').mkdir(parents=True,exist_ok=True)
    from agent.lean_index import save,sha
    save(project/'corpus/embeddings',[{'chunk_id':'1','doc_id':'fixture','clause_category':'category','char_start':0,'char_end':16}],[[1.]],'fake',document_hashes={'fixture':sha(project/'corpus/documents/fixture.txt')})
    case={'id':'fixture','document_id':'fixture','intake_party':'customer','class':'clear','gold_obligations':[{'type':'T','owed_by':'customer','deadline':{'kind':'none'}}], 'gold_should_escalate':False,'gold_escalation_codes':[]}
    (project/'corpus/documents/duplicate-fixture.txt').write_text('fixture evidence')
    duplicate={**case,'id':'copy','document_id':'duplicate-fixture','duplicate_of':'fixture'}
    (project/'cases/dev.json').write_text(json.dumps([case,duplicate]));cache=Cache(project/'cache/llm')
    cache.put({'kind':'embed','model_id':'fake','text':'duty'},[1.],{'latency_ms':0})
    prompt=(project/'prompts/system_v1.md').read_text();desc=yaml.safe_load((project/'config/tool_descriptions.yaml').read_text())
    req=request_object('mock',initial_messages(prompt,'customer',None),schemas(['T'],desc),'auto',0,100,'fixture')
    msg={'role':'assistant','content':None,'tool_calls':[{'id':'mock-call','type':'function','function':{'name':'record_obligations','arguments':json.dumps(args())}}]}
    cache.put(req,{'choices':[{'message':msg}]},{'latency_ms':11,'tokens_in':5,'tokens_out':2,'attempts':1})
    tr={'kind':'transaction','case_hash':hashlib.sha256(canonical(case).encode()).hexdigest(),'model':'mock','prompt_version':'system_v1','corpus_version':'fixture','e1_floor':0.0}
    cache.put(tr,{'latency_ms':22},{'latency_ms':22})
    env={**os.environ,'B2_OFFLINE':'1'}
    p=subprocess.run([sys.executable,'run_eval.py','--split','dev'],cwd=project,env=env,capture_output=True,text=True)
    assert p.returncode==0,p.stderr
    m=json.loads((project/'eval_results/metrics_dev.json').read_text())
    assert m['exception_rate']['value']==0 and m['latency']['p50_ms']==11
    import csv
    with next((project/'eval_results').glob('run_dev_*.csv')).open() as f: rr=list(csv.DictReader(f))
    assert rr[1]['tokens_in']=='0' and rr[1]['tokens_out']=='0' and rr[1]['cost_usd']=='0'
    # A missing request must be error 3, without HTTP fallback.
    (project/'cache/llm'/(__import__('agent.cache',fromlist=['key_for']).key_for(req)+'.json')).unlink()
    p=subprocess.run([sys.executable,'run_eval.py','--split','dev'],cwd=project,env=env,capture_output=True,text=True)
    assert p.returncode==3 and 'incomplete cache' in p.stderr

def test_model_failure_goes_to_dead_letter(data,tmp_path,monkeypatch):
    from agent import engine
    db,rid,cfg,desc,chunks=data
    def down(*a,**k):
        err=TimeoutError('offline mock'); err.retry_count=2; raise err
    monkeypatch.setattr(engine,'complete',down)
    out=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],Cache(tmp_path),cfg,desc,'instructions')
    assert out['decision']['escalation_codes']==['E6_TOOL_FAILURE']
    assert db.execute('select error_class from dead_letter').fetchone()[0]=='TimeoutError'
    assert db.execute("select retry_count from tool_calls where tool_name='llm_response'").fetchone()[0]==2
    assert db.execute('select queue from escalations').fetchone()[0]=='engineering'

def test_model_e2_and_default_crosscheck(data,tmp_path):
    db,rid,cfg,desc,chunks=data
    with db: db.execute("UPDATE obligation_types SET escalates_by_default=1 WHERE code='T'")
    a=args(); a['obligations'].append({**a['obligations'][0],'clause_quote':'evidence'});a['escalate']=True; a['escalation_codes']=['E2_CONFLICTING_CLAUSES']
    cache=Cache(tmp_path);cache_reply(cache,cfg,desc,a)
    out=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],cache,cfg,desc,'instructions')
    assert out['decision']['escalation_codes']==['E2_CONFLICTING_CLAUSES']
    assert out['decision']['conflict_crosscheck']['default_types']==['T','T']
    assert db.execute('select queue from escalations').fetchone()[0]=='legal-ops'

def test_default_escalation_never_silently_cleared(data,tmp_path):
    db,rid,cfg,desc,chunks=data
    with db: db.execute("UPDATE obligation_types SET escalates_by_default=1 WHERE code='T'")
    cache=Cache(tmp_path);cache_reply(cache,cfg,desc,args())
    out=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],cache,cfg,desc,'instructions')
    assert out['decision']['escalation_codes']==['E3_CONDITIONAL_OR_AMBIGUOUS']

def test_mocked_groq_429_retries_exhaust(monkeypatch,tmp_path):
    import requests
    from agent import llm
    from agent.retry import retry
    monkeypatch.setattr(llm,'ensure_online',lambda:None)
    monkeypatch.setenv('GROQ_API_KEY','fake')
    monkeypatch.setattr(llm,'retry',lambda fn,retryable:retry(fn,retryable=retryable,sleeper=lambda _:None,jitter=lambda:0))
    calls=[]
    def post(*a,**kw):
        calls.append(1); r=requests.Response();r.status_code=429;r.url='https://example.invalid';return r
    req=request_object('mock',[],[],'auto',0,10,'fixture')
    with pytest.raises(requests.HTTPError) as e: llm.complete(req,Cache(tmp_path),live=True,post=post)
    assert len(calls)==3 and e.value.retry_count==2

def test_heldout_digest_and_calibration_refuse_before_freeze(tmp_path):
    (tmp_path/'run_metadata.json').write_text('{"split":"test"}')
    for script,args_ in [('scripts/failure_digest.py',['--run',str(tmp_path),'--out',str(tmp_path/'out'),'--post-freeze']),('scripts/calibrate_floors.py',['--run',str(tmp_path)])]:
        p=subprocess.run([sys.executable,script,*args_],capture_output=True,text=True)
        assert p.returncode!=0

def test_heldout_eval_refuses_before_freeze():
    p=subprocess.run([sys.executable,'run_eval.py','--split','test'],capture_output=True,text=True,env={**os.environ,'B2_OFFLINE':'1'})
    assert p.returncode!=0

def test_pre_push_guard_blocks_deleted_protected_history(tmp_path):
    import shutil
    repo=tmp_path/'repo';repo.mkdir();(repo/'scripts').mkdir();shutil.copy(Path('scripts/pre_push_guard.py'),repo/'scripts/pre_push_guard.py')
    def git(*x): subprocess.run(['git',*x],cwd=repo,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    git('init');git('config','user.email','test@example.invalid');git('config','user.name','Test')
    (repo/'safe.txt').write_text('safe');git('add','safe.txt');git('commit','-m','first')
    (repo/'cases').mkdir();(repo/'cases/test.json').write_text('[]');git('add','cases/test.json');git('commit','-m','unsafe')
    git('rm','cases/test.json');git('commit','-m','remove')
    p=subprocess.run([sys.executable,'scripts/pre_push_guard.py'],cwd=repo,input='',capture_output=True,text=True)
    assert p.returncode and 'protected paths in outgoing commit' in p.stderr

def test_all_fixture_request_hashes_match_in_separate_processes():
    env={**os.environ,'B2_OFFLINE':'1','PYTHONPATH':str(Path('.').resolve())}
    def run(): return json.loads(subprocess.check_output([sys.executable,'tests/determinism_probe.py'],env=env,text=True))
    first,second=run(),run()
    assert len(first)==2 and first==second

def test_recurring_anchor_rules_and_unresolved():
    from agent.deadlines import resolve
    d,_=resolve({'kind':'recurring','recurring_rule':'monthly after effective date'}, {'effective_date':'2025-01-31'})
    assert d['resolved_date']=='2025-02-28'
    d,unresolved=resolve({'kind':'recurring','recurring_rule':'monthly after delivery'}, {'effective_date':'2025-01-31'})
    assert d['resolved_date'] is None and unresolved
    _,unresolved=resolve({'kind':'recurring','recurring_rule':'anniversary of termination'}, {'effective_date':'2025-01-31'})
    assert unresolved

def test_prompt_hygiene_checks_corpus_and_identifiers(tmp_path):
    from scripts.prompt_hygiene import check
    (tmp_path/'corpus/documents').mkdir(parents=True);(tmp_path/'prompts').mkdir(); (tmp_path/'config').mkdir()
    (tmp_path/'corpus/documents/DOCXYZ001.txt').write_text('one two three four five six seven eight nine')
    (tmp_path/'prompts/system.md').write_text('one two three four five six seven eight')
    with pytest.raises(ValueError,match='corpus text'): check(tmp_path)
    (tmp_path/'prompts/system.md').write_text('Use DOCXYZ001 as an example')
    with pytest.raises(ValueError,match='document or case id'): check(tmp_path)

def test_e5_floor_recomputes_without_request_drift(data,tmp_path):
    db,rid,cfg,desc,chunks=data; a=args();a['obligations'][0]['confidence']=.55
    cache=Cache(tmp_path);cache_reply(cache,cfg,desc,a)
    one=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],cache,cfg,desc,'instructions')
    rid2=begin(db,'other-ref','x','customer',None,'fixture',cfg)[0]
    cfg['e5_floor']=.6
    two=run_agent(db,rid2,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],cache,cfg,desc,'instructions')
    assert one['decision']['escalation_codes']==[] and two['decision']['escalation_codes']==['E5_LOW_CONFIDENCE']

def test_engine_two_invalid_terminal_calls_go_to_engineering(data,tmp_path,monkeypatch):
    from agent import engine
    db,rid,cfg,desc,chunks=data; calls=[]
    def invalid(req,*args,**kw):
        calls.append(req)
        msg={'role':'assistant','content':None,'tool_calls':[{'id':'model-id','type':'function','function':{'name':'record_obligations','arguments':'{}'}}]}
        return {'response':{'choices':[{'message':msg}]},'metadata':{'latency_ms':0,'attempts':1}}, True,False
    monkeypatch.setattr(engine,'complete',invalid)
    out=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],Cache(tmp_path),cfg,desc,'instructions')
    assert len(calls)==2 and out['decision']['escalation_codes']==['E4_SCHEMA_FAIL']
    assert db.execute('select count(*) from tool_calls where error_class="VALIDATION_ERROR"').fetchone()[0]==2
    assert db.execute('select queue from escalations').fetchone()[0]=='engineering'

def test_e2_conflict_pair_crosscheck(data,tmp_path,monkeypatch):
    from agent import engine
    db,rid,cfg,desc,chunks=data
    with db:
        db.execute("UPDATE obligation_types SET cuad_category='Cap On Liability',escalates_by_default=1 WHERE code='T'")
        db.execute("INSERT INTO obligation_types(code,name,cuad_category,deadline_behaviour,escalates_by_default) VALUES('U','other','Uncapped Liability','none',1)")
    chunks[0]['clause_category']='Cap On Liability'
    a=args();a['obligations'][0]['clause_category']='Cap On Liability';a['obligations'].append({**a['obligations'][0],'type':'U','clause_category':'Uncapped Liability'});a.update(escalate=True,escalation_codes=['E2_CONFLICTING_CLAUSES'])
    def response(req,*args,**kw):
        msg={'role':'assistant','content':None,'tool_calls':[{'id':'x','type':'function','function':{'name':'record_obligations','arguments':json.dumps(a)}}]}
        return {'response':{'choices':[{'message':msg}]},'metadata':{'latency_ms':0,'attempts':1}},True,False
    monkeypatch.setattr(engine,'complete',response)
    out=run_agent(db,rid,'x','customer',None,'fixture evidence',chunks,lambda q,s:[1.],Cache(tmp_path),cfg,desc,'instructions')
    cross=out['decision']['conflict_crosscheck']
    assert cross['candidate_pairs']==[['Cap On Liability','Uncapped Liability']] and set(cross['default_types'])=={'T','U'} and cross['model_flagged']

def test_calibration_dev_only_and_records_provenance(tmp_path,monkeypatch):
    from scripts import calibrate_floors as cal
    import yaml
    (tmp_path/'eval_results').mkdir();(tmp_path/'config').mkdir();run=tmp_path/'dev';run.mkdir()
    (run/'run_metadata.json').write_text('{"split":"dev"}')
    (tmp_path/'config/splits.yaml').write_text('dev: {clear: 26}\n')
    rows=[]
    for i in range(26):
        positive=i<13
        rows.append({'case':{'gold_should_escalate':positive,'gold_escalation_codes':['E1_NO_OBLIGATION'] if positive else []},'result':{'retrieval_score':0.2 if positive else .9,'decision':{'escalation_codes':[]},'args':{'confidence':.9,'obligations':[]}}})
    (run/'details.json').write_text(json.dumps(rows));monkeypatch.setattr(cal,'ROOT',tmp_path)
    cal.main(run)
    conf=yaml.safe_load((tmp_path/'config/thresholds.yaml').read_text())
    assert conf['e1']['provenance']=='dev-sweep' and conf['e5']['value']==.5 and len(conf['calibration_sha256'])==64
    (tmp_path/'eval_results/test_run_log.jsonl').write_text('{"status":"completed","valid":true}\n')
    with pytest.raises(ValueError,match='forbidden'): cal.main(run)

def test_release_replay_and_readme_from_synthetic_frozen_fixture(tmp_path):
    """Synthetic only: simulate a logged completion, never invoke a real model."""
    import shutil,yaml,hashlib,csv
    from agent.cache import canonical
    root=Path(__file__).resolve().parents[1];project=tmp_path/'repo'
    shutil.copytree(root,project,ignore=shutil.ignore_patterns('.venv','__pycache__','.pytest_cache','b2.sqlite','.git'))
    # Hermetic fixture: ignore any real corpus built in the source tree (Phase B+).
    (project/'eval_results/dev_run_log.jsonl').unlink(missing_ok=True); (project/'eval_results/test_run_log.jsonl').unlink(missing_ok=True)
    (project/'corpus/selection.json').unlink(missing_ok=True); shutil.rmtree(project/'corpus/embeddings',ignore_errors=True)
    db=initialize(project/'db/b2.sqlite')
    with db:
        db.execute("INSERT INTO corpus_documents(id,title) VALUES('fixture','Fixture')")
        db.execute("INSERT INTO obligation_types(code,name,cuad_category,deadline_behaviour) VALUES('T','duty','category','none')")
    db.close()
    (project/'guide/obligation_types.yaml').write_text(yaml.safe_dump({'categories':[{'category':'category','include':True,'code':'T','name':'duty','deadline_behaviour':'none','escalates_by_default':False}]}))
    model=yaml.safe_load((project/'config/model.yaml').read_text());model.update(model='mock',corpus_version='fixture',max_tokens=100,embedding_model='fake')
    (project/'config/model.yaml').write_text(yaml.safe_dump(model))
    report=project/'eval_results/threshold_calibration.md';report.write_text('synthetic calibration\n')
    (project/'config/thresholds.yaml').write_text(yaml.safe_dump({'e1':{'value':0.0,'provenance':'dev-sweep'},'e5':{'value':0.5,'provenance':'dev-sweep'},'calibration_sha256':hashlib.sha256(report.read_bytes()).hexdigest()}))
    (project/'corpus/documents/fixture.txt').write_text('fixture evidence')
    from agent.lean_index import save,sha
    save(project/'corpus/embeddings',[{'chunk_id':'1','doc_id':'fixture','clause_category':'category','char_start':0,'char_end':16}],[[1.]],'fake',document_hashes={'fixture':sha(project/'corpus/documents/fixture.txt')})
    counts={'clear':12,'conflicting':9,'out_of_scope':5,'adversarial':4};cases=[]
    for cls,n in counts.items():
        for i in range(n): cases.append({'id':f'{cls}-{i}','document_id':'fixture','intake_party':'customer','class':cls,'gold_obligations':[],'gold_should_escalate':False,'gold_escalation_codes':[]})
    (project/'cases').mkdir(parents=True,exist_ok=True)
    raw=json.dumps(cases);(project/'cases/test.json').write_text(raw);checksum=hashlib.sha256(raw.encode()).hexdigest()
    (project/'cases/FROZEN.sha256').write_text(checksum+'  cases/test.json\n')
    dev_counts={'clear':14,'conflicting':5,'out_of_scope':5,'adversarial':2}
    dev=[{'id':f'dev-{cls}-{i}','class':cls,'document_id':'fixture'} for cls,n in dev_counts.items() for i in range(n)]
    (project/'cases/dev.json').write_text(json.dumps(dev))
    # Pure fixture: seal a dummy local-only synthetic shard before the code tag.
    from agent.synthetic import open_output
    testdb,folder,manifest=open_output(project,'test')
    with testdb: testdb.execute("INSERT INTO corpus_documents(id,title,char_count) VALUES('synthetic-fixture','Fixture',1)")
    testdb.close();(folder/'synthetic-fixture.txt').write_text('x');manifest.write_text('{}')
    save(project/'corpus/synthetic_test/index',[{'chunk_id':'x','doc_id':'synthetic-fixture','clause_category':None,'char_start':0,'char_end':1}],[[1.]],'fake',document_hashes={'synthetic-fixture':sha(folder/'synthetic-fixture.txt')})
    from scripts.freeze_test_synthetics import seal
    seal(project)
    def git(*args): subprocess.run(['git',*args],cwd=project,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    git('init');git('config','user.email','test@example.invalid');git('config','user.name','Test');git('add','.');git('commit','-m','synthetic fixture');git('tag','guide-v1.0');git('tag','code-frozen')
    cache=Cache(project/'cache/llm');cache.put({'kind':'embed','model_id':'fake','text':'duty'},[1.],{'latency_ms':0})
    prompt=(project/'prompts/system_v1.md').read_text();desc=yaml.safe_load((project/'config/tool_descriptions.yaml').read_text())
    req=request_object('mock',initial_messages(prompt,'customer',None),schemas(['T'],desc),'auto',0,100,'fixture')
    terminal={'obligations':[],'confidence':.9,'escalate':False,'escalation_codes':[]}
    msg={'role':'assistant','content':None,'tool_calls':[{'id':'random','type':'function','function':{'name':'record_obligations','arguments':json.dumps(terminal)}}]}
    cache.put(req,{'choices':[{'message':msg}]},{'latency_ms':9,'tokens_in':5,'tokens_out':2,'attempts':1,'cost_usd':.001})
    for case in cases:
        tr={'kind':'transaction','case_hash':hashlib.sha256(canonical(case).encode()).hexdigest(),'model':'mock','prompt_version':'system_v1','corpus_version':'fixture','e1_floor':0.0}
        cache.put(tr,{'latency_ms':22},{'latency_ms':22})
    env={**os.environ,'B2_OFFLINE':'1'}
    p=subprocess.run([sys.executable,'run_eval.py','--split','test'],cwd=project,env=env,capture_output=True,text=True)
    assert p.returncode and 'completed valid live test run' in p.stderr
    log={'status':'completed','valid':True,'mode':'live','cases':30,'case_sha256':checksum}
    (project/'eval_results/test_run_log.jsonl').write_text(json.dumps({'status':'started','mode':'live','attempt_id':'synthetic'})+'\n'+json.dumps(log)+'\n')
    for cmd in ([sys.executable,'run_eval.py','--split','test'],[sys.executable,'scripts/render_readme.py'],[sys.executable,'check_readme.py']):
        p=subprocess.run(cmd,cwd=project,env=env,capture_output=True,text=True)
        assert p.returncode==0,p.stderr
    again=subprocess.run([sys.executable,'run_eval.py','--split','test'],cwd=project,env=env,capture_output=True,text=True)
    assert again.returncode==0,again.stderr
    text=(project/'README.md').read_text();assert '0.0% (0/30;' in text and 'live test runs executed: 1' in text.lower()
    (project/'README.md').write_text(text.replace('0.0% (0/30;', '1.0% (0/30;',1))
    assert subprocess.run([sys.executable,'check_readme.py'],cwd=project,env=env,capture_output=True).returncode!=0
