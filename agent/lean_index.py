"""Text-free, deterministic NumPy index. Contract text is read from the document store."""
import hashlib, json
from pathlib import Path
import numpy as np

FIELDS={'chunk_id','doc_id','char_start','char_end','clause_category'}

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save(folder, rows, vectors, model_id, dtype='float16', document_hashes=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if dtype not in ('float16','float32'): raise ValueError('dtype must be float16 or float32')
    if any(set(row)!=FIELDS for row in rows): raise ValueError('index must contain only the five permitted metadata fields')
    order=sorted(range(len(rows)),key=lambda i:rows[i]['chunk_id'])
    rows=[rows[i] for i in order]; vectors=np.asarray(vectors,dtype=np.float32)
    if vectors.ndim!=2 or len(vectors)!=len(rows) or not np.isfinite(vectors).all(): raise ValueError('invalid vector matrix')
    if len({r['chunk_id'] for r in rows})!=len(rows): raise ValueError('duplicate chunk IDs')
    vectors=vectors[order].astype(dtype)
    if not np.isfinite(vectors).all(): raise ValueError('vector precision overflow')
    cp=folder/'chunks.json.tmp';cp.write_text(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8');cp.replace(folder/'chunks.json')
    vp=folder/'vectors.npy.tmp'
    with vp.open('wb') as f: np.save(f,vectors,allow_pickle=False)
    vp.replace(folder/'vectors.npy')
    manifest={'format':'b2-lean-v1','model_id':model_id,'dimensions':vectors.shape[1],'chunks':len(rows),'dtype':dtype,'chunking':{'max_chars':700,'overlap':100},'chunks_sha256':sha(folder/'chunks.json'),'vectors_sha256':sha(folder/'vectors.npy'),'document_sha256':document_hashes or {}}
    mp=folder/'manifest.json.tmp';mp.write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n');mp.replace(folder/'manifest.json')
    return manifest

class LeanIndex:
    def __init__(self,folder,documents,model_id=None):
        self.folder=Path(folder);self.documents=Path(documents)
        m=json.loads((self.folder/'manifest.json').read_text());self.manifest=m
        if m.get('format')!='b2-lean-v1' or (model_id is not None and m.get('model_id')!=model_id): raise ValueError('unsupported lean index or model mismatch')
        if sha(self.folder/'chunks.json')!=m['chunks_sha256'] or sha(self.folder/'vectors.npy')!=m['vectors_sha256']: raise ValueError('lean index checksum mismatch')
        self.rows=json.loads((self.folder/'chunks.json').read_text(encoding='utf-8'))
        self.vectors=np.load(self.folder/'vectors.npy',allow_pickle=False)
        if self.vectors.ndim!=2 or self.vectors.shape!=(m['chunks'],m['dimensions']) or str(self.vectors.dtype)!=m['dtype'] or not np.isfinite(self.vectors).all(): raise ValueError('lean vector matrix mismatch')
        if len(self.rows)!=m['chunks'] or any(set(r)!=FIELDS for r in self.rows): raise ValueError('invalid text-free index')
        ids=[r['chunk_id'] for r in self.rows]
        if ids!=sorted(ids) or len(set(ids))!=len(ids): raise ValueError('chunk ids must be unique and sorted')
        self.by_doc={}
        for did,expected in m.get('document_sha256',{}).items():
            if not isinstance(did,str) or Path(did).name!=did or not did: raise ValueError('unsafe document id')
            if sha(self.documents/f'{did}.txt')!=expected: raise ValueError('indexed document content changed')
        for i,r in enumerate(self.rows):
            did=r['doc_id']
            if not isinstance(did,str) or Path(did).name!=did or not did or type(r['char_start']) is not int or type(r['char_end']) is not int or not 0<=r['char_start']<r['char_end']: raise ValueError('invalid chunk metadata')
            self.by_doc.setdefault(did,[]).append(i)
    def search(self,query,document_id,top_k=8):
        if type(top_k) is not int or top_k<1: raise ValueError('top_k must be positive')
        v=np.asarray(query,dtype=np.float32)
        if v.shape!=(self.vectors.shape[1],) or not np.isfinite(v).all(): raise ValueError('embedding dimension mismatch or nonfinite query')
        indices=self.by_doc.get(document_id,[])
        if not indices: return []
        text=(self.documents/f'{document_id}.txt').read_text(encoding='utf-8')
        mat=self.vectors[indices].astype(np.float32); denom=np.linalg.norm(mat,axis=1)*np.linalg.norm(v)
        sims=np.divide(mat@v,denom,out=np.zeros(len(indices),dtype=np.float32),where=denom!=0)
        scores=[round(float(np.clip(s,-1,1)),4) for s in sims]
        ranked=sorted(zip(indices,scores),key=lambda x:(-x[1],self.rows[x[0]]['chunk_id']))[:top_k]
        result=[]
        for i,score in ranked:
            r=self.rows[i];a,b=r['char_start'],r['char_end']
            if b>len(text): raise ValueError('chunk outside document')
            result.append({'chunk_id':r['chunk_id'],'document_id':document_id,'clause_category':r['clause_category'],'section_hint':r['clause_category'] or 'unlabelled paragraph','char_start':a,'char_end':b,'text':text[a:b],'score':score})
        return result

class Shards:
    def __init__(self,*shards):
        self.shards=shards
        seen=set()
        for s in shards:
            overlap=seen & set(s.by_doc)
            if overlap: raise ValueError('document appears in multiple index shards')
            seen.update(s.by_doc)
    def search(self,query,document_id,top_k=8):
        rows=[]
        for s in self.shards: rows.extend(s.search(query,document_id,top_k))
        return sorted(rows,key=lambda r:(-r['score'],r['chunk_id']))[:top_k]
