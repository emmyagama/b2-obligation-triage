"""B1-style local Chroma store, opened from an ephemeral copy during replay."""
import hashlib,json,os,shutil,tempfile
from pathlib import Path
os.environ.setdefault('ANONYMIZED_TELEMETRY','false')

def client(path):
    import chromadb
    from chromadb.config import Settings
    return chromadb.PersistentClient(path=str(path),settings=Settings(anonymized_telemetry=False))

def canonical_chunks(chunks):
    return json.dumps(chunks,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def digest(chunks): return hashlib.sha256(canonical_chunks(chunks)).hexdigest()

def _read(path):
    c=client(path)
    try:
        coll=c.get_collection(name='b2_contracts',embedding_function=None);rows=[];offset=0
        while True:
            page=coll.get(limit=1000,offset=offset,include=['documents','embeddings','metadatas']); ids=page['ids']
            if not ids: break
            for i,cid in enumerate(ids):
                m=page['metadatas'][i];v=page['embeddings'][i]
                rows.append({'chunk_id':cid,'document_id':m['document_id'],'clause_category':m['clause_category'] or None,'section_hint':m['section_hint'],'char_start':m['char_start'],'char_end':m['char_end'],'text':page['documents'][i],'embedding':[float(x) for x in v]})
            offset+=len(ids)
        return sorted(rows,key=lambda x:x['chunk_id'])
    finally: c.close()

def load(path):
    # Chroma modifies its SQLite/HNSW files even on reads. Copy first, so offline
    # replay cannot modify the committed/frozen vector store or invalidate tags.
    with tempfile.TemporaryDirectory(prefix='b2-chroma-read-') as td:
        snapshot=Path(td)/'store';shutil.copytree(path,snapshot)
        return _read(snapshot)

def build(path,chunks):
    path=Path(path);path.mkdir(parents=True,exist_ok=True);c=client(path)
    try:
        try: c.delete_collection('b2_contracts')
        except Exception as e:
            if e.__class__.__name__ not in ('NotFoundError','InvalidCollectionException'): raise
        coll=c.create_collection(name='b2_contracts',metadata={'hnsw:space':'l2'},embedding_function=None)
        for i in range(0,len(chunks),500):
            b=chunks[i:i+500]
            coll.add(ids=[x['chunk_id'] for x in b],embeddings=[x['embedding'] for x in b],documents=[x['text'] for x in b],metadatas=[{'document_id':x['document_id'],'clause_category':x['clause_category'] or '', 'section_hint':x['section_hint'],'char_start':x['char_start'],'char_end':x['char_end']} for x in b])
    finally: c.close()
    stored=load(path)
    if len(stored)!=len(chunks): raise ValueError('Chroma stored chunk count mismatch')
    return stored
