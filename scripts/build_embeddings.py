#!/usr/bin/env python3
"""Build deterministic clause/paragraph chunks and locally cached embeddings."""
import argparse,hashlib,importlib,json,os,re,sqlite3,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def windows(start,end,max_chars=700,overlap=100):
    if max_chars<=0 or not 0<=overlap<max_chars: raise ValueError('invalid chunk sizing')
    pos=start
    while pos<end:
        stop=min(pos+max_chars,end);yield pos,stop
        if stop==end: break
        pos=stop-overlap

def chunk_document(did,text,labels,max_chars=700,overlap=100):
    specs=set(); intervals=[]
    for row in labels:
        cat,start,end=row['category'],row['char_start'],row['char_end']
        if not 0<=start<end<=len(text) or text[start:end]!=row['answer_text']: raise ValueError('label offset does not match document')
        intervals.append((start,end))
        for a,b in windows(start,end,max_chars,overlap):
            if text[a:b].strip(): specs.add((a,b,cat))
    merged=[]
    for a,b in sorted(intervals):
        if merged and a<=merged[-1][1]: merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else: merged.append((a,b))
    gaps=[];pos=0
    for a,b in merged:
        if pos<a: gaps.append((pos,a))
        pos=max(pos,b)
    if pos<len(text): gaps.append((pos,len(text)))
    for start,end in gaps:
        # Pack adjacent short paragraphs while respecting their boundaries.
        # Window an individually oversized paragraph with overlap.
        gap=text[start:end]; pending_start=None;pending_end=None
        for match in re.finditer(r'.*?(?:\n\s*\n|\Z)',gap,re.S):
            a=start+match.start();b=start+match.end()
            if a>=b: continue
            if b-a>max_chars:
                if pending_start is not None:
                    if text[pending_start:pending_end].strip(): specs.add((pending_start,pending_end,''))
                    pending_start=pending_end=None
                for x,y in windows(a,b,max_chars,overlap):
                    if text[x:y].strip(): specs.add((x,y,''))
            elif pending_start is None: pending_start,pending_end=a,b
            elif b-pending_start<=max_chars: pending_end=b
            else:
                if text[pending_start:pending_end].strip(): specs.add((pending_start,pending_end,''))
                pending_start,pending_end=a,b
        if pending_start is not None and text[pending_start:pending_end].strip(): specs.add((pending_start,pending_end,''))
    chunks=[]
    for start,end,cat in sorted(specs,key=lambda v:(v[0],v[1],v[2])):
        cid=hashlib.sha256(json.dumps([did,cat,start,end],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()[:24]
        chunks.append({'chunk_id':cid,'document_id':did,'clause_category':cat or None,'section_hint':cat or 'unlabelled paragraph','char_start':start,'char_end':end,'text':text[start:end]})
    return chunks

def build(root,provider,model_id,cache_dir=None,batch_provider=None,batch_size=32,split='dev',dtype='float16'):
    from agent.embed import embed
    from agent.cache import Cache,CacheMiss
    from agent.lean_index import LeanIndex,save,sha
    import numpy as np
    if split not in ('dev','test'): raise ValueError('split must be dev or test')
    if not model_id or provider is None: raise ValueError('embedding model and local adapter must be configured')
    test=split=='test'
    db=sqlite3.connect(root/('db/test_docs.sqlite' if test else 'db/b2.sqlite'));db.row_factory=sqlite3.Row
    docs=root/('corpus/synthetic_test/documents' if test else 'corpus/documents')
    folder=root/('corpus/synthetic_test/index' if test else 'corpus/embeddings')
    cache=Cache(cache_dir or root/('corpus/synthetic_test/embed_cache' if test else 'cache/llm'))
    chunks=[];hashes={}
    for row in db.execute('SELECT id FROM corpus_documents ORDER BY id'):
        did=row['id'];path=docs/f'{did}.txt';text=path.read_text(encoding='utf-8');hashes[did]=sha(path)
        labels=db.execute('SELECT category,answer_text,char_start,char_end FROM clause_labels WHERE document_id=? ORDER BY char_start,char_end,category',(did,)).fetchall()
        chunks.extend(chunk_document(did,text,labels))
    db.close()
    # Reuse vectors only for documents whose bytes are unchanged; new or modified
    # documents are encoded locally. Do not rebuild the original 14,903 vectors.
    old={}
    if (folder/'manifest.json').exists():
        manifest=json.loads((folder/'manifest.json').read_text())
        if manifest.get('format')=='b2-lean-v1' and manifest.get('model_id')==model_id:
            if manifest.get('dtype')!=dtype: raise ValueError('changing vector dtype requires a fresh export or rebuild')
            # Loading verifies old files, but document bytes may deliberately have
            # changed. Verify checksums directly and reuse unchanged documents only.
            if sha(folder/'vectors.npy')!=manifest['vectors_sha256'] or sha(folder/'chunks.json')!=manifest['chunks_sha256']: raise ValueError('existing lean index corrupted')
            rr=json.loads((folder/'chunks.json').read_text());vv=np.load(folder/'vectors.npy',allow_pickle=False)
            if len(rr)!=len(vv): raise ValueError('existing lean index length mismatch')
            for r,v in zip(rr,vv):
                if manifest.get('document_sha256',{}).get(r['doc_id'])==hashes.get(r['doc_id']): old[r['chunk_id']]=v.astype(np.float32).tolist()
    missing=[c for c in chunks if c['chunk_id'] not in old]
    if batch_provider:
        pending=[];seen=set()
        for c in missing:
            text=c['text'];req={'kind':'embed','model_id':model_id,'text':text}
            try: cache.get(req)
            except CacheMiss:
                if text not in seen: seen.add(text);pending.append(text)
        for i in range(0,len(pending),batch_size):
            batch=pending[i:i+batch_size];vectors,meta=batch_provider(batch,model_id)
            if len(vectors)!=len(batch): raise ValueError('batch adapter returned wrong vector count')
            for text,vector in zip(batch,vectors):
                if not isinstance(vector,list) or not vector: raise ValueError('invalid embedding vector')
                entrymeta={'provider':'embedder','model':model_id,'created_at':datetime.now(timezone.utc).isoformat(),'latency_ms':0,'tokens_in':0,'tokens_out':0,'attempts':1,**meta}
                cache.put({'kind':'embed','model_id':model_id,'text':text},vector,entrymeta)
    vectors=[];rows=[]
    for c in chunks:
        vector=old.get(c['chunk_id'])
        if vector is None: vector=embed(c['text'],model_id,cache,provider,live=True,resume=True)
        vectors.append(vector);rows.append({'chunk_id':c['chunk_id'],'doc_id':c['document_id'],'char_start':c['char_start'],'char_end':c['char_end'],'clause_category':c['clause_category']})
    if not vectors:
        config=root/'config/model.yaml'
        import yaml
        dimension=yaml.safe_load(config.read_text()).get('embedding_dimensions') if config.exists() else None
        if not dimension: raise ValueError('empty index requires configured embedding_dimensions')
        vectors=np.empty((0,dimension),dtype=np.float32)
    manifest=save(folder,rows,vectors,model_id,dtype,hashes)
    config_file=root/'config/model.yaml'
    if not test and config_file.exists():
        import yaml
        from agent.corpus_version import version
        cfg=yaml.safe_load(config_file.read_text());cfg['corpus_version']=version(root)
        config_file.write_text(yaml.safe_dump(cfg,sort_keys=False))
    return len(rows),manifest['dimensions']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--allow-network',action='store_true',help='explicitly permit adapter network access');p.add_argument('--split',choices=['dev','test'],default='dev');p.add_argument('--dtype',choices=['float16','float32'],default='float16');a=p.parse_args()
    if not a.allow_network: os.environ['B2_OFFLINE']='1'
    sys.path.insert(0,str(ROOT));import agent
    try:
        from agent.config import load
        cfg=load('model.yaml');adapter=cfg.get('embedding_adapter')
        if not adapter: raise ValueError('embedding_adapter is not configured')
        module,name=adapter.rsplit(':',1);module=importlib.import_module(module);provider=getattr(module,name);batch_provider=getattr(module,'embed_batch',None)
        count,dim=build(ROOT,provider,cfg.get('embedding_model'),batch_provider=batch_provider,split=a.split,dtype=a.dtype);print(f'embedded {count} chunks, dimension {dim}')
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
