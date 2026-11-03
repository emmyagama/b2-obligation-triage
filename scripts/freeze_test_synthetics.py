#!/usr/bin/env python3
"""Commit only a digest of the local-only synthetic test inputs before code freeze.

Cross-platform canonical digest: normalizes line endings, hashes SQLite
logically (ordered by content, not rowid/page layout), and excludes
hardware-dependent vectors.npy (float16 BLAS variance) from the seal.
"""
import hashlib,json,sqlite3,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def _canonical_json_bytes(path: Path) -> bytes:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Exclude hardware-dependent vectors_sha256 from index manifests
    if isinstance(data, dict) and "vectors_sha256" in data:
        data = {k: v for k, v in data.items() if k != "vectors_sha256"}
    # Canonical JSON: sorted keys, ensure_ascii False, separators, LF
    # Use indent 2 to match existing manifests but normalize fully via dump
    return json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"

def _canonical_bytes(path: Path) -> bytes:
    suffix = path.suffix.lower()
    name = path.name
    # JSON: canonical dump (normalizes CRLF, ordering, excludes vectors_sha256)
    if suffix == ".json":
        try:
            return _canonical_json_bytes(path)
        except Exception:
            # fallback: just normalize line endings
            raw = path.read_bytes()
            return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if suffix == ".txt":
        raw = path.read_bytes()
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if suffix == ".sqlite":
        db = sqlite3.connect(f"file:{path.resolve().as_posix()}?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        h = hashlib.sha256()
        tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        for table in tables:
            h.update(table.encode("utf-8"))
            h.update(b"\x1e")
            # Deterministic ordering by logical keys, not rowid (insert order)
            if table == "corpus_documents":
                order = 'ORDER BY id'
            elif table == "clause_labels":
                order = 'ORDER BY document_id, category, char_start, char_end'
            else:
                # Generic: order by all columns
                cols = [r[1] for r in db.execute(f'PRAGMA table_info("{table}")')]
                if cols:
                    order = 'ORDER BY "' + '", "'.join(cols) + '"'
                else:
                    order = 'ORDER BY rowid'
            for row in db.execute(f'SELECT * FROM "{table}" {order}'):
                for val in row:
                    if val is None:
                        h.update(b"\x00")
                    elif isinstance(val, bytes):
                        h.update(val)
                    else:
                        h.update(str(val).encode("utf-8"))
                    h.update(b"\x1f")
                h.update(b"\n")
            h.update(b"\x1e")
        db.close()
        return h.digest()
    # .npy: skip hardware-dependent raw vectors - return empty to exclude,
    # but keep file in list for existence check (hash excludes content)
    if suffix == ".npy":
        # Hash model/chunking identity instead of raw vectors: use chunks count
        # For backwards compatibility, return empty bytes - file checked but not hashed
        return b""
    return path.read_bytes()

def digest(root):
    root=Path(root);folder=root/'corpus/synthetic_test';docs=folder/'documents';index=folder/'index'
    required=[root/'db/test_docs.sqlite',folder/'manifest.json',index/'manifest.json',index/'chunks.json',index/'vectors.npy']
    if not docs.is_dir() or any(not p.is_file() or p.is_symlink() for p in required): raise ValueError('local test synthetic database, manifest, documents and lean shard required')
    files=required+sorted(docs.rglob('*.txt'))
    if len(files)==len(required) or any(p.is_symlink() for p in files): raise ValueError('test synthetic documents missing or symlinked')
    h=hashlib.sha256()
    for path in sorted(files,key=lambda p:str(p.relative_to(root))):
        name=path.relative_to(root).as_posix().encode()
        # vectors.npy exists check but content excluded for portability
        data=_canonical_bytes(path)
        # For .npy, we still frame name but with empty data (seals existence, not bytes)
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
