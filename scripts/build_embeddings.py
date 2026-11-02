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

def build(root,provider,model_id,cache_dir=None,batch_provider=None,batch_size=32):
    from agent.embed import embed
    from agent.cache import Cache,CacheMiss
    if not model_id or provider is None: raise ValueError('embedding model and local adapter must be configured')
    db=sqlite3.connect(root/'db/b2.sqlite');db.row_factory=sqlite3.Row;cache=Cache(cache_dir or root/'cache/llm');chunks=[];dim=None
    for row in db.execute('SELECT id FROM corpus_documents ORDER BY id'):
        did=row['id'];text=(root/'corpus/documents'/f'{did}.txt').read_text(encoding='utf-8')
        labels=db.execute('SELECT category,answer_text,char_start,char_end FROM clause_labels WHERE document_id=? ORDER BY char_start,char_end,category',(did,)).fetchall()
        chunks.extend(chunk_document(did,text,labels))
    db.close()
    if not chunks: raise ValueError('no chunks generated')
    if batch_provider:
        # Cache each request separately, but batch only unique cache misses.
        missing=[]; seen=set()
        for c in chunks:
            text=c['text']; req={'kind':'embed','model_id':model_id,'text':text}
            try: cache.get(req)
            except CacheMiss:
                if text not in seen: seen.add(text);missing.append(text)
        for i in range(0,len(missing),batch_size):
            batch=missing[i:i+batch_size];vectors,meta=batch_provider(batch,model_id)
            if len(vectors)!=len(batch): raise ValueError('batch adapter returned wrong vector count')
            for text,vector in zip(batch,vectors):
                if not isinstance(vector,list) or not vector: raise ValueError('invalid embedding vector')
                entrymeta={'provider':'embedder','model':model_id,'created_at':datetime.now(timezone.utc).isoformat(),'latency_ms':0,'tokens_in':0,'tokens_out':0,'attempts':1,**meta}
                cache.put({'kind':'embed','model_id':model_id,'text':text},vector,entrymeta)
    for c in chunks:
        vector=embed(c['text'],model_id,cache,provider,live=True,resume=True)
        if dim is None: dim=len(vector)
        if len(vector)!=dim: raise ValueError('embedding dimensions differ')
        c['embedding']=vector
    folder=root/'corpus/embeddings';folder.mkdir(parents=True,exist_ok=True)
    from agent.chroma_store import build as build_chroma,digest
    stored=build_chroma(folder/'chroma',chunks)
    manifest={'store':'chroma','collection':'b2_contracts','distance':'l2','model_id':model_id,'dimensions':dim,'chunks':len(stored),'content_sha256':digest(stored)}
    tmp=folder/'manifest.json.tmp';tmp.write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n');tmp.replace(folder/'manifest.json')
    for obsolete in (folder/'chunks.json',folder/'chunks.json.gz'):
        if obsolete.exists(): obsolete.unlink()
    config_file=root/'config/model.yaml'
    if config_file.exists():
        import yaml
        from agent.corpus_version import version
        cfg=yaml.safe_load(config_file.read_text());cfg['corpus_version']=version(root)
        config_file.write_text(yaml.safe_dump(cfg,sort_keys=False))
    return len(chunks),dim
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--allow-network',action='store_true',help='explicitly permit adapter network access');a=p.parse_args()
    if not a.allow_network: os.environ['B2_OFFLINE']='1'
    sys.path.insert(0,str(ROOT));import agent
    try:
        from agent.config import load
        cfg=load('model.yaml');adapter=cfg.get('embedding_adapter')
        if not adapter: raise ValueError('embedding_adapter is not configured')
        module,name=adapter.rsplit(':',1);module=importlib.import_module(module);provider=getattr(module,name);batch_provider=getattr(module,'embed_batch',None)
        if batch_provider is None: print('warning: adapter has no embed_batch; using single-text encoding',file=sys.stderr)
        count,dim=build(ROOT,provider,cfg.get('embedding_model'),batch_provider=batch_provider);print(f'embedded {count} chunks, dimension {dim}')
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
