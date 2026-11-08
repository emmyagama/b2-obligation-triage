"""b2cli runner: local contract-triage pipeline over the frozen B2 engine.

Design notes (v0.1.0):
- Reuses the baseline engine, sqlite schema, tools, validation, escalation
  routing, cache and prompt unchanged.
- Works on *user-supplied* contract text that has NO CUAD clause labels. The
  category-filtered E1 precheck is therefore disabled for this path: absent
  labels are not treated as evidence that no obligation exists.
  Instead the model loop always runs, and E1 is applied afterwards if the
  model records zero obligations.
- Default mode is offline replay: a cache miss is a hard error and no socket
  is opened (B2_OFFLINE is set before the agent package is imported).
- Live mode requires an explicit acknowledgement flag and a real provider key.
- All state (sqlite DB, cache, reports) lives outside tracked baseline paths.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

VERSION = '0.1.0'

MAX_CONTRACT_BYTES = 2_000_000
EMBED_DIM = 384
CHUNK_MAX_CHARS = 700
CHUNK_OVERLAP = 100


class BudgetExceeded(Exception):
    """Raised before a provider call that would exceed the approved cap."""


class PathRefused(Exception):
    """Raised when a file argument points into a protected repository path."""


PROTECTED_ROOTS = ('agent', 'corpus', 'cases', 'config', 'guide', 'prompts',
                   'scripts', 'db', 'eval_results', 'reviews', 'tests',
                   'adapters', '.git', '.github')


def _refuse_protected(path, label, root):
    resolved = Path(path).resolve()
    for name in PROTECTED_ROOTS:
        protected = (Path(root) / name).resolve()
        if resolved == protected or protected in resolved.parents:
            raise PathRefused(
                f'{label} path must not live inside tracked baseline "{name}/": '
                f'{resolved}')
    if resolved == Path(root).resolve():
        raise PathRefused(f'{label} path must not be the repository root')


def sanitize_document_id(stem, digest):
    clean = re.sub(r'[^A-Za-z0-9._-]+', '-', stem).strip('.-') or 'contract'
    return f'user-{clean[:40]}-{digest[:8]}'


def chunk_text(text, max_chars=CHUNK_MAX_CHARS, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append({'chunk_id': f'chunk_{chunk_id:05d}',
                       'char_start': start, 'char_end': end,
                       'clause_category': None})
        chunk_id += 1
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def hash_embed_batch(texts, dim=EMBED_DIM):
    """Deterministic lexical hash embedder (fallback, clearly labelled)."""
    import numpy as np
    vectors = []
    for t in texts:
        values = []
        counter = 0
        while len(values) < dim:
            digest = hashlib.blake2b(f'{counter}:{t}'.encode('utf-8'), digest_size=64).digest()
            for i in range(0, len(digest), 2):
                values.append(int.from_bytes(digest[i:i + 2], 'little', signed=True) / 32768.0)
            counter += 1
        arr = np.array(values[:dim], dtype=np.float32)
        norm = float(np.linalg.norm(arr))
        vectors.append(arr / norm if norm else np.zeros(dim, dtype=np.float32))
    return np.array(vectors, dtype=np.float32)


class BudgetedCache:
    """Cache wrapper enforcing a hard spend/request cap for live smokeless runs."""
    def __init__(self, cache, max_usd=None, max_requests=None):
        self.cache = cache
        self.path = getattr(cache, 'path', None)
        self.max_usd = max_usd
        self.max_requests = max_requests
        self.spent_usd = 0.0
        self.requests = 0

    def get(self, request, case_id=None, seq=None):
        return self.cache.get(request, case_id, seq)

    def put(self, request, response, metadata):
        cost = metadata.get('cost_usd')
        projected = self.spent_usd + (cost or 0.0)
        if self.max_requests is not None and self.requests + 1 > self.max_requests:
            raise BudgetExceeded(
                f'request cap reached ({self.max_requests}); refusing further provider calls')
        if self.max_usd is not None and projected > self.max_usd:
            raise BudgetExceeded(
                f'spend cap would be exceeded (spent {self.spent_usd:.6f} + '
                f'{cost!r} > {self.max_usd} USD); refusing further provider calls')
        self.cache.put(request, response, metadata)
        self.spent_usd = projected
        self.requests += 1


def _load_env_file(path):
    """Load KEY=VALUE lines into the environment without echoing values."""
    loaded = []
    for line in Path(path).read_text(encoding='utf-8', errors='replace').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
            continue
        if value and key not in os.environ:
            os.environ[key] = value
            loaded.append(key)
    return loaded


def _build_embedder(model_cfg):
    """Return (embed_batch callable, embed_query callable, label)."""
    model_id = model_cfg.get('embedding_model', 'all-MiniLM-L6-v2')
    adapter_spec = model_cfg.get('embedding_adapter')
    if adapter_spec:
        try:
            import importlib
            module_name, func_name = adapter_spec.rsplit(':', 1)
            module = importlib.import_module(module_name)
            single = getattr(module, func_name)

            def batch(texts):
                return single(list(texts), model_id)

            # Probe once so a missing optional dependency falls back cleanly.
            probe, _ = batch(['embedder probe'])
            if len(probe) != 1:
                raise ValueError('embedder probe returned unexpected shape')

            def query(text, seq=None):
                vec, _ = single([text], model_id)
                return vec[0]
            return batch, query, f'{model_id} (B1 adapter)'
        except Exception:
            pass
    return (lambda texts: hash_embed_batch(texts),
            lambda text, seq=None: hash_embed_batch([text])[0],
            f'b2cli-hash-{EMBED_DIM}d (deterministic fallback; NOT MiniLM)')


class UserDocumentChunks:
    """In-memory chunk store with the LeanIndex.search interface."""

    def __init__(self, rows, vectors, doc_text, document_id):
        self.rows = rows
        self.vectors = vectors
        self.doc_text = doc_text
        self.document_id = document_id

    def search(self, query_vector, document_id, top_k=8):
        import numpy as np
        if document_id != self.document_id:
            return []
        if type(top_k) is not int or top_k < 1:
            raise ValueError('top_k must be positive')
        query = np.asarray(query_vector, dtype=np.float32)
        mat = self.vectors.astype(np.float32)
        if query.shape != (mat.shape[1],) or not np.isfinite(query).all():
            raise ValueError('embedding dimension mismatch or nonfinite query')
        denoms = np.linalg.norm(mat, axis=1) * np.linalg.norm(query)
        sims = np.divide(mat @ query, denoms,
                         out=np.zeros(len(mat), dtype=np.float32), where=denoms != 0)
        scored = [(i, round(float(np.clip(s, -1, 1)), 4)) for i, s in enumerate(sims)]
        ranked = sorted(scored, key=lambda x: (-x[1], self.rows[x[0]]['chunk_id']))[:top_k]
        out = []
        for i, score in ranked:
            r = self.rows[i]
            a, b = r['char_start'], r['char_end']
            out.append({'chunk_id': r['chunk_id'], 'document_id': document_id,
                        'clause_category': r['clause_category'],
                        'section_hint': 'unlabelled paragraph',
                        'char_start': a, 'char_end': b,
                        'text': self.doc_text[a:b], 'score': score})
        return out


def _read_contract(path):
    raw = Path(path).read_bytes()
    if len(raw) > MAX_CONTRACT_BYTES:
        raise ValueError(f'contract exceeds size limit ({len(raw)} > {MAX_CONTRACT_BYTES} bytes)')
    try:
        text = raw.decode('utf-8')
        encoding = 'utf-8'
    except UnicodeDecodeError:
        text = raw.decode('cp1252')
        encoding = 'cp1252 (fallback)'
    if not text.strip():
        raise ValueError('contract file is empty')
    return text, encoding, len(raw)


def run_cli(args):
    from agent.config import ROOT, load
    from agent.db import initialize, connect
    from agent.intake import begin
    from agent.engine import run_agent
    from agent.taxonomy import load_taxonomy
    from agent.cache import Cache
    from agent.evalio import jsonwrite

    root = Path(ROOT)

    if args.env_file:
        loaded = _load_env_file(args.env_file)
        if args.verbose:
            print(f'env file loaded keys: {", ".join(loaded) or "(none)"}')

    contract_path = Path(args.contract).resolve()
    if not contract_path.is_file():
        raise FileNotFoundError(f'contract file not found: {contract_path}')
    text, encoding, byte_count = _read_contract(contract_path)

    digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    document_id = sanitize_document_id(contract_path.stem, digest)

    db_path = Path(args.db).resolve()
    cache_path = Path(args.cache_dir).resolve()
    out_dir = Path(args.out).resolve()
    for p, label in ((db_path, 'db'), (cache_path, 'cache-dir'), (out_dir, 'out')):
        _refuse_protected(p, label, root)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    if db_path.exists():
        db = connect(db_path)
        # Basic schema sanity: the DB must already contain the taxonomy table.
        have = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='obligation_types'").fetchone()
        if not have:
            db.close()
            raise ValueError(f'existing db file lacks the B2 schema: {db_path}')
    else:
        db = initialize(db_path)

    model_cfg = load('model.yaml')
    thresholds = load('thresholds.yaml')
    descriptions = load('tool_descriptions.yaml')
    pricing = load('pricing.yaml')
    prompt = (root / 'prompts' / f"{model_cfg['prompt_version']}.md").read_text(encoding='utf-8')

    if args.live:
        from agent.llm import endpoint
        _url, key_env, _provider = endpoint(model_cfg['model'])
        if not os.environ.get(key_env):
            raise RuntimeError(f'{key_env} is required for live mode '
                               f'(set it in the environment or pass --env-file)')

    load_taxonomy(db, root / 'guide' / 'obligation_types.yaml')

    with db:
        db.execute(
            "INSERT OR REPLACE INTO corpus_documents(id, title, contract_family, char_count) VALUES(?,?,?,?)",
            (document_id, contract_path.name, 'USER_SUBMITTED', len(text)))

    raw_chunks = chunk_text(text)
    chunk_batch, embed_query, embedder_label = _build_embedder(model_cfg)
    embedded = chunk_batch([text[c['char_start']:c['char_end']] for c in raw_chunks])
    vectors = embedded[0] if isinstance(embedded, tuple) else embedded
    chunks_store = UserDocumentChunks(raw_chunks, vectors, text, document_id)

    versions = {'model': model_cfg['model'],
                'prompt_version': model_cfg['prompt_version'],
                'schema_version': model_cfg['schema_version'],
                'corpus_version': model_cfg['corpus_version']}

    run_id, hit = begin(db, args.ref, document_id, args.party, args.context, 'b2cli', versions)
    cache = BudgetedCache(Cache(cache_path), args.max_cost_usd, args.max_requests)

    decision = None
    if hit:
        print(f'duplicate intake: returning existing run {run_id} (no provider call)')
        row = db.execute('SELECT * FROM decisions WHERE run_id=?', (run_id,)).fetchone()
        if row:
            decision = {'decision_id': row['id'], 'escalated': bool(row['escalated']),
                        'escalation_codes': json.loads(row['escalation_codes_json'])}
    else:
        config = {**model_cfg,
                  'e1_floor': thresholds['e1']['value'],
                  'e5_floor': thresholds['e5']['value'],
                  'pricing': pricing}
        # Unlabelled document: the category-filtered E1 precheck would read
        # "no CUAD labels" as "no obligation" and never call the model.
        # Neutralise the precheck; E1 is applied after the model loop instead.
        result = run_agent(db, run_id, document_id, args.party, args.context,
                           text, chunks_store, embed_query, cache, config,
                           descriptions, prompt, live=args.live, resume=False,
                           case_id=args.ref, precomputed_scores=0.0)
        decision = result['decision']
        n_obs = db.execute('SELECT count(*) FROM obligations WHERE decision_id=?',
                           (decision['decision_id'],)).fetchone()[0]
        codes = decision.get('escalation_codes') or []
        # E1 means "the model completed and recorded no obligations". Engine
        # failures (E4/E6) and other escalations already carry their own route.
        if n_obs == 0 and not codes:
            from agent.escalation import QUEUES
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc).isoformat()
            with db:
                db.execute('INSERT INTO escalations(decision_id,reason_code,queue,created_at) VALUES(?,?,?,?)',
                           (decision['decision_id'], 'E1_NO_OBLIGATION',
                            QUEUES['E1_NO_OBLIGATION'], now))
                codes = list(codes) + ['E1_NO_OBLIGATION']
                db.execute('UPDATE decisions SET escalated=1, escalation_codes_json=? WHERE id=?',
                           (json.dumps(codes), decision['decision_id']))
                db.execute("UPDATE runs SET status='escalated' WHERE id=?", (run_id,))
            decision['escalated'] = True
            decision['escalation_codes'] = codes

    obrows = []
    if decision:
        obrows = db.execute(
            'SELECT o.*, d.deadline_kind, d.raw_text, d.resolved_date, d.anchor_event,'
            ' d.offset_days, d.recurring_rule FROM obligations o'
            ' JOIN obligation_deadlines d ON d.obligation_id=o.id'
            ' WHERE o.decision_id=? ORDER BY o.id',
            (decision['decision_id'],)).fetchall()
    obligations = []
    for row in obrows:
        obligations.append({
            'type': row['obligation_type'], 'owed_by': row['owed_by'],
            'description': row['description'], 'clause_category': row['clause_category'],
            'clause_quote': row['clause_quote'], 'consequence': row['consequence'],
            'confidence': row['confidence'], 'needs_human': bool(row['needs_human']),
            'deadline': {'kind': row['deadline_kind'], 'raw_text': row['raw_text'],
                         'resolved_date': row['resolved_date'],
                         'anchor_event': row['anchor_event'],
                         'offset_days': row['offset_days'],
                         'recurring_rule': row['recurring_rule']}})
    escalations = []
    if decision:
        escalations = [dict(r) for r in db.execute(
            'SELECT reason_code, queue, created_at FROM escalations WHERE decision_id=? ORDER BY id',
            (decision['decision_id'],)).fetchall()]
    run_row = db.execute('SELECT status, cost_usd, latency_ms FROM runs WHERE id=?', (run_id,)).fetchone()

    report = {
        'cli_version': VERSION,
        'run_id': run_id,
        'external_ref': args.ref,
        'document_id': document_id,
        'contract_file': contract_path.name,
        'contract_sha256': digest,
        'contract_bytes': byte_count,
        'contract_encoding': encoding,
        'intake_party': args.party,
        'business_context': args.context,
        'mode': 'live' if args.live else 'offline-replay',
        'model': model_cfg['model'],
        'prompt_version': model_cfg['prompt_version'],
        'embedder': embedder_label,
        'retrieval_note': ('user document has no CUAD clause labels; the category-filtered '
                           'E1 precheck is disabled for this path and E1 is applied after '
                           'the model loop when zero obligations are recorded'),
        'duplicate_intake': hit,
        'decision': decision,
        'obligations': obligations,
        'escalations': escalations,
        'run_status': run_row['status'] if run_row else None,
        'cost_usd': run_row['cost_usd'] if run_row else None,
        'requests': cache.requests,
        'provider_calls': cache.requests if args.live else 0,
        'warning': ('Not legal advice. The system extracts and routes obligations for human '
                    'review; humans decide escalated issues.'),
    }
    jsonwrite(out_dir / 'report.json', report)
    db.close()

    print(f'b2cli {VERSION} - {report["mode"]} - model={report["model"]} - embedder={embedder_label}')
    esc = decision['escalated'] if decision else None
    codes = (decision.get('escalation_codes') or '-') if decision else '-'
    print(f'run {run_id}: status={report["run_status"]} obligations={len(obligations)} '
          f'escalated={esc} codes={codes}')
    if args.live:
        print(f'provider requests={cache.requests} spent_usd={cache.spent_usd:.6f}')
    print(f'report: {out_dir / "report.json"}')
    return 0
