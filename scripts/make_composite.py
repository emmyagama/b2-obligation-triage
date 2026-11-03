#!/usr/bin/env python3
"""Join two human-selected real documents; never decide conflict or gold."""
import argparse,hashlib,json,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from agent.synthetic import open_output

def create(root,source_ids,split='dev'):
    if len(source_ids)!=2 or len(set(source_ids))!=2: raise ValueError('exactly two distinct source documents required')
    log=root/'eval_results/test_run_log.jsonl'
    if log.exists() and any(json.loads(x).get('valid') is True for x in log.read_text().splitlines() if x.strip()): raise ValueError('composite creation forbidden after frozen test results')
    source=sqlite3.connect(root/'db/b2.sqlite');source.row_factory=sqlite3.Row
    texts=[];labels=[]
    try:
        for sid in source_ids:
            if not isinstance(sid,str) or not sid or Path(sid).name!=sid: raise ValueError('unsafe source id')
            doc=source.execute('SELECT contract_family FROM corpus_documents WHERE id=?',(sid,)).fetchone()
            if not doc or str(doc['contract_family'] or '').startswith('SYNTHETIC'): raise ValueError('sources must be distinct real base documents')
            text=(root/'corpus/documents'/f'{sid}.txt').read_text(encoding='utf-8');texts.append(text)
            rr=source.execute('SELECT category,answer_text,char_start,char_end FROM clause_labels WHERE document_id=? ORDER BY category,char_start,char_end',(sid,)).fetchall()
            if any(not 0<=r['char_start']<r['char_end']<=len(text) or text[r['char_start']:r['char_end']]!=r['answer_text'] for r in rr): raise ValueError('source label offset mismatch')
            labels.append(rr)
    finally: source.close()
    separator='\n\n--- DOCUMENT BOUNDARY ---\n\n';text=separator.join(texts)
    digest=lambda t:hashlib.sha256(t.encode('utf-8')).hexdigest()
    did='composite_'+hashlib.sha256(json.dumps({'sources':source_ids,'text_hash':digest(text)},sort_keys=True).encode()).hexdigest()[:20]
    shifts=[0,len(texts[0])+len(separator)]
    meta={'document_id':did,'mechanism':'composite','source_document_ids':source_ids,'char_count':len(text),'separator':separator,'text_sha256':digest(text),'sources':[{'document_id':sid,'sha256':digest(t),'char_start':shift,'char_end':shift+len(t)} for sid,t,shift in zip(source_ids,texts,shifts)]}
    db,folder,mfile=open_output(root,split);path=folder/f'{did}.txt';manifest=json.loads(mfile.read_text()) if mfile.exists() else {}
    try:
        if did in manifest:
            if manifest[did]!=meta or not path.exists() or path.read_bytes()!=text.encode() or not db.execute('SELECT 1 FROM corpus_documents WHERE id=?',(did,)).fetchone(): raise ValueError('inconsistent existing composite')
            return did
        if path.exists() or db.execute('SELECT 1 FROM corpus_documents WHERE id=?',(did,)).fetchone(): raise ValueError('document exists without matching provenance')
        with db:
            db.execute("INSERT INTO corpus_documents(id,title,contract_family,char_count,license) VALUES(?,?,'SYNTHETIC_COMPOSITE',?,'CC BY 4.0')",(did,'Composite source documents',len(text)))
            for shift,rr in zip(shifts,labels):
                for r in rr:
                    a,b=r['char_start']+shift,r['char_end']+shift
                    if text[a:b]!=r['answer_text']: raise ValueError('mapped composite offset mismatch')
                    db.execute('INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES(?,?,?,?,?)',(did,r['category'],r['answer_text'],a,b))
            path.write_bytes(text.encode());manifest[did]=meta
            try: tmp=mfile.with_suffix('.tmp');tmp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');tmp.replace(mfile)
            except Exception: path.unlink(missing_ok=True);raise
        return did
    finally: db.close()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['dev','test'],default='dev');p.add_argument('source',nargs=2);a=p.parse_args()
    try: print(create(ROOT,a.source,a.split))
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
