import os, time
from datetime import datetime, timezone
from .cache import CacheMiss, ensure_online
from .retry import retry

def request_object(model, messages, tools, tool_choice, temperature, max_tokens, corpus_version):
    return dict(kind='llm', model=model, messages=messages, tools=tools, tool_choice=tool_choice, temperature=temperature, max_tokens=max_tokens, corpus_version=corpus_version)

def complete(request, cache, *, live=False, resume=False, case_id=None, seq=None, post=None, throttle=None, pricing=None):
    old=None
    try: old=cache.get(request, case_id, seq)
    except CacheMiss:
        if not live: raise
    if old and (not live or resume): return old, True, False
    ensure_online()
    import requests
    key=os.environ.get('GROQ_API_KEY')
    if not key: raise RuntimeError('GROQ_API_KEY is required for live mode')
    body={k:v for k,v in request.items() if k not in ('kind','corpus_version')}
    start=time.monotonic()
    def call():
        if throttle: throttle()
        response=(post or requests.post)('https://api.groq.com/openai/v1/chat/completions',headers={'Authorization':f'Bearer {key}'},json=body,timeout=60)
        response.raise_for_status()
        return response.json()
    def transient(e):
        if isinstance(e,requests.HTTPError): return e.response is not None and (e.response.status_code==429 or e.response.status_code>=500)
        return isinstance(e,requests.RequestException)
    data,retries=retry(call,retryable=transient)
    usage=data.get('usage',{})
    meta={'provider':'groq','model':request['model'],'created_at':datetime.now(timezone.utc).isoformat(),'latency_ms':round((time.monotonic()-start)*1000),'tokens_in':usage.get('prompt_tokens',0),'tokens_cached_in':(usage.get('prompt_tokens_details') or {}).get('cached_tokens',0),'tokens_out':usage.get('completion_tokens',0),'attempts':retries+1,'system_fingerprint':data.get('system_fingerprint')}
    if pricing and pricing.get('input_per_million_usd') is not None and pricing.get('output_per_million_usd') is not None:
        cached=meta['tokens_cached_in']
        if not 0<=cached<=meta['tokens_in']: raise ValueError('provider returned invalid cached token count')
        cached_price=pricing.get('cached_input_per_million_usd',pricing['input_per_million_usd'])
        meta['cost_usd']=((meta['tokens_in']-cached)*pricing['input_per_million_usd']+cached*cached_price+meta['tokens_out']*pricing['output_per_million_usd'])/1000000
    else: meta['cost_usd']=None
    cache.put(request,data,meta)
    return {'request':request,'response':data,'metadata':meta},False,bool(old and old['response']!=data)
