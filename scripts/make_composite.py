#!/usr/bin/env python3
"""Join two source contracts for human conflict review; does not label conflicts."""
import argparse,hashlib,json,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def create(root,source_ids):
    if len(source_ids)!=2 or len(set(source_ids))!=2: raise ValueError('exactly two distinct source documents required')
    log=root/'eval_results/test_run_log.jsonl'
    if log.exists() and any(json.loads(x).get('valid') is True for x in log.read_text().splitlines() if x.strip()): raise ValueError('composite creation forbidden after frozen test results')
    db=sqlite3.connect(root/'db/b2.sqlite');db.row_factory=sqlite3.Row;db.execute('PRAGMA foreign_keys=ON')
    texts=[]
    for sid in source_ids:
        if not db.execute('SELECT 1 FROM corpus_documents WHERE id=?',(sid,)).fetchone(): raise ValueError('source document not found')
        texts.append((root/'corpus/documents'/f'{sid}.txt').read_text(encoding='utf-8'))
    separator='\n\n--- DOCUMENT BOUNDARY ---\n\n'; text=separator.join(texts);did='composite_'+hashlib.sha256(json.dumps({'sources':source_ids,'text_hash':hashlib.sha256(text.encode()).hexdigest()},sort_keys=True).encode()).hexdigest()[:20]
    mfile=root/'corpus/adversarial/manifest.json';mfile.parent.mkdir(parents=True,exist_ok=True);manifest=json.loads(mfile.read_text()) if mfile.exists() else {}
    meta={'document_id':did,'mechanism':'composite','source_document_ids':source_ids,'char_count':len(text),'separator':separator}
    path=root/'corpus/documents'/f'{did}.txt'
    if did in manifest:
        if manifest[did]!=meta or not path.exists() or path.read_bytes()!=text.encode(): raise ValueError('inconsistent existing composite')
        db.close();return did
    if path.exists(): raise ValueError('document exists without provenance')
    with db:
        db.execute("INSERT INTO corpus_documents(id,title,contract_family,char_count,license) VALUES(?,?,'SYNTHETIC_COMPOSITE',?,'CC BY 4.0')",(did,'Composite source documents',len(text)))
        for i,sid in enumerate(source_ids):
            shift=0 if i==0 else len(texts[0])+len(separator)
            for r in db.execute('SELECT category,answer_text,char_start,char_end FROM clause_labels WHERE document_id=? ORDER BY category,char_start,char_end',(sid,)).fetchall():
                db.execute('INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES(?,?,?,?,?)',(did,r['category'],r['answer_text'],r['char_start']+shift,r['char_end']+shift))
        path.write_bytes(text.encode());manifest[did]=meta
        try: tmp=mfile.with_suffix('.tmp');tmp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');tmp.replace(mfile)
        except Exception: path.unlink(missing_ok=True);raise
    db.close();return did
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',nargs=2);a=p.parse_args()
    try: print(create(ROOT,a.source))
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
