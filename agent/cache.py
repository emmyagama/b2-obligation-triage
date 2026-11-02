import hashlib, json, os
from pathlib import Path

class CacheMiss(Exception):
    def __init__(self, key, case_id=None, seq=None):
        self.key, self.case_id, self.seq = key, case_id, seq
        super().__init__(f'CacheMiss({key}, case={case_id}, seq={seq}): code or prompt drift, or incomplete cache')

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)

def key_for(request):
    return hashlib.sha256(canonical(request).encode()).hexdigest()

class Cache:
    def __init__(self, path): self.path = Path(path)
    def get(self, request, case_id=None, seq=None):
        key = key_for(request); path = self.path / (key + '.json')
        if not path.exists(): raise CacheMiss(key, case_id, seq)
        entry = json.loads(path.read_text())
        if entry.get('request') != request: raise ValueError('cache entry request mismatch')
        return entry
    def put(self, request, response, metadata):
        self.path.mkdir(parents=True, exist_ok=True)
        p = self.path / (key_for(request) + '.json'); tmp = p.with_suffix('.tmp')
        tmp.write_text(canonical({'request': request, 'response': response, 'metadata': metadata})+'\n')
        os.replace(tmp, p)

def ensure_online():
    if os.environ.get('B2_OFFLINE') == '1': raise RuntimeError('B2_OFFLINE prohibits HTTP')
