#!/usr/bin/env python3
import argparse,json,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATEGORIES=('agree','disagree','insufficient_information')
def agreement(db):
    rows=db.execute('SELECT escalation_id,reviewer_id,verdict FROM human_reviews ORDER BY escalation_id,reviewer_id').fetchall()
    ids=sorted({r[1] for r in rows})
    if len(ids)!=3: raise ValueError('exactly three distinct reviewers required')
    groups={}
    for eid,rid,verdict in rows:
        if verdict not in CATEGORIES: raise ValueError('invalid review verdict')
        groups.setdefault(eid,{})[rid]=verdict
    complete=[v for v in groups.values() if set(v)==set(ids)]
    if not complete: raise ValueError('no escalations have three verdicts')
    counts=[[list(group.values()).count(category) for category in CATEGORIES] for group in complete]
    n=len(counts);pbar=sum(sum(x*(x-1) for x in row)/6 for row in counts)/n
    props=[sum(row[j] for row in counts)/(3*n) for j in range(3)]; pe=sum(p*p for p in props)
    kappa=None if abs(1-pe)<1e-15 else (pbar-pe)/(1-pe)
    return {'reviewers':len(ids),'complete_escalations':n,'incomplete_escalations':len(groups)-n,'pairwise_percent_agreement':pbar*100,'unanimous_percent':sum(max(row)==3 for row in counts)/n*100,'fleiss_kappa':kappa,'kappa_note':'undefined (no variance)' if kappa is None else None}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path);p.add_argument('--out',type=Path);a=p.parse_args()
    try:
        from common import default_review_db
        db=sqlite3.connect(a.db or default_review_db());result=agreement(db);db.close();text=json.dumps(result,indent=2,sort_keys=True)+'\n'
        if a.out: a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(text)
        print(text,end='')
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
