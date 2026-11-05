#!/usr/bin/env python3
"""Rebuild a run's details.json from run.sqlite, cases, corpus and the LLM cache.

The run's own details.json is only opened by --diff, so the reconstruction stays
independent of the file it is checked against. --lean emits only the fields
calibrate_floors.py reads, wrapped with a reconstructed flag.
"""
import argparse, csv, hashlib, json, sqlite3, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.config import ROOT
from agent.evalio import jsonwrite
from agent.scoring import normal_ws, score
from agent.synthetic import document_path

E1_ARGS = {'obligations': [], 'confidence': 1.0, 'escalate': True,
           'escalation_codes': ['E1_NO_OBLIGATION']}
LEAN_FIELDS = ('case', 'retrieval_score', 'args', 'escalation_codes')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_cache(cache_dir):
    by_key = {}
    for fp in Path(cache_dir).glob('*.json'):
        entry = json.loads(fp.read_text(encoding='utf-8'))
        if (entry.get('request') or {}).get('kind') != 'llm':
            continue
        message = entry['response']['choices'][0]['message']
        key = (json.dumps(message, sort_keys=True, ensure_ascii=False),
               entry['metadata'].get('latency_ms'))
        by_key.setdefault(key, []).append(entry)
    return by_key


def open_db(run_dir):
    db = sqlite3.connect('file:' + str(run_dir / 'run.sqlite') + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    return db


def run_index(db):
    intake_to_run = {r['intake_id']: r['id'] for r in db.execute('SELECT id,intake_id FROM runs')}
    ref_to_intake = {r['external_ref']: r['id'] for r in db.execute('SELECT id,external_ref FROM intakes')}
    return ref_to_intake, intake_to_run


def lean_view(row):
    view = {'case': row['case'],
            'retrieval_score': row['result']['retrieval_score'],
            'escalation_codes': row['result']['decision']['escalation_codes']}
    if 'args' in row['result']:
        view['args'] = row['result']['args']
    return view


def rebuild(run_dir, cache_dir, drift_path, out_path, do_diff, lean):
    run_dir = Path(run_dir)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    meta = json.loads((run_dir / 'run_metadata.json').read_text(encoding='utf-8'))
    cases_path = ROOT / 'cases' / f"{meta['split']}.json"
    cases = json.loads(cases_path.read_text())
    if sha(cases_path) != meta['case_sha256']:
        raise SystemExit('case file digest does not match run_metadata.json')
    with (run_dir / 'cases.csv').open(newline='', encoding='utf-8') as f:
        csv_rows = {r['case_id']: r for r in csv.DictReader(f)}
    db = open_db(run_dir)
    ref_to_intake, intake_to_run = run_index(db)
    run_of = {}
    for case in cases:
        cid = str(case['id'])
        original = case.get('duplicate_of')
        ref = cid if original is None else str(original)
        run_of[cid] = intake_to_run[ref_to_intake['eval:' + ref]]
    cache = None if lean else load_cache(ROOT / cache_dir)
    drift_by_run = {}
    if drift_path and not lean:
        with Path(drift_path).open(newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                drift_by_run.setdefault(run_of[row['case_id']], []).append(
                    {'request_hash': row['request_hash'], 'case_id': row['case_id'],
                     'seq': int(row['seq'])})
    gaps = []
    records = []
    for case in cases:
        cid = str(case['id'])
        run_id = run_of[cid]
        run = db.execute('SELECT * FROM runs WHERE id=?', (run_id,)).fetchone()
        decision_row = db.execute(
            'SELECT * FROM decisions WHERE run_id=? ORDER BY id DESC LIMIT 1', (run_id,)).fetchone()
        codes = json.loads(decision_row['escalation_codes_json'])
        if run['status'] == 'failed':
            dead = db.execute(
                'SELECT error_class FROM dead_letter WHERE run_id=? ORDER BY id DESC LIMIT 1',
                (run_id,)).fetchone()
            decision = {'decision_id': decision_row['id'], 'escalated': True,
                        'escalation_codes': codes, 'error_class': dead['error_class']}
            args = None
        else:
            terminal = None
            for row in db.execute(
                    "SELECT args_json,result_json FROM tool_calls WHERE run_id=? "
                    "AND tool_name='record_obligations' AND error_class IS NULL ORDER BY seq",
                    (run_id,)):
                terminal = row
            decision = {'decision_id': decision_row['id'],
                        'escalated': bool(decision_row['escalated']),
                        'escalation_codes': codes}
            if terminal:
                decision = json.loads(terminal['result_json'])
                args = json.loads(terminal['args_json'])
            elif codes == E1_ARGS['escalation_codes']:
                args = dict(E1_ARGS)
            else:
                gaps.append((cid, 'args', 'no successful terminal call and not an E1 decision'))
                args = None
        precheck = db.execute(
            "SELECT result_json FROM tool_calls WHERE run_id=? AND tool_name='retrieval_precheck' "
            "ORDER BY seq LIMIT 1", (run_id,)).fetchone()
        retrieval_score = json.loads(precheck['result_json']).get('max_score')
        trace_error = db.execute(
            'SELECT error_class FROM tool_calls WHERE run_id=? AND error_class IS NOT NULL LIMIT 1',
            (run_id,)).fetchone()
        observed = decision.get('error_class') or (trace_error[0] if trace_error else None)
        if csv_rows[cid]['error_class'] != (observed or ''):
            gaps.append((cid, 'error_class',
                         f"cases.csv={csv_rows[cid]['error_class']!r} rebuilt={observed!r}"))
        if csv_rows[cid]['schema_valid'] != str(args is not None):
            gaps.append((cid, 'schema_valid',
                         f"cases.csv={csv_rows[cid]['schema_valid']} rebuilt={args is not None}"))
        result = {'decision': decision, 'retrieval_score': retrieval_score}
        if args is not None:
            result['args'] = args
        if lean:
            records.append({'case': case, 'result': result})
            continue
        metadata = []
        for row in db.execute(
                "SELECT seq,result_json,latency_ms FROM tool_calls WHERE run_id=? "
                "AND tool_name='llm_response' ORDER BY seq", (run_id,)):
            message = json.loads(row['result_json'])
            if 'role' not in message:
                continue
            key = (json.dumps(message, sort_keys=True, ensure_ascii=False), row['latency_ms'])
            entries = cache.get(key, [])
            if not entries:
                gaps.append((cid, 'metadata',
                             f"turn seq={row['seq']} latency={row['latency_ms']} missing from cache"))
                continue
            metadata.append(entries[0]['metadata'])
        result['metadata'] = metadata
        result['drift'] = drift_by_run.get(run_id, [])
        result['transaction_latency_ms'] = run['latency_ms']
        document = document_path(ROOT, case['document_id']).read_text(encoding='utf-8')
        obligations = db.execute(
            'SELECT o.*,d.deadline_kind,d.raw_text,d.resolved_date,d.anchor_event,d.offset_days,'
            'd.recurring_rule FROM obligations o JOIN obligation_deadlines d ON d.obligation_id=o.id '
            'WHERE o.decision_id=? ORDER BY o.id', (decision['decision_id'],)).fetchall()
        obs = [{'type': ob['obligation_type'], 'owed_by': ob['owed_by'],
                'clause_quote': ob['clause_quote'],
                'deadline': {'kind': ob['deadline_kind'], 'resolved_date': ob['resolved_date']}}
               for ob in obligations]
        output = {'schema_valid': 'args' in result, 'obligations': obs,
                  'escalated': decision['escalated'], 'escalation_codes': decision['escalation_codes']}
        checks, _matches = score(case, output, document, observed)
        ungrounded = [o['clause_quote'] for o in obs
                      if not normal_ws(o['clause_quote'])
                      or normal_ws(o['clause_quote']) not in normal_ws(document)]
        records.append({'case': case, 'output': output, 'checks': checks, 'result': result,
                        'run_id': run_id, 'ungrounded_quotes': ungrounded})
    db.close()
    payload = {'reconstructed': True, 'rows': records} if lean else records
    jsonwrite(out_path, payload)
    print('rebuilt %d cases -> %s (%d bytes%s)'
          % (len(records), out_path, Path(out_path).stat().st_size,
             ', lean' if lean else ''))
    for cid, field, detail in gaps:
        print('GAP %-7s %-16s %s' % (cid, field, detail))
    print('gaps: %d' % len(gaps))
    if not do_diff:
        return 0 if not gaps else 1
    real_path = run_dir / 'details.json'
    real = real_path.read_bytes()
    if not real:
        print('DIFF: real details.json is empty (%s)' % real_path)
        return 1
    real_obj = json.loads(real)
    if not lean:
        if real == Path(out_path).read_bytes():
            print('DIFF: byte-identical to %s' % real_path)
            return 0
        print('DIFF: MISMATCH against %s (%d vs %d bytes)'
              % (real_path, len(real), Path(out_path).stat().st_size))
        for i, (a, b) in enumerate(zip(real_obj, records)):
            if a == b:
                continue
            for key in sorted(set(a) | set(b)):
                if a.get(key) != b.get(key):
                    print('  case[%d] %s: %r != %r' % (i, key, a.get(key), b.get(key)))
        if len(real_obj) != len(records):
            print('  length differs: %d vs %d' % (len(real_obj), len(records)))
        return 1
    if len(real_obj) != len(records):
        print('DIFF: MISMATCH row count %d vs %d' % (len(real_obj), len(records)))
        return 1
    bad = 0
    for i, (real_row, new_row) in enumerate(zip(real_obj, records)):
        want = lean_view(real_row)
        got = lean_view(new_row)
        if want != got:
            bad += 1
            for key in sorted(set(want) | set(got)):
                if want.get(key) != got.get(key):
                    print('  case[%d] %s: %r != %r'
                          % (i, key, want.get(key), got.get(key)))
    if bad:
        print('DIFF: MISMATCH on lean fields for %d/%d rows vs %s'
              % (bad, len(records), real_path))
        return 1
    print('DIFF: lean fields identical for all %d rows vs %s' % (len(records), real_path))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--cache-dir', default='cache/scratch')
    ap.add_argument('--drift', default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--diff', action='store_true')
    ap.add_argument('--lean', action='store_true')
    a = ap.parse_args()
    out = a.out or (Path(a.run_dir) / 'details.reconstructed.json')
    raise SystemExit(rebuild(a.run_dir, a.cache_dir, a.drift, out, a.diff, a.lean))


if __name__ == '__main__':
    main()
