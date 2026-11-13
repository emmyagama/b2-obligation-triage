"""End-to-end and orchestration tests for b2cli (offline; provider call seam mocked).

These tests exercise the real engine + sqlite schema + validation + escalation
routing, replacing only agent.engine.complete (the single provider boundary).
"""
import json
import os
import sys
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from b2cli import runner as cli_runner  # noqa: E402
from b2cli.__main__ import build_parser, main  # noqa: E402
from agent.cache import CacheMiss  # noqa: E402
from agent.retry import retry  # noqa: E402

CONTRACT = """\
1. Effective Date. This fictional pilot agreement takes effect on 2026-03-01 and \
expires on 2027-02-28 for evaluation purposes only.
2. Licence. Provider grants Customer a non-exclusive licence to use the fictional \
software described in this synthetic document.
3. Access. Customer must provide Provider with audit access within 30 days after signature.
4. Notice. Customer may terminate on 60 days written notice.
"""
ABSOLUTE_QUOTE = "This fictional pilot agreement takes effect on 2026-03-01"
LICENCE_QUOTE = "Provider grants Customer a non-exclusive licence to use the fictional software described in this synthetic document"
RELATIVE_QUOTE = "Customer must provide Provider with audit access within 30 days after signature"
NOTICE_QUOTE = "Customer may terminate on 60 days written notice"


class FakeProvider:
    """Stand-in for agent.engine.complete; scripts one message per turn."""

    def __init__(self, messages):
        self.messages = list(messages)
        self.requests = []

    def __call__(self, request, cache, **kwargs):
        self.requests.append(request)
        if not self.messages:
            raise AssertionError('provider call beyond scripted turns')
        item = self.messages.pop(0)
        if isinstance(item, Exception):
            raise item
        message = item if 'tool_calls' in item else {'role': 'assistant',
                                                     'content': None, 'tool_calls': [item]}
        entry = {'response': {'choices': [{'message': message}]},
                 'metadata': {'latency_ms': 1, 'attempts': 1, 'cost_usd': 0.0,
                              'tokens_in': 0, 'tokens_out': 0}}
        return entry, False, False


def call(name, args):
    return {'id': 'provider_generated', 'type': 'function',
            'function': {'name': name, 'arguments': json.dumps(args)}}


def terminal(obligations, confidence=0.9, escalate=False, codes=None):
    return call('record_obligations', {'obligations': obligations, 'confidence': confidence,
                                       'escalate': escalate, 'escalation_codes': codes or []})


def obligation(quote=LICENCE_QUOTE, otype='LIC-GRANT', owed_by='provider',
               category='Grant', confidence=0.9, deadline=None, consequence=None):
    return {'type': otype, 'description': 'Synthetic obligation for testing.',
            'owed_by': owed_by, 'clause_category': category, 'clause_quote': quote,
            'consequence': consequence, 'confidence': confidence,
            'deadline': deadline or {'kind': 'none', 'raw_text': None}}


def run(tmp_path, monkeypatch, provider=None, extra=None, live=False, ack=False,
        contract_text=CONTRACT, ref='ACME-2026-01', party='customer'):
    if provider is not None:
        import agent.engine
        monkeypatch.setattr(agent.engine, 'complete', provider)
    contract = tmp_path / 'contract.txt'
    contract.write_text(contract_text, encoding='utf-8')
    argv = ['--contract', str(contract), '--party', party, '--ref', ref,
            '--db', str(tmp_path / 'db.sqlite'),
            '--cache-dir', str(tmp_path / 'cache'),
            '--out', str(tmp_path / 'out')] + (extra or [])
    if live:
        argv.append('--live')
    if ack:
        argv.append('--acknowledge-live')
    return main(argv)


def report(tmp_path):
    return json.loads((tmp_path / 'out' / 'report.json').read_text(encoding='utf-8'))


def git_status():
    out = subprocess.run(['git', 'status', '--porcelain'], cwd=str(ROOT),
                         capture_output=True, text=True, check=True)
    return set(out.stdout.splitlines())


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(['--version'])
    assert exc.value.code == 0
    assert 'b2cli 0.1.1' in capsys.readouterr().out


def test_runs_as_module_in_subprocess():
    env = dict(os.environ, PYTHONPATH=str(ROOT), B2_OFFLINE='1', PYTHONUTF8='1')
    out = subprocess.run([sys.executable, '-m', 'b2cli', '--version'], cwd=str(ROOT),
                         capture_output=True, text=True, env=env)
    assert out.returncode == 0
    assert 'b2cli 0.1.1' in out.stdout

def test_positional_arguments_required(capsys):
    assert main(['--contract', 'x.txt', '--party', 'customer']) == 2
    assert '--ref' in capsys.readouterr().err


def test_offline_empty_cache_exits_3_without_provider(tmp_path, monkeypatch, capsys):
    rc = run(tmp_path, monkeypatch, None)
    assert rc == 3
    assert 'cache miss' in capsys.readouterr().err
    cache_dir = tmp_path / 'cache'
    assert not cache_dir.exists() or not any(cache_dir.glob('*'))


def test_live_requires_acknowledgement(tmp_path, capsys):
    contract = tmp_path / 'c.txt'
    contract.write_text(CONTRACT, encoding='utf-8')
    rc = main(['--contract', str(contract), '--party', 'customer', '--ref', 'X-1',
               '--live', '--db', str(tmp_path / 'db.sqlite'),
               '--cache-dir', str(tmp_path / 'cache'), '--out', str(tmp_path / 'out')])
    assert rc == 1
    err = capsys.readouterr().err
    assert '--acknowledge-live' in err and 'transmits' in err


def test_live_with_ack_but_no_key_fails_before_network(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv('B2_OFFLINE', raising=False)
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    rc = run(tmp_path, monkeypatch, None, live=True, ack=True)
    assert rc == 1
    err = capsys.readouterr().err
    assert 'GEMINI_API_KEY' in err


def test_offline_success_pipeline(tmp_path, monkeypatch, capsys):
    provider = FakeProvider([terminal([obligation(
        deadline={'kind': 'absolute', 'raw_text': '2026-03-01', 'resolved_date': '2026-03-01'})])])
    before = git_status()
    rc = run(tmp_path, monkeypatch, provider)
    assert rc == 0
    rep = report(tmp_path)
    assert rep['mode'] == 'offline-replay'
    assert rep['provider_calls'] == 0
    assert rep['budget']['enforcement'] == 'offline-no-provider-calls'
    assert rep['budget']['attempts'] == 0
    assert rep['budget']['known_cost_estimate_usd'] is None
    assert rep['duplicate_intake'] is False
    assert rep['run_status'] == 'ok'
    assert len(rep['obligations']) == 1
    ob = rep['obligations'][0]
    assert ob['type'] == 'LIC-GRANT'
    assert ob['deadline']['kind'] == 'absolute'
    assert ob['deadline']['resolved_date'] == '2026-03-01'
    assert rep['decision']['escalated'] is False
    # The unlabelled document must reach the model: no CUAD labels => no E1 shortcut.
    assert len(provider.requests) == 1
    assert 'disabled for this path' in rep['retrieval_note']
    # User document was persisted with the real schema (title/char_count).
    import sqlite3
    con = sqlite3.connect(tmp_path / 'db.sqlite')
    row = con.execute('SELECT title, contract_family, char_count FROM corpus_documents').fetchone()
    con.close()
    assert row[0] == 'contract.txt' and row[1] == 'USER_SUBMITTED'
    assert row[2] == len((tmp_path / 'contract.txt').read_bytes().decode('utf-8'))
    # No repository paths were written.
    assert not (ROOT / 'b2cli_data').exists()
    assert git_status() == before


def test_zero_obligations_adds_e1_escalation(tmp_path, monkeypatch):
    provider = FakeProvider([terminal([])])
    assert run(tmp_path, monkeypatch, provider) == 0
    rep = report(tmp_path)
    assert rep['decision']['escalated'] is True
    assert 'E1_NO_OBLIGATION' in rep['decision']['escalation_codes']
    assert [(e['reason_code'], e['queue']) for e in rep['escalations']] == [('E1_NO_OBLIGATION', 'legal-ops')]
    assert rep['run_status'] == 'escalated'


def test_relative_deadline_without_anchor_and_low_confidence(tmp_path, monkeypatch):
    provider = FakeProvider([terminal([obligation(
        quote=RELATIVE_QUOTE, otype='CTL-AUDIT-RIGHT', confidence=0.5,
        deadline={'kind': 'relative', 'raw_text': '30 days after signature'})], confidence=0.5)])
    assert run(tmp_path, monkeypatch, provider) == 0
    rep = report(tmp_path)
    codes = rep['decision']['escalation_codes']
    assert 'E3_CONDITIONAL_OR_AMBIGUOUS' in codes and 'E5_LOW_CONFIDENCE' in codes
    assert rep['obligations'][0]['deadline']['resolved_date'] is None
    assert rep['obligations'][0]['needs_human'] is True
    assert {e['queue'] for e in rep['escalations']} == {'legal-ops'}


def test_model_conflict_escalation_needs_two_excerpts(tmp_path, monkeypatch):
    provider = FakeProvider([terminal([
        obligation(category='Cap On Liability', quote=LICENCE_QUOTE, otype='LIA-CAP'),
        obligation(category='Uncapped Liability', quote=NOTICE_QUOTE, otype='LIA-UNCAPPED'),
    ], escalate=True, codes=['E2_CONFLICTING_CLAUSES'])])
    assert run(tmp_path, monkeypatch, provider) == 0
    rep = report(tmp_path)
    assert 'E2_CONFLICTING_CLAUSES' in rep['decision']['escalation_codes']
    assert len(rep['obligations']) == 2


@pytest.mark.parametrize('bad', [
    obligation(quote='this sentence is not in the contract at all'),
    obligation(deadline={'kind': 'absolute', 'raw_text': '2026-03-01', 'resolved_date': '2026-04-01'}),
    obligation(otype='E1_NO_OBLIGATION'),
])
def test_invalid_terminal_twice_routes_e4(tmp_path, monkeypatch, bad):
    response = terminal([bad])
    provider = FakeProvider([response, response, response])
    assert run(tmp_path, monkeypatch, provider) == 0
    rep = report(tmp_path)
    assert rep['decision']['escalation_codes'] == ['E4_SCHEMA_FAIL']
    assert rep['run_status'] == 'failed'
    assert rep['escalations'][0]['queue'] == 'engineering'
    assert rep['obligations'] == []


def test_retryable_provider_error_routes_e6(tmp_path, monkeypatch):
    provider = FakeProvider([TimeoutError('provider stalled'), terminal([])])
    assert run(tmp_path, monkeypatch, provider) == 0
    rep = report(tmp_path)
    assert rep['decision']['escalation_codes'] == ['E6_TOOL_FAILURE']
    assert rep['escalations'][0]['queue'] == 'engineering'
    assert len(provider.requests) == 1


def test_idempotent_reference_makes_no_second_call(tmp_path, monkeypatch, capsys):
    provider = FakeProvider([terminal([obligation()])])
    assert run(tmp_path, monkeypatch, provider) == 0
    assert run(tmp_path, monkeypatch, provider) == 0
    rep = report(tmp_path)
    assert rep['duplicate_intake'] is True
    assert len(provider.requests) == 1
    assert 'duplicate intake' in capsys.readouterr().out
    import sqlite3
    con = sqlite3.connect(tmp_path / 'db.sqlite')
    assert con.execute('SELECT count(*) FROM runs').fetchone()[0] == 1
    assert con.execute('SELECT count(*) FROM obligations').fetchone()[0] == 1
    con.close()


def test_provider_requests_carry_no_gold_or_heldout_markers(tmp_path, monkeypatch):
    provider = FakeProvider([terminal([obligation()])])
    assert run(tmp_path, monkeypatch, provider) == 0
    payload = json.dumps(provider.requests[0]).lower()
    for marker in ('gold', 'heldout', 'held-out', 'cuad_'):
        assert marker not in payload
    assert 'expected' not in payload


def test_containment_refuses_tracked_paths(tmp_path, capsys):
    contract = tmp_path / 'c.txt'
    contract.write_text(CONTRACT, encoding='utf-8')
    for flag, bad in (('--db', ROOT / 'corpus' / 'x.sqlite'),
                      ('--cache-dir', ROOT / '.git' / 'cache'),
                      ('--out', ROOT / 'eval_results')):
        rc = main(['--contract', str(contract), '--party', 'customer', '--ref', 'X-2',
                   '--db', str(tmp_path / 'db.sqlite'),
                   '--cache-dir', str(tmp_path / 'cache'),
                   '--out', str(tmp_path / 'out'), flag, str(bad)])
        assert rc == 5, flag
    assert 'refused path' in capsys.readouterr().err


def test_contract_encoding_and_size_limits(tmp_path):
    latin = tmp_path / 'latin.txt'
    latin.write_bytes(b'Fictional clauses caf\xe9 only.')
    text, encoding, size = cli_runner._read_contract(latin)
    assert 'caf\xe9' in text
    assert encoding == 'cp1252 (fallback)'
    assert size == len(latin.read_bytes())
    empty = tmp_path / 'empty.txt'
    empty.write_bytes(b'   \n')
    with pytest.raises(ValueError):
        cli_runner._read_contract(empty)


def test_retry_helper_backoff_and_retry_count():
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError('429 transient')
        return 'ok'

    result, retries = retry(flaky, sleeper=lambda _s: None, jitter=lambda: 0.0)
    assert (result, retries, len(calls)) == ('ok', 2, 3)


class FakeCache:
    def __init__(self):
        self.puts = []

    def get(self, request, case_id=None, seq=None):
        raise CacheMiss('empty')

    def put(self, request, response, metadata):
        self.puts.append(metadata)


def test_cache_records_costs_without_being_the_gate():
    base = FakeCache()
    ledger = cli_runner.BudgetLedger(max_usd=1.0, max_requests=1)
    capped = cli_runner.BudgetedCache(base, ledger=ledger)
    # Cache writes only record observed usage; they are not the enforcement point.
    capped.put({'r': 1}, {'usage': {'prompt_tokens': 1, 'completion_tokens': 1}},
               {'cost_usd': 0.002})
    capped.put({'r': 2}, {'usage': None}, {'cost_usd': 0.0})
    assert ledger.attempts == 0
    assert ledger.known_cost_attempts == 1
    assert ledger.unknown_cost_attempts == 1
    assert abs(ledger.spent_usd - 0.002) < 1e-12


def test_transport_gate_refuses_before_http_call():
    ledger = cli_runner.BudgetLedger(max_requests=1)
    calls = []

    def real_post(url, **kwargs):
        calls.append(url)

    transport = cli_runner._BudgetedTransport(real_post, ledger)
    transport('http://first', json={'max_tokens': 10})
    with pytest.raises(cli_runner.BudgetExceeded):
        transport('http://second', json={'max_tokens': 10})
    assert calls == ['http://first']
