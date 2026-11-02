import json,uuid
from agent import engine
from agent.cache import key_for
from agent.db import initialize
from agent.intake import begin

db=initialize(':memory:')
with db:
    db.execute("INSERT INTO corpus_documents(id,title) VALUES('x','fixture')")
    db.execute("INSERT INTO obligation_types(code,name,cuad_category,deadline_behaviour) VALUES('T','duty','category','none')")
model={'model':'mock','prompt_version':'system_v1','schema_version':'1','corpus_version':'fixture','e1_floor':0.,'e5_floor':.5,'temperature':0,'max_tokens':100}
r=begin(db,'fixture','x','customer',None,'eval',model)[0]
seen=[]
def complete(req,*args,**kw):
    seen.append(key_for(req))
    if len(seen)==1: name='get_document_dates'; values={'document_id':'x'}
    else: name='record_obligations'; values={'obligations':[],'confidence':.9,'escalate':False,'escalation_codes':[]}
    msg={'role':'assistant','content':None,'tool_calls':[{'id':uuid.uuid4().hex,'type':'function','function':{'name':name,'arguments':json.dumps(values)}}]}
    return {'response':{'choices':[{'message':msg}]},'metadata':{'latency_ms':0,'attempts':1}},True,False
engine.complete=complete
desc={x:x for x in ('search_corpus','get_clause','get_document_dates','record_obligations')}
chunks=[{'chunk_id':'1','document_id':'x','clause_category':'category','text':'fixture','embedding':[1.]}]
engine.run_agent(db,r,'x','customer',None,'fixture',chunks,lambda q,s:[1.],None,model,desc,'instructions')
print(json.dumps(seen))
