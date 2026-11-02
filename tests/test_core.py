import os, json, sqlite3, subprocess, sys
from datetime import date
import pytest
from jsonschema.exceptions import ValidationError
from agent.db import initialize
from agent.cache import Cache, CacheMiss, key_for, ensure_online
from agent.deadlines import resolve
from agent.escalation import apply_floor
from agent.intake import begin
from agent.tools import get_clause, ClauseNotFound, record_obligations, search_corpus
from agent.scoring import deadline_match,score
from agent.metrics import wilson
from agent.loop import run_loop

@pytest.fixture
def db(tmp_path):
    d=initialize(tmp_path/'test.sqlite')
    with d:
        d.execute("INSERT INTO corpus_documents(id,title) VALUES('d','Document')")
        d.execute("INSERT INTO obligation_types(code,name,deadline_behaviour) VALUES('T','Test','none')")
    yield d
    d.close()

def start(db, ref='x'):
    return begin(db,ref,'d','customer',None,'test',{'model':'test','prompt_version':'1','schema_version':'1','corpus_version':'1'})[0]

def args():
    return {'obligations':[{'type':'T','description':'Duty','owed_by':'customer','clause_category':'Category','clause_quote':'actual quote','consequence':None,'deadline':{'kind':'none','raw_text':None},'confidence':0.9}], 'confidence':0.9,'escalate':False,'escalation_codes':[]}

def test_foreign_keys(db):
    with pytest.raises(sqlite3.IntegrityError): db.execute("INSERT INTO clause_labels(document_id,category) VALUES('missing','X')")

def test_terminal_atomic_and_unique(db):
    r=start(db); record_obligations(db,r,args(),{},0.5)
    with pytest.raises(sqlite3.IntegrityError): record_obligations(db,r,args(),{},0.5)
    assert db.execute('select count(*) from decisions').fetchone()[0]==1

def test_absolute_check(db):
    r=start(db); record_obligations(db,r,args(),{},0.5)
    oid=db.execute('select id from obligations').fetchone()[0]
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO obligation_deadlines(obligation_id,deadline_kind) VALUES(?,'absolute')",(oid,))

def test_midwrite_rollback(db):
    r=start(db)
    db.execute("CREATE TRIGGER fail_deadline BEFORE INSERT ON obligation_deadlines BEGIN SELECT RAISE(ABORT, 'failure'); END;"); db.commit()
    with pytest.raises(sqlite3.IntegrityError): record_obligations(db,r,args(),{},0.5)
    assert db.execute('SELECT count(*) FROM decisions').fetchone()[0]==0
    assert db.execute('SELECT count(*) FROM obligations').fetchone()[0]==0

def test_idempotency_and_conflict(db):
    r=start(db); assert start(db)==r
    with pytest.raises(ValueError): begin(db,'x','d','provider',None,'test',{'model':'a','prompt_version':'1','schema_version':'1','corpus_version':'1'})

def test_cache_round_trip_and_miss(tmp_path):
    c=Cache(tmp_path); req={'kind':'embed','text':'x','model_id':'m'}
    with pytest.raises(CacheMiss): c.get(req,'case',1)
    c.put(req,[1.0],{'latency_ms':5}); assert c.get(req)['response']==[1.0]
    assert key_for({'b':1,'a':2})==key_for({'a':2,'b':1})

def test_cross_process_hash():
    code="from agent.cache import key_for; print(key_for({'b':[1,2],'a':'test'}))"
    a=subprocess.check_output([sys.executable,'-c',code]); b=subprocess.check_output([sys.executable,'-c',code]); assert a==b

def test_offline(monkeypatch):
    monkeypatch.setenv('B2_OFFLINE','1')
    with pytest.raises(RuntimeError): ensure_online()

def test_deadlines():
    assert resolve({'kind':'absolute','resolved_date':'2027-01-01'},{})[0]['resolved_date']=='2027-01-01'
    assert resolve({'kind':'relative','anchor_event':'effective_date','offset_days':30},{'effective_date':'2026-01-01'})[0]['resolved_date']=='2026-01-31'
    assert resolve({'kind':'relative','anchor_event':'termination','offset_days':1},{})[1]
    assert resolve({'kind':'recurring','recurring_rule':'each anniversary'},{'effective_date':'2024-02-29'})[0]['resolved_date']=='2025-02-28'
    assert resolve({'kind':'none'}, {})[0]['resolved_date'] is None
    with pytest.raises(ValueError): resolve({'kind':'absolute'}, {})

def test_e5():
    assert apply_floor(.8,[{'confidence':.4}],[],.5)==['E5_LOW_CONFIDENCE']
    with pytest.raises(ValueError): apply_floor(.9,[],[],None)

def test_quote_and_deadline():
    a={'gold_obligations':[{'type':'T','owed_by':'customer','deadline':{'kind':'none'}}],'gold_should_escalate':False}
    p={'schema_valid':True,'obligations':args()['obligations'],'escalated':False}
    assert not score(a,p,'actual\nquote')[0]['exception']
    assert score(a,p,'unrelated')[0]['exception']
    assert deadline_match({'kind':'relative','resolved_date':'2026-02-01'},{'kind':'relative','resolved_date':'2026-02-02'})

def test_wilson():
    low, high=wilson(15,30); assert 0.33 < low < 0.34 and 0.66 < high < 0.67
    assert wilson(0,0) is None

def test_clause_not_found(db):
    with pytest.raises(ClauseNotFound): get_clause(db,'d','missing')

def test_search_ties():
    rows=[{'chunk_id':x,'document_id':'d','embedding':[1,0]} for x in ['b','a']]
    assert [x['chunk_id'] for x in search_corpus(rows,[1,0],'d')]==['a','b']

def test_invalid_terminal_twice(db):
    r=start(db)
    def bad(history): return 'record_obligations',{}
    result=run_loop(db,r,bad,{}, {},.5)
    assert result['escalation_codes']==['E4_SCHEMA_FAIL']
    assert db.execute('select count(*) from tool_calls').fetchone()[0]==2

def test_loop_exhaustion(db):
    r=start(db)
    result=run_loop(db,r,lambda h:('other',{}),{'other':lambda: 'ok'},{},.5,max_turns=2)
    assert result['error_class']=='LOOP_EXHAUSTED'

def test_anchor_unresolved_escalates(db):
    r=start(db); a=args(); a['obligations'][0]['deadline']={'kind':'relative','raw_text':'after termination','anchor_event':'termination','offset_days':30}
    result=record_obligations(db,r,a,{},.5); assert 'E3_CONDITIONAL_OR_AMBIGUOUS' in result['escalation_codes']
    row=db.execute('select raw_text,resolved_date from obligation_deadlines').fetchone(); assert row[0]=='after termination' and row[1] is None
