"""The dispatcher records a trace and terminates only on a valid terminal call."""
import json, time
from datetime import datetime, timezone
from .tools import record_obligations
from .escalation import QUEUES
from .cache import CacheMiss

def failure(db, run_id, code, error_class, detail, payload=None):
    now=datetime.now(timezone.utc).isoformat()
    with db:
        db.execute('INSERT INTO dead_letter(run_id,error_class,error_detail,payload_json,created_at) VALUES(?,?,?,?,?)',(run_id,error_class,str(detail),json.dumps(payload,sort_keys=True) if payload is not None else None,now))
        cur=db.execute('INSERT INTO decisions(run_id,escalated,escalation_codes_json) VALUES(?,1,?)',(run_id,json.dumps([code])))
        db.execute('INSERT INTO escalations(decision_id,reason_code,queue,created_at) VALUES(?,?,?,?)',(cur.lastrowid,code,QUEUES[code],now))
        db.execute("UPDATE runs SET status='failed',finished_at=? WHERE id=?",(now,run_id))
    return {'decision_id':cur.lastrowid,'escalated':True,'escalation_codes':[code], 'error_class':error_class}

def run_loop(db, run_id, next_call, tool_handlers, anchors, floor, max_turns=8):
    errors=0; history=[]
    for seq in range(1,max_turns+1):
        try: name,args=next_call(history)
        except CacheMiss: raise
        except Exception as e: return failure(db,run_id,'E6_TOOL_FAILURE',type(e).__name__,e)
        start=time.monotonic(); err=None; result=None
        try:
            if name=='record_obligations': result=record_obligations(db,run_id,args,anchors,floor)
            elif name in tool_handlers: result=tool_handlers[name](**args)
            else: raise ValueError('unknown tool')
        except Exception as e:
            err=type(e).__name__; result={'error':str(e)}
            if name=='record_obligations': errors+=1
        with db:
            db.execute('INSERT INTO tool_calls(run_id,seq,tool_name,args_json,result_json,latency_ms,error_class) VALUES(?,?,?,?,?,?,?)',(run_id,seq,name,json.dumps(args,sort_keys=True),json.dumps(result,sort_keys=True),round(1000*(time.monotonic()-start)),err))
        history.append({'name':name,'args':args,'result':result})
        if name=='record_obligations' and not err: return result
        if errors>=2: return failure(db,run_id,'E4_SCHEMA_FAIL','SCHEMA_FAIL',result)
    return failure(db,run_id,'E4_SCHEMA_FAIL','LOOP_EXHAUSTED','terminal call absent')
