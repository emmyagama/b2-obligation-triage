"""CLI runner implementation for b2cli."""
import hashlib
import json
import os
from pathlib import Path
import numpy as np

from agent.config import load, ROOT
from agent.db import initialize, connect
from agent.intake import begin
from agent.engine import run_agent
from agent.taxonomy import load_taxonomy
from agent.cache import Cache
from agent.evalio import jsonwrite

def chunk_text(text, max_chars=700, overlap=100):
    chunks = []
    start = 0
    length = len(text)
    chunk_id = 0
    while start < length:
        end = min(start + max_chars, length)
        chunks.append({
            "chunk_id": f"chunk_{chunk_id:04d}",
            "char_start": start,
            "char_end": end,
            "clause_category": None,
        })
        chunk_id += 1
        if end == length:
            break
        start = end - overlap
    return chunks

def hash_embedder(texts, dim=384):
    """Deterministic local hash embedder fallback for unlabelled user documents."""
    vectors = []
    for t in texts:
        h = hashlib.blake2b(t.encode('utf-8'), digest_size=dim * 4).digest()
        arr = np.frombuffer(h, dtype=np.float32)
        # Normalize to unit vector
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        else:
            arr = np.zeros(dim, dtype=np.float32)
        vectors.append(arr)
    return np.array(vectors, dtype=np.float32)

def run_cli(args):
    contract_path = args.contract.resolve()
    if not contract_path.is_file():
        raise FileNotFoundError(f"Contract file not found: {contract_path}")

    # Read contract text
    try:
        text = contract_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        text = contract_path.read_text(encoding='cp1252')

    doc_id = contract_path.stem
    doc_sha = hashlib.sha256(text.encode('utf-8')).hexdigest()

    # Configure environment for offline if not live
    if not args.live:
        os.environ['B2_OFFLINE'] = '1'

    # Setup directories
    db_path = args.db.resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    out_dir = args.out.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = args.cache_dir.resolve()

    # Initialize DB
    db = initialize(db_path)

    # Load config and taxonomy
    model_cfg = load('model.yaml')
    thresholds = load('thresholds.yaml')
    descriptions = load('tool_descriptions.yaml')
    pricing = load('pricing.yaml')
    prompt = (ROOT / 'prompts' / f"{model_cfg['prompt_version']}.md").read_text(encoding='utf-8')

    load_taxonomy(db, ROOT / 'guide' / 'obligation_types.yaml')

    # Ensure corpus_documents row exists
    with db:
        db.execute(
            "INSERT OR REPLACE INTO corpus_documents(id, contract_family, text_length, content_sha256) VALUES(?, ?, ?, ?)",
            (doc_id, 'USER_SUBMITTED', len(text), doc_sha)
        )

    # Build chunks and embeddings
    raw_chunks = chunk_text(text)
    chunk_texts = [text[c['char_start']:c['char_end']] for c in raw_chunks]

    # Try B1 embedder if available, else fallback to hash embedder
    vectors = None
    embed_model_id = model_cfg.get('embedding_model', 'all-MiniLM-L6-v2')
    if model_cfg.get('embedding_adapter'):
        try:
            mod_name, func_name = model_cfg['embedding_adapter'].rsplit(':', 1)
            adapter = getattr(__import__(mod_name, fromlist=[func_name]), func_name)
            vectors, meta = adapter(chunk_texts, embed_model_id)
            vectors = np.array(vectors, dtype=np.float32)
        except Exception:
            pass

    if vectors is None:
        vectors = hash_embedder(chunk_texts, dim=384)

    # In-memory chunk search object matching Shards/LeanIndex expected interface
    class UserDocumentChunks:
        def __init__(self, rows, vecs, doc_text):
            self.rows = rows
            self.vectors = vecs
            self.doc_text = doc_text
        def search(self, query_vector, document_id, top_k=8):
            if document_id != doc_id:
                return []
            query = np.asarray(query_vector, dtype=np.float32)
            mat = self.vectors.astype(np.float32)
            denoms = np.linalg.norm(mat, axis=1) * np.linalg.norm(query)
            sims = np.divide(mat @ query, denoms, out=np.zeros(len(mat), dtype=np.float32), where=denoms != 0)
            scores = [round(float(np.clip(s, -1, 1)), 4) for s in sims]
            ranked = sorted(zip(range(len(self.rows)), scores), key=lambda x: (-x[1], self.rows[x[0]]['chunk_id']))[:top_k]
            res = []
            for i, score in ranked:
                r = self.rows[i]
                a, b = r['char_start'], r['char_end']
                res.append({
                    'chunk_id': r['chunk_id'],
                    'document_id': doc_id,
                    'clause_category': r['clause_category'],
                    'section_hint': 'user document paragraph',
                    'char_start': a,
                    'char_end': b,
                    'text': self.doc_text[a:b],
                    'score': score
                })
            return res

    chunks_store = UserDocumentChunks(raw_chunks, vectors, text)

    # Begin intake (idempotency check)
    versions = {
        'model': model_cfg['model'],
        'prompt_version': model_cfg['prompt_version'],
        'schema_version': model_cfg['schema_version'],
        'corpus_version': model_cfg['corpus_version']
    }

    run_id, hit = begin(db, args.ref, doc_id, args.party, args.context, 'b2cli', versions)
    if hit:
        print(f"Idempotent duplicate intake: returning existing run {run_id}")

    config = {
        **model_cfg,
        'e1_floor': thresholds['e1']['value'],
        'e5_floor': thresholds['e5']['value'],
        'pricing': pricing
    }

    cache = Cache(cache_dir)

    def embed_query_fn(query_text, seq):
        # Embed query using same method
        if model_cfg.get('embedding_adapter'):
            try:
                mod_name, func_name = model_cfg['embedding_adapter'].rsplit(':', 1)
                adapter = getattr(__import__(mod_name, fromlist=[func_name]), func_name)
                v, _ = adapter([query_text], embed_model_id)
                return v[0]
            except Exception:
                pass
        return hash_embedder([query_text], dim=384)[0]

    # Run agent if not hit
    if not hit:
        res = run_agent(
            db=db,
            run_id=run_id,
            document_id=doc_id,
            party=args.party,
            context=args.context,
            document=text,
            chunks=chunks_store,
            embed_query=embed_query_fn,
            llm_cache=cache,
            config=config,
            descriptions=descriptions,
            prompt=prompt,
            live=args.live,
            resume=False,
            case_id=args.ref
        )
        decision = res['decision']
    else:
        # Load existing decision from DB
        d_row = db.execute("SELECT * FROM decisions WHERE run_id=?", (run_id,)).fetchone()
        if d_row:
            decision = {'decision_id': d_row['id'], 'escalated': bool(d_row['escalated']), 'escalation_codes': json.loads(d_row['escalation_codes_json'])}
        else:
            decision = {'decision_id': None, 'escalated': False, 'escalation_codes': []}

    # Fetch recorded obligations and deadlines
    obrows = db.execute(
        "SELECT o.*, d.deadline_kind, d.raw_text, d.resolved_date, d.anchor_event, d.offset_days, d.recurring_rule "
        "FROM obligations o JOIN obligation_deadlines d ON d.obligation_id=o.id WHERE o.decision_id=? ORDER BY o.id",
        (decision.get('decision_id'),)
    ).fetchall()

    obligations = [dict(r) for r in obrows]
    esc_rows = db.execute("SELECT * FROM escalations WHERE decision_id=?", (decision.get('decision_id'),)).fetchall()
    escalations = [dict(r) for r in esc_rows]

    report = {
        "run_id": run_id,
        "external_ref": args.ref,
        "document_id": doc_id,
        "intake_party": args.party,
        "mode": "live" if args.live else "offline-replay",
        "decision": decision,
        "obligations": obligations,
        "escalations": escalations,
        "warning": "Disclaimer: This tool provides post-signature obligation extraction and routing. It does not render legal advice."
    }

    jsonwrite(out_dir / "report.json", report)
    db.close()

    print(f"B2 CLI: Run completed successfully. Run ID: {run_id}")
    print(f"Obligations extracted: {len(obligations)}")
    print(f"Escalated: {decision.get('escalated')} ({decision.get('escalation_codes')})")
    print(f"Report written to: {out_dir / 'report.json'}")
    return 0
