#!/usr/bin/env python3
"""Commit only a digest of the local-only synthetic test inputs before code freeze."""
import hashlib,json,sqlite3,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def _canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    suffix = path.suffix.lower()
    # JSON and txt: normalize line endings (CRLF -> LF) for cross-platform reproducibility
    if suffix in (".json", ".txt"):
        # Normalize CRLF and lone CR to LF
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if suffix == ".sqlite":
        # Hash logical DB content, not raw file bytes (page layout varies)
        db = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        h = hashlib.sha256()
        # Hash tables in deterministic order, rows ordered by rowid
        tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        for table in tables:
            h.update(table.encode("utf-8"))
            h.update(b"\x1e")
            # Get column names for deterministic ordering
            cols = [r[1] for r in db.execute(f'PRAGMA table_info("{table}")')]
            # Order by rowid for reproducibility; fallback to all cols
            try:
                rows = list(db.execute(f'SELECT * FROM "{table}" ORDER BY rowid'))
            except sqlite3.OperationalError:
                rows = list(db.execute(f'SELECT * FROM "{table}" ORDER BY "{cols[0]}"'))
            for row in rows:
                for val in row:
                    if val is None:
                        h.update(b"\x00")
                    elif isinstance(val, bytes):
                        h.update(val)
                    else:
                        # Canonical text for numbers/strings
                        h.update(str(val).encode("utf-8"))
                    h.update(b"\x1f")
                h.update(b"\n")
            h.update(b"\x1e")
        db.close()
        # Return digest bytes as canonical representation
        return h.digest()
    # .npy and others: raw bytes (vectors.npy is deterministic across runs per report)
    return raw

def digest(root):
    root=Path(root);folder=root/'corpus/synthetic_test';docs=folder/'documents';index=folder/'index'
    required=[root/'db/test_docs.sqlite',folder/'manifest.json',index/'manifest.json',index/'chunks.json',index/'vectors.npy']
    if not docs.is_dir() or any(not p.is_file() or p.is_symlink() for p in required): raise ValueError('local test synthetic database, manifest, documents and lean shard required')
    files=required+sorted(docs.rglob('*.txt'))
    if len(files)==len(required) or any(p.is_symlink() for p in files): raise ValueError('test synthetic documents missing or symlinked')
    h=hashlib.sha256()
    for path in sorted(files,key=lambda p:str(p.relative_to(root))):
        name=path.relative_to(root).as_posix().encode();data=_canonical_bytes(path)
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
