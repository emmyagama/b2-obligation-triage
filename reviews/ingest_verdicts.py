#!/usr/bin/env python3
"""Ingest real verdicts atomically; retain optional reviewer counts in note JSON."""
import argparse,csv,json,sqlite3,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VALID={'agree','disagree','insufficient_information'}
def ingest(db,files):
    records=[]
    for path in files:
        with open(path,newline='',encoding='utf-8-sig') as f:
            r=csv.DictReader(f)
            expected={'escalation_id','reviewer_id','reviewer_role','verdict','note','human_obligation_count'}
            if not expected<=set(r.fieldnames or []): raise ValueError('verdict CSV headers are missing')
            for x in r:
                verdict=x['verdict'].strip();rid=x['reviewer_id'].strip();role=x['reviewer_role'].strip();note=x['note'].strip()
                if verdict not in VALID or not rid or not role: raise ValueError('reviewer, role and valid verdict are required')
                if verdict=='disagree' and not note: raise ValueError('a disagreement requires a note')
                try: eid=int(x['escalation_id']); count=int(x['human_obligation_count']) if x['human_obligation_count'].strip() else None
                except ValueError: raise ValueError('escalation id and optional count must be integers')
                if count is not None and count<0: raise ValueError('human obligation count cannot be negative')
                if not db.execute('SELECT 1 FROM escalations WHERE id=?',(eid,)).fetchone(): raise ValueError('unknown escalation id')
                records.append((eid,rid,role,verdict,json.dumps({'note':note,'human_obligation_count':count},ensure_ascii=False,sort_keys=True),datetime.now(timezone.utc).isoformat()))
    if not records: raise ValueError('no verdict rows')
    with db:
        db.executemany('INSERT INTO human_reviews(escalation_id,reviewer_id,reviewer_role,verdict,note,reviewed_at) VALUES(?,?,?,?,?,?)',records)
        for eid in sorted({r[0] for r in records}):
            rows=db.execute('SELECT note FROM human_reviews WHERE escalation_id=?',(eid,)).fetchall()
            values=[]
            for row in rows:
                try: values.append(json.loads(row[0]).get('human_obligation_count'))
                except (ValueError,AttributeError,TypeError): values.append(None)
            # Do not invent a consensus if the three reviewers disagree or omit counts.
            consensus=values[0] if len(values)==3 and values[0] is not None and len(set(values))==1 else None
            db.execute('UPDATE escalations SET human_obligation_count=? WHERE id=?',(consensus,eid))
    return len(records)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('files',nargs='+',type=Path);p.add_argument('--db',type=Path);a=p.parse_args()
    try:
        from common import default_review_db
        db=sqlite3.connect(a.db or default_review_db());db.execute('PRAGMA foreign_keys=ON'); print(f'ingested {ingest(db,a.files)} verdicts');db.close()
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
