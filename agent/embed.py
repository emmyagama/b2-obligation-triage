from datetime import datetime, timezone
from .cache import CacheMiss

def embed(text, model_id, cache, provider=None, *, live=False, resume=False, case_id=None, seq=None, on_drift=None):
    req={'kind':'embed','model_id':model_id,'text':text}; old=None
    try:
        old=cache.get(req,case_id,seq)
        if not live or resume: return old['response']
    except CacheMiss:
        if not live: raise
    if provider is None: raise RuntimeError('embedding provider is not configured')
    vector,meta=provider(text,model_id)
    if not isinstance(vector,list) or not vector: raise ValueError('invalid embedding vector')
    if old and old['response']!=vector and on_drift: on_drift(req)
    cache.put(req,vector,{'provider':'embedder','model':model_id,'created_at':datetime.now(timezone.utc).isoformat(), 'latency_ms':0,'tokens_in':0,'tokens_out':0,'attempts':1, **meta})
    return vector
