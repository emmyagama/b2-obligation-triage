#!/usr/bin/env python3
"""Commit only a digest of the local-only synthetic test inputs before code freeze."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(root):
    root=Path(root);folder=root/'corpus/synthetic_test';docs=folder/'documents';index=folder/'index'
    required=[root/'db/test_docs.sqlite',folder/'manifest.json',index/'manifest.json',index/'chunks.json',index/'vectors.npy']
    if not docs.is_dir() or any(not p.is_file() or p.is_symlink() for p in required): raise ValueError('local test synthetic database, manifest, documents and lean shard required')
    files=required+sorted(docs.rglob('*.txt'))
    if len(files)==len(required) or any(p.is_symlink() for p in files): raise ValueError('test synthetic documents missing or symlinked')
    h=hashlib.sha256()
    for path in sorted(files,key=lambda p:str(p.relative_to(root))):
        name=path.relative_to(root).as_posix().encode();data=path.read_bytes()
        h.update(len(name).to_bytes(8,'big'));h.update(name);h.update(len(data).to_bytes(8,'big'));h.update(data)
    return h.hexdigest()

def seal(root):
    if subprocess.run(['git','rev-parse','--verify','refs/tags/code-frozen'],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0: raise ValueError('synthetic commitment must be created before code-frozen')
    value=digest(root);target=Path(root)/'cases/FROZEN-SYNTHETIC.sha256'
    devlog=Path(root)/'eval_results/dev_run_log.jsonl'
    started=devlog.exists() and any(json.loads(line).get('status')=='started' for line in devlog.read_text().splitlines() if line.strip())
    if started and (not target.exists() or target.read_text().split()[0]!=value): raise ValueError('synthetic commitment cannot change after dev live runs begin')
    target.write_text(value+'  local-test-synthetic-shard\n');return value
if __name__=='__main__':
    try: print('synthetic commitment: '+seal(ROOT))
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
