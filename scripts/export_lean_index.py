#!/usr/bin/env python3
"""One-time Chroma migration. Always checks every stored chunk against source slices."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.lean_index import save,sha
from agent.corpus_version import version
ROOT=Path(__file__).resolve().parents[1]

def compare_search(rows,vectors,dtype,queries=200,top_k=8):
    """Diagnostic only: compare old rounded L2 and new cosine on stored-vector self queries."""
    import numpy as np
    if queries<1 or top_k<1: raise ValueError('queries and top-k must be positive')
    matrix=np.asarray(vectors,dtype=np.float32);quant=matrix.astype(dtype).astype(np.float32)
    groups={}
    for i,r in enumerate(rows): groups.setdefault(r['doc_id'],[]).append(i)
    picks=np.linspace(0,len(rows)-1,min(queries,len(rows)),dtype=int)
    overlaps=[]
    for q in picks:
        ii=groups[rows[q]['doc_id']];v=matrix[q];orig=matrix[ii];recovered=quant[ii]
        distances=np.sum((orig-v)**2,axis=1);denom=np.linalg.norm(recovered,axis=1)*np.linalg.norm(v)
        scores=np.divide(recovered@v,denom,out=np.zeros(len(ii),dtype=np.float32),where=denom!=0)
        old=sorted(range(len(ii)),key=lambda j:(-round(float(1/(1+distances[j])),4),rows[ii[j]]['chunk_id']))[:top_k]
        new=sorted(range(len(ii)),key=lambda j:(-round(float(np.clip(scores[j],-1,1)),4),rows[ii[j]]['chunk_id']))[:top_k]
        overlaps.append(len(set(old)&set(new))/len(old))
    return {'query_kind':'stored-vector self queries; not human queries','queries':len(overlaps),'top_k':top_k,'mean_top_k_overlap':sum(overlaps)/len(overlaps),'minimum_top_k_overlap':min(overlaps)}

def export(root,source,expect_chunks=14903,dtype='float16',queries=200,top_k=8):
    # Chroma mutates on open; load() copies the store to a temporary directory first.
    from agent.chroma_store import load,digest as chroma_digest
    import yaml
    chunks=load(source)
    if expect_chunks is not None and len(chunks)!=expect_chunks: raise ValueError(f'expected {expect_chunks} Chroma chunks, got {len(chunks)}')
    docs={};rows=[];vectors=[]
    for c in chunks:
        did=c['document_id']
        if Path(did).name!=did: raise ValueError('unsafe document id')
        path=root/'corpus/documents'/f'{did}.txt'
        if did not in docs: docs[did]=(path.read_text(encoding='utf-8'),sha(path))
        text=docs[did][0];a,b=c['char_start'],c['char_end']
        if not 0<=a<b<=len(text) or text[a:b]!=c['text']: raise ValueError('Chroma chunk does not match its source document slice')
        rows.append({'chunk_id':c['chunk_id'],'doc_id':did,'char_start':a,'char_end':b,'clause_category':c['clause_category']})
        vectors.append(c['embedding'])
    if not chunks: raise ValueError('no chunks')
    cfg_path=root/'config/model.yaml';cfg=yaml.safe_load(cfg_path.read_text())
    folder=root/'corpus/embeddings';legacy=folder/'legacy_chroma_manifest.json'
    legacy_source=legacy if legacy.exists() else folder/'manifest.json'
    if not legacy_source.exists(): raise ValueError('legacy Chroma manifest required to verify model and content')
    legacy_bytes=legacy_source.read_bytes();previous=json.loads(legacy_bytes)
    if previous.get('store')!='chroma' or previous.get('model_id')!=cfg['embedding_model'] or previous.get('chunks')!=len(chunks) or previous.get('content_sha256')!=chroma_digest(chunks): raise ValueError('legacy Chroma manifest model or content mismatch')
    if not legacy.exists(): legacy.write_bytes(legacy_bytes)
    m=save(root/'corpus/embeddings',rows,vectors,cfg['embedding_model'],dtype,{k:v[1] for k,v in docs.items()})
    diagnostic=compare_search(rows,vectors,dtype,queries,top_k)
    folder=root/'corpus/embeddings'
    diagnostic['index_bytes']=sum((folder/f).stat().st_size for f in ('chunks.json','vectors.npy','manifest.json','legacy_chroma_manifest.json'))
    (folder/'migration_report.json').write_text(json.dumps(diagnostic,sort_keys=True,indent=2)+'\n')
    cfg['corpus_version']=version(root);cfg_path.write_text(yaml.safe_dump(cfg,sort_keys=False))
    import sqlite3
    db=sqlite3.connect(root/'db/b2.sqlite');all_ids={r[0] for r in db.execute('SELECT id FROM corpus_documents')};db.close()
    missing=sorted(all_ids-set(docs))
    return {'verified_chunks':len(rows),'dimensions':m['dimensions'],'corpus_version':cfg['corpus_version'],'unindexed_base_documents':len(missing),'diagnostic':diagnostic,'note':'Run build_embeddings.py --split dev to index any missing dev synthetics.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=ROOT/'corpus/embeddings/chroma');p.add_argument('--expect-chunks',type=int,default=14903);p.add_argument('--dtype',choices=['float16','float32'],default='float16');p.add_argument('--queries',type=int,default=200);p.add_argument('--top-k',type=int,default=8);a=p.parse_args()
    try: print(json.dumps(export(ROOT,a.source,a.expect_chunks,a.dtype,a.queries,a.top_k),sort_keys=True))
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
