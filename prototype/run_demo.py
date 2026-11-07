#!/usr/bin/env python3
"""B2 prototype: offline synthetic demonstration of the baseline pipeline.

A deterministic end-to-end triage over FICTIONAL documents inside a
temporary workspace: lean index build, retrieval precheck, the baseline
tool-calling engine driven by a SCRIPTED response served from a local
demo cache (the real offline cache path -- a cache miss raises; no socket
is ever opened), jsonschema/grounding/deadline validation, sqlite
decisions, scoring against synthetic gold, and the baseline Wilson
metrics.

Honesty notes (also printed at runtime):
- no provider calls, no credentials, no network; B2_OFFLINE is enforced
  before the baseline package import so its socket-level guard is active;
- the model response is fabricated by this script (labelled
  scripted-offline-response) and pre-seeded into a demo cache;
- the embedder is a demo-local deterministic hash function, NOT the
  baseline MiniLM/Gemini embedder -- retrieval scores are illustrative;
- no held-out/test cases, no CUAD content, no private material;
- this is a functionality demonstration (n=3 synthetic cases), not an
  evaluation, and it makes no quality claim. Live evaluation remains
  disabled and unavailable.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import date, timedelta
from pathlib import Path

os.environ['B2_OFFLINE'] = '1'  # before agent import: socket guard active

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import numpy as np

from agent.cache import Cache
from agent.config import load as load_config
from agent.db import initialize
from agent.evalio import jsonwrite, summary
from agent.engine import initial_messages, run_agent
from agent.intake import begin
from agent.lean_index import LeanIndex, Shards, save as save_index
from agent.llm import request_object
from agent.metrics import aggregate
from agent.scoring import score
from agent.taxonomy import load_taxonomy
from agent.tool_schemas import schemas

DEMO_MODEL = 'scripted-offline-response'
EMBED_ID = 'b2-demo-local-hash-64d'
DIM = 64

MSA_HEADER = ('SYNTHETIC DEMONSTRATION DOCUMENT - fictional; not a real contract; '
              'contains no third-party content. Master Services Agreement between '
              'DemoCo Ltd (Supplier) and SampleCorp Inc (Customer).')
MSA_EFFECTIVE = 'The parties agree this Agreement is effective as of January 5, 2026.'
MSA_LICENSE = ('Supplier grants Customer a non-exclusive, non-transferable right to '
               'use the Documentation delivered under this Agreement.')
MSA_WARRANTY = ('Supplier warrants that the Services will perform materially free of '
                'defects for ninety (90) days from the Effective Date.')
MSA_NONCOMPETE = ('During the Term and for twelve (12) months after it ends, Consultant '
                  'will not provide services that directly compete with the Customer Offering.')

DPA_HEADER = ('SYNTHETIC DEMONSTRATION DOCUMENT - fictional; not a real contract; '
              'contains no third-party content. Data Processing Addendum between '
              'DemoCo Ltd (Supplier) and SampleCorp Inc (Customer).')
DPA_IP = ('All Deliverables created under the Statement of Work are assigned to Customer '
          'upon creation, and Supplier must complete final deliverables by 2026-03-01.')
DPA_TRANSFER = ("Customer may not transfer this Agreement to an affiliate without "
                "Supplier's prior written consent.")

SECTIONS = {
    'toy-msa': [(None, MSA_HEADER), (None, MSA_EFFECTIVE), ('License Grant', MSA_LICENSE),
                ('Warranty Duration', MSA_WARRANTY), ('Non-Compete', MSA_NONCOMPETE)],
    'toy-dpa': [(None, DPA_HEADER), ('Ip Ownership Assignment', DPA_IP),
                ('Non-Transferable License', DPA_TRANSFER)],
}

EFFECTIVE_ANCHOR_DATE = date(2026, 1, 5)
WARRANTY_RESOLVED = (EFFECTIVE_ANCHOR_DATE + timedelta(days=90)).isoformat()
EFFECTIVE_LABEL_TEXT = 'January 5, 2026'


def deadline_none():
    return {'kind': 'none', 'raw_text': None, 'resolved_date': None,
            'anchor_event': None, 'offset_days': None, 'recurring_rule': None}


def deadline_relative(raw_text, anchor_event, offset_days):
    return {'kind': 'relative', 'raw_text': raw_text, 'resolved_date': None,
            'anchor_event': anchor_event, 'offset_days': offset_days, 'recurring_rule': None}


def deadline_absolute(raw_text, resolved_date):
    return {'kind': 'absolute', 'raw_text': raw_text, 'resolved_date': resolved_date,
            'anchor_event': None, 'offset_days': None, 'recurring_rule': None}


def obligation(kind_type, description, owed_by, category, quote, consequence, deadline, confidence):
    return {'type': kind_type, 'description': description, 'owed_by': owed_by,
            'clause_category': category, 'clause_quote': quote, 'consequence': consequence,
            'deadline': deadline, 'confidence': confidence}


def gold_obligation(kind_type, owed_by, category, quote, deadline, confidence):
    return {'type': kind_type, 'description': 'see clause_quote', 'owed_by': owed_by,
            'clause_category': category, 'clause_quote': quote,
            'deadline': {'kind': deadline['kind'], 'resolved_date': deadline['resolved_date']},
            'confidence': confidence}


CASE_SPECS = [
    {
        'id': 'demo-001', 'document_id': 'toy-msa', 'intake_party': 'customer',
        'business_context': 'Routine post-signature obligation triage of a fictional services agreement.',
        'class': 'clear', 'gold_should_escalate': False, 'gold_escalation_codes': [],
        'gold': [
            gold_obligation('LIC-GRANT', 'provider', 'License Grant', MSA_LICENSE,
                            deadline_none(), 0.93),
            gold_obligation('WAR-DURATION', 'provider', 'Warranty Duration', MSA_WARRANTY,
                            {'kind': 'relative', 'resolved_date': WARRANTY_RESOLVED}, 0.90),
        ],
        'scripted': {
            'obligations': [
                obligation('LIC-GRANT', 'Non-exclusive right to use the Documentation',
                           'provider', 'License Grant', MSA_LICENSE, None,
                           deadline_none(), 0.93),
                obligation('WAR-DURATION', 'Warranty of material defect-free performance',
                           'provider', 'Warranty Duration', MSA_WARRANTY,
                           'Re-performance at no additional charge',
                           deadline_relative('ninety (90) days from the Effective Date',
                                             'effective_date', 90), 0.90),
            ],
            'confidence': 0.92, 'escalate': False, 'escalation_codes': [],
        },
    },
    {
        'id': 'demo-002', 'document_id': 'toy-msa', 'intake_party': 'customer',
        'business_context': 'Low-confidence triage decision routed to human review.',
        'class': 'low-confidence-escalation', 'gold_should_escalate': True,
        'gold_escalation_codes': ['E5_LOW_CONFIDENCE'],
        'gold': [
            gold_obligation('COV-NON-COMPETE', 'provider', 'Non-Compete', MSA_NONCOMPETE,
                            deadline_none(), 0.50),
        ],
        'scripted': {
            'obligations': [
                obligation('COV-NON-COMPETE', 'Consultant non-compete during and after the term',
                           'provider', 'Non-Compete', MSA_NONCOMPETE, None,
                           deadline_none(), 0.50),
            ],
            'confidence': 0.50, 'escalate': False, 'escalation_codes': [],
        },
    },
    {
        'id': 'demo-003', 'document_id': 'toy-dpa', 'intake_party': 'provider',
        'business_context': 'Post-signature IP and assignment triage of a fictional addendum.',
        'class': 'clear', 'gold_should_escalate': False, 'gold_escalation_codes': [],
        'gold': [
            gold_obligation('IP-OWNERSHIP-ASSIGNMENT', 'provider', 'Ip Ownership Assignment',
                            DPA_IP, deadline_absolute('2026-03-01', '2026-03-01'), 0.94),
            gold_obligation('LIC-NO-TRANSFER', 'customer', 'Non-Transferable License',
                            DPA_TRANSFER, deadline_none(), 0.90),
        ],
        'scripted': {
            'obligations': [
                obligation('IP-OWNERSHIP-ASSIGNMENT', 'Deliverables assigned on creation',
                           'provider', 'Ip Ownership Assignment', DPA_IP, None,
                           deadline_absolute('2026-03-01', '2026-03-01'), 0.94),
                obligation('LIC-NO-TRANSFER', 'No affiliate transfer without consent',
                           'customer', 'Non-Transferable License', DPA_TRANSFER, None,
                           deadline_none(), 0.90),
            ],
            'confidence': 0.91, 'escalate': False, 'escalation_codes': [],
        },
    },
]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def embed_text(text):
    """Demo-local deterministic unit vector (non-negative, 64 dims).

    NOT the baseline embedder: illustrative retrieval only. Non-negative
    components keep every cosine in [0, 1], so the baseline retrieval
    floor cannot misfire for arithmetic reasons.
    """
    raw = hashlib.blake2b(text.encode('utf-8'), digest_size=DIM).digest()
    vec = np.frombuffer(raw, dtype=np.uint8).astype(np.float32) / 255.0
    norm = float(np.linalg.norm(vec))
    if norm == 0.0:
        vec = np.ones(DIM, dtype=np.float32)
        norm = float(np.linalg.norm(vec))
    return vec / norm


def embed_query(text, seq):  # engine calls embed_query(text, seq)
    return embed_text(text)


def render_document(docid):
    text = '\n\n'.join(part for _, part in SECTIONS[docid])
    spans = []
    offset = 0
    for category, part in SECTIONS[docid]:
        spans.append((category, offset, offset + len(part)))
        offset += len(part) + 2  # '\n\n' joiner
    return text, spans


def write_documents(ws):
    docs = {}
    folder = ws / 'corpus' / 'documents'
    folder.mkdir(parents=True, exist_ok=True)
    for docid in sorted(SECTIONS):
        text, spans = render_document(docid)
        data = text.encode('utf-8')
        (folder / f'{docid}.txt').write_bytes(data)
        docs[docid] = {'text': text, 'spans': spans, 'sha256': sha256_bytes(data)}
    return docs


def setup_db(ws, docs):
    (ws / 'db').mkdir(parents=True, exist_ok=True)
    db = initialize(ws / 'db' / 'b2.sqlite')
    load_taxonomy(db, REPO / 'guide' / 'obligation_types.yaml')
    for docid in sorted(docs):
        db.execute('INSERT INTO corpus_documents(id,title,contract_family,source_url,'
                   'char_count,page_count,license) VALUES(?,?,?,?,?,?,?)',
                   (docid, 'Synthetic demonstration document (fictional)', 'demonstration',
                    None, len(docs[docid]['text'].encode('utf-8')), 1,
                    'synthetic-fixture; no third-party content'))
    msa = docs['toy-msa']['text']
    start = msa.index(EFFECTIVE_LABEL_TEXT)
    db.execute('INSERT INTO clause_labels(document_id,category,answer_text,char_start,'
               'char_end) VALUES(?,?,?,?,?)',
               ('toy-msa', 'Effective Date', EFFECTIVE_LABEL_TEXT, start,
                start + len(EFFECTIVE_LABEL_TEXT)))
    db.commit()
    return db


def build_index(ws, docs, name_by_category):
    rows, vectors = [], []
    for docid in sorted(docs):
        for i, (category, start, end) in enumerate(docs[docid]['spans']):
            chunk_id = f'{docid}-{i:04d}'
            rows.append({'chunk_id': chunk_id, 'doc_id': docid, 'char_start': start,
                         'char_end': end, 'clause_category': category or ''})
            if category and category in name_by_category:
                vectors.append(embed_text(name_by_category[category]))
            else:
                vectors.append(embed_text('background:' + chunk_id))
    folder = ws / 'corpus' / 'embeddings'
    document_hashes = {docid: docs[docid]['sha256'] for docid in sorted(docs)}
    save_index(folder, rows, np.stack(vectors), EMBED_ID, dtype='float16',
               document_hashes=document_hashes)
    index = LeanIndex(folder, ws / 'corpus' / 'documents', EMBED_ID)
    return Shards(index)


def demo_config():
    model = load_config('model.yaml')
    floors = load_config('thresholds.yaml')
    pricing = {'model': DEMO_MODEL, 'input_per_million_usd': 0.0,
               'cached_input_per_million_usd': 0.0, 'output_per_million_usd': 0.0,
               'source': 'demo placeholder: no provider spend exists in this demo',
               'verified_on': 'not applicable'}
    if floors['e1']['value'] is None or floors['e5']['value'] is None:
        raise ValueError('baseline thresholds are not set')
    return {**model, 'model': DEMO_MODEL, 'e1_floor': floors['e1']['value'],
            'e5_floor': floors['e5']['value'], 'floors': floors, 'pricing': pricing}


def corpus_version(ws, docs):
    h = hashlib.sha256()
    for docid in sorted(docs):
        h.update(docid.encode('utf-8'))
        h.update(bytes.fromhex(docs[docid]['sha256']))
    h.update((ws / 'corpus' / 'embeddings' / 'manifest.json').read_bytes())
    return 'sha256:' + h.hexdigest()


def seed_scripted_response(cache, cfg, prompt, tooldefs, spec):
    messages = initial_messages(prompt, spec['intake_party'], spec['business_context'])
    request = request_object(cfg['model'], messages, tooldefs, 'auto',
                             cfg['temperature'], cfg['max_tokens'], cfg['corpus_version'])
    arguments = json.dumps(spec['scripted'], ensure_ascii=False, sort_keys=True,
                           separators=(',', ':'))
    response = {
        'choices': [{'index': 0, 'message': {
            'role': 'assistant', 'content': None,
            'tool_calls': [{'id': 'call_demo_1_1', 'type': 'function',
                            'function': {'name': 'record_obligations',
                                         'arguments': arguments}}]}}],
        'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
        'system_fingerprint': 'scripted-demo-response',
    }
    metadata = {'provider': 'scripted-demo', 'model': cfg['model'],
                'created_at': '1970-01-01T00:00:00+00:00', 'latency_ms': 0,
                'tokens_in': 0, 'tokens_cached_in': 0, 'tokens_out': 0, 'attempts': 1,
                'system_fingerprint': 'scripted-demo-response', 'cost_usd': 0.0}
    cache.put(request, response, metadata)


def git_sha():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO,
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return 'unversioned'


def run(workspace):
    ws = Path(workspace)
    ws.mkdir(parents=True, exist_ok=True)
    credentials = {'GROQ_API_KEY': bool(os.environ.get('GROQ_API_KEY')),
                   'GEMINI_API_KEY': bool(os.environ.get('GEMINI_API_KEY'))}
    print('B2 prototype: offline synthetic demonstration (no provider calls)')
    print('B2_OFFLINE=1 enforced; baseline socket-level guard active; live mode never used')
    print('credentials present: ' + ', '.join(f'{k}={"yes" if v else "no"}'
                                              for k, v in sorted(credentials.items()))
          + ' (unused by this demo)')

    docs = write_documents(ws)
    db = setup_db(ws, docs)
    types = [dict(r) for r in db.execute('SELECT * FROM obligation_types ORDER BY code')]
    if not types:
        raise ValueError('taxonomy did not load')
    name_by_category = {t['cuad_category']: t['name'] for t in types if t['cuad_category']}
    chunks = build_index(ws, docs, name_by_category)

    cfg = demo_config()
    cfg['corpus_version'] = corpus_version(ws, docs)
    prompt = (REPO / 'prompts' / f"{cfg['prompt_version']}.md").read_text(encoding='utf-8')
    descriptions = load_config('tool_descriptions.yaml')
    tooldefs = schemas([t['code'] for t in types], descriptions)
    versions = {'model': cfg['model'], 'prompt_version': cfg['prompt_version'],
                'schema_version': str(cfg['schema_version']),
                'corpus_version': cfg['corpus_version']}
    cache = Cache(ws / 'cache' / 'llm')

    records = []
    case_reports = []
    for spec in CASE_SPECS:
        cid = spec['id']
        docid = spec['document_id']
        document = (ws / 'corpus' / 'documents' / f'{docid}.txt').read_text(encoding='utf-8')
        seed_scripted_response(cache, cfg, prompt, tooldefs, spec)
        run_id, hit = begin(db, 'demo:' + cid, docid, spec['intake_party'],
                            spec['business_context'], 'demonstration', versions)
        if hit:
            raise ValueError('unexpected idempotent intake hit for ' + cid)
        started = time.monotonic()
        result = run_agent(db, run_id, docid, spec['intake_party'],
                           spec['business_context'], document, chunks, embed_query, cache,
                           cfg, descriptions, prompt, live=False, resume=False, case_id=cid)
        elapsed_ms = int(round((time.monotonic() - started) * 1000))
        decision = result['decision']
        obrows = db.execute(
            'SELECT o.*,d.deadline_kind,d.raw_text,d.resolved_date,d.anchor_event,'
            'd.offset_days,d.recurring_rule FROM obligations o '
            'JOIN obligation_deadlines d ON d.obligation_id=o.id '
            'WHERE o.decision_id=? ORDER BY o.id', (decision['decision_id'],)).fetchall()
        observed = [{'type': ob['obligation_type'], 'owed_by': ob['owed_by'],
                     'clause_quote': ob['clause_quote'],
                     'deadline': {'kind': ob['deadline_kind'],
                                  'resolved_date': ob['resolved_date']}} for ob in obrows]
        output = {'schema_valid': 'args' in result, 'obligations': observed,
                  'escalated': decision['escalated'],
                  'escalation_codes': decision['escalation_codes']}
        trace_error = db.execute('SELECT error_class FROM tool_calls WHERE run_id=? '
                                 'AND error_class IS NOT NULL LIMIT 1', (run_id,)).fetchone()
        case = {'id': cid, 'document_id': docid, 'class': spec['class'],
                'gold_obligations': spec['gold'],
                'gold_should_escalate': spec['gold_should_escalate'],
                'gold_escalation_codes': spec['gold_escalation_codes']}
        checks, matches = score(case, output, document,
                                decision.get('error_class')
                                or (trace_error[0] if trace_error else None))
        cost = (sum(m.get('cost_usd') for m in result['metadata'])
                if result['metadata'] and all(m.get('cost_usd') is not None
                                              for m in result['metadata']) else None)
        records.append({'case': case, 'output': output, 'document': document,
                        'checks': checks, 'matches': matches, 'latency_ms': elapsed_ms,
                        'cost_usd': cost, 'result': result, 'run_id': run_id,
                        'retrieval_score': result.get('retrieval_score')})
        case_reports.append({'id': cid, 'document_id': docid, 'class': spec['class'],
                             'gold_obligations': len(spec['gold']),
                             'matched': len(matches),
                             'escalated': bool(output['escalated']),
                             'escalation_codes': list(output['escalation_codes']),
                             'retrieval_score': result.get('retrieval_score'),
                             'latency_ms': elapsed_ms, 'cost_usd': cost,
                             'checks': checks})
        print(f'case {cid}: matched {len(matches)}/{len(spec["gold"])} obligations; '
              f'escalated={bool(output["escalated"])}; '
              f'codes={",".join(output["escalation_codes"]) or "-"}; '
              f'retrieval={result.get("retrieval_score")}; '
              f'exception={bool(checks["exception"])}')

    metrics = aggregate(records)
    metrics['split'] = 'demonstration'
    metrics['mode'] = 'offline-scripted'
    out_dir = ws / 'out'
    out_dir.mkdir(parents=True, exist_ok=True)
    jsonwrite(out_dir / 'metrics.json', metrics)
    (out_dir / 'summary.md').write_text(
        summary(metrics, 'B2 offline synthetic demonstration'), encoding='utf-8')
    exceptions = sum(1 for c in case_reports if c['checks']['exception'])
    report = {
        'mode': 'offline synthetic demonstration (no provider calls)',
        'provider_calls': 0,
        'model': cfg['model'],
        'prompt_version': cfg['prompt_version'],
        'schema_version': str(cfg['schema_version']),
        'corpus_version': cfg['corpus_version'],
        'embedding': ('demo-local deterministic hash vectors (b2-demo, 64d); '
                      'NOT the baseline embedder'),
        'baseline_git_sha': git_sha(),
        'floors': {'e1_value': cfg['e1_floor'], 'e1_provenance': cfg['floors']['e1']['provenance'],
                   'e5_value': cfg['e5_floor'], 'e5_provenance': cfg['floors']['e5']['provenance']},
        'credentials_present': credentials,
        'cache_entries': len(list((ws / 'cache' / 'llm').glob('*.json'))),
        'workspace': str(ws),
        'cases': case_reports,
        'metrics': metrics,
        'exceptions': exceptions,
    }
    jsonwrite(out_dir / 'report.json', report)
    print('summary:')
    print(summary(metrics, 'B2 offline synthetic demonstration'))
    print(f'report: {out_dir / "report.json"}')
    if exceptions:
        print(f'DEMO_FAILED cases={len(case_reports)} exceptions={exceptions}')
        return 1
    print(f'DEMO_OK cases={len(case_reports)} exceptions={exceptions} provider_calls=0')
    db.close()
    print(f'workspace: {ws}')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Offline synthetic demonstration of the B2 pipeline (no provider calls).')
    parser.add_argument('--workdir', default=None,
                        help='workspace directory (default: a fresh temp directory)')
    args = parser.parse_args(argv)
    workdir = args.workdir or tempfile.mkdtemp(prefix='b2_demo_')
    try:
        return run(workdir)
    except Exception:
        traceback.print_exc()
        print('DEMO_FAILED unhandled error', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
