import json, math
from pathlib import Path
from datetime import datetime, timezone
from .validate import validate_terminal
from .deadlines import resolve
from .escalation import apply_floor, QUEUES

class ClauseNotFound(Exception): pass

def get_clause(db, document_id, category):
    rows=db.execute('SELECT answer_text,char_start,char_end FROM clause_labels WHERE document_id=? AND category=? ORDER BY char_start,char_end',(document_id,category)).fetchall()
    if not rows: raise ClauseNotFound(category)
    return [dict(x) for x in rows]

def search_corpus(chunks, query_vector, document_id, top_k=8):
    if top_k < 1: raise ValueError('top_k must be positive')
    def cosine(a,b):
        if len(a)!=len(b): raise ValueError('embedding dimension mismatch')
        # B1's Chroma collection uses squared L2; convert distance to a bounded similarity.
        return 1.0/(1.0+sum((i-j)**2 for i,j in zip(a,b)))
    rows=[]
    for c in chunks:
        if c['document_id']==document_id:
            rows.append({**{k:v for k,v in c.items() if k!='embedding'},'score':round(cosine(query_vector,c['embedding']),4)})
    return sorted(rows,key=lambda c:(-c['score'],str(c['chunk_id'])))[:top_k]

def get_document_dates(db, document_id):
    from .dateparse import explicit_dates
    out={}; found=False
    for field,category in [('effective_date','Effective Date'),('expiration_date','Expiration Date')]:
        rows=db.execute('SELECT answer_text FROM clause_labels WHERE document_id=? AND category=? ORDER BY char_start,char_end',(document_id,category)).fetchall()
        values=set()
        for row in rows: values.update(explicit_dates(row[0]))
        out[field]=next(iter(values)) if len(values)==1 else None
        found |= bool(out[field])
    out['source']='cuad_label' if found else 'absent'
    return out

def record_obligations(db, run_id, args, anchors, floor):
    types=[r[0] for r in db.execute('SELECT code FROM obligation_types ORDER BY code')]
    validate_terminal(args,types)
    prepared=[]; codes=list(args['escalation_codes'])
    for ob in args['obligations']:
        default_row=db.execute('SELECT escalates_by_default FROM obligation_types WHERE code=?',(ob['type'],)).fetchone()
        if default_row and default_row[0] and 'E2_CONFLICTING_CLAUSES' not in codes:
            codes.append('E3_CONDITIONAL_OR_AMBIGUOUS')
        d,unresolved=resolve(ob['deadline'],anchors)
        if unresolved or ob['owed_by']=='unclear': codes.append('E3_CONDITIONAL_OR_AMBIGUOUS')
        prepared.append((ob,d,unresolved))
    codes=apply_floor(args['confidence'],args['obligations'],codes,floor)
    now=datetime.now(timezone.utc).isoformat()
    # Caller must not have an open transaction. All decision children commit atomically.
    with db:
        cur=db.execute('INSERT INTO decisions(run_id,obligation_count,confidence,escalated,escalation_codes_json) VALUES(?,?,?,?,?)', (run_id,len(prepared),args['confidence'],bool(codes),json.dumps(codes)))
        did=cur.lastrowid
        for ob,d,unresolved in prepared:
            cur=db.execute('INSERT INTO obligations(decision_id,obligation_type,description,owed_by,clause_category,clause_quote,consequence,confidence,needs_human) VALUES(?,?,?,?,?,?,?,?,?)', (did,ob['type'],ob['description'],ob['owed_by'],ob['clause_category'],ob['clause_quote'],ob.get('consequence'),ob['confidence'],bool(codes) or unresolved))
            db.execute('INSERT INTO obligation_deadlines(obligation_id,deadline_kind,raw_text,resolved_date,anchor_event,offset_days,recurring_rule) VALUES(?,?,?,?,?,?,?)',(cur.lastrowid,d['kind'],d.get('raw_text'),d.get('resolved_date'),d.get('anchor_event'),d.get('offset_days'),d.get('recurring_rule')))
        for code in codes: db.execute('INSERT INTO escalations(decision_id,reason_code,queue,created_at) VALUES(?,?,?,?)',(did,code,QUEUES[code],now))
        db.execute('UPDATE runs SET status=?, finished_at=? WHERE id=?',('escalated' if codes else 'ok',now,run_id))
    return {'decision_id':did,'escalated':bool(codes),'escalation_codes':codes}
