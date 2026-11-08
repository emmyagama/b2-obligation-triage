"""Safe budget-boundary tests for b2cli (provider mocked at the HTTP seam).

These invert the independent synthetic reproducer, which asserted the old
unsafe behaviour (HTTP request sent before the cap was checked). Here every
attempt must be refused before the real transport call, retries must be
counted, unknown usage must stay unknown, and the offline path must never
touch the network.
"""
import json
import os
import sys
import threading
from pathlib import Path

import pytest
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from b2cli import runner as cli_runner  # noqa: E402
from b2cli.__main__ import main  # noqa: E402
from agent.retry import retry  # noqa: E402

CONTRACT = """\
1. Licence. Provider grants Customer a non-exclusive licence to use the \
fictional software described in this synthetic document for evaluation.
"""
LICENCE_QUOTE = ("Provider grants Customer a non-exclusive licence to use the "
                 "fictional software described in this synthetic document")
PRICING = {'input_per_million_usd': 0.30, 'cached_input_per_million_usd': 0.03,
           'output_per_million_usd': 2.50}


def response(message, usage={'prompt_tokens': 10, 'completion_tokens': 5}):
    payload = {'choices': [{'message': message}]}
    if usage is not None:
        payload['usage'] = usage
    return payload


class FakeHTTP:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def terminal_message():
    args = {'obligations': [{
        'type': 'LIC-GRANT', 'description': 'Synthetic obligation.',
        'owed_by': 'provider', 'clause_category': 'Grant',
        'clause_quote': LICENCE_QUOTE, 'consequence': None,
        'confidence': 0.9, 'deadline': {'kind': 'none', 'raw_text': None}}],
        'confidence': 0.9, 'escalate': False, 'escalation_codes': []}
    return {'role': 'assistant', 'content': None, 'tool_calls': [{
        'id': 'x', 'type': 'function',
        'function': {'name': 'record_obligations', 'arguments': json.dumps(args)}}]}


def argv(tmp_path, extra=()):
    contract = tmp_path / 'contract.txt'
    contract.write_text(CONTRACT, encoding='utf-8')
    return ['--contract', str(contract), '--party', 'customer', '--ref', 'BUDGET-1',
            '--db', str(tmp_path / 'db.sqlite'), '--cache-dir', str(tmp_path / 'cache'),
            '--out', str(tmp_path / 'out'), '--live', '--acknowledge-live',
            '--max-cost-usd', '0.5', *extra]


def live_env(monkeypatch):
    monkeypatch.delenv('B2_OFFLINE', raising=False)
    monkeypatch.setenv('GEMINI_API_KEY', 'synthetic-test-only')


def report(tmp_path):
    return json.loads((tmp_path / 'out' / 'report.json').read_text(encoding='utf-8'))


def test_request_cap_blocks_attempt_before_real_transport(tmp_path, monkeypatch, capsys):
    live_env(monkeypatch)
    calls = []

    def fake_post(url, **kwargs):
        calls.append(kwargs.get('json'))
        return FakeHTTP(response({'role': 'assistant', 'content': 'still thinking'}))

    monkeypatch.setattr(requests, 'post', fake_post)
    rc = main(argv(tmp_path, extra=['--max-requests', '1']))
    assert rc == 4
    assert 'request cap reached (1)' in capsys.readouterr().err
    # The engine asked for a second turn; the gate refused before HTTP call 2.
    assert len(calls) == 1


def test_usd_cap_refuses_first_request_before_transport(tmp_path, monkeypatch, capsys):
    live_env(monkeypatch)
    calls = []
    monkeypatch.setattr(requests, 'post', lambda *a, **k: calls.append(1))
    rc = main(argv(tmp_path, extra=['--max-cost-usd', '0.000001']))
    assert rc == 4
    assert 'spend cap would be exceeded' in capsys.readouterr().err
    assert calls == []


def test_retries_are_counted_and_capped_before_each_attempt():
    ledger = cli_runner.BudgetLedger(max_requests=2, pricing=PRICING)
    real_calls = []
    sent = {'n': 0}

    def real_post(url, **kwargs):
        real_calls.append(1)
        sent['n'] += 1
        if sent['n'] < 3:
            raise requests.ConnectionError('transient')
        return FakeHTTP(response(terminal_message()))

    transport = cli_runner._BudgetedTransport(real_post, ledger)
    with pytest.raises(cli_runner.BudgetExceeded):
        retry(lambda: transport('http://synthetic', json={'max_tokens': 100}),
              sleeper=lambda _s: None)
    assert len(real_calls) == 2          # cap refused attempt 3 before the real call
    assert ledger.attempts == 2


def test_unknown_usage_is_not_treated_as_free():
    ledger = cli_runner.BudgetLedger(max_usd=1.0, pricing=PRICING)
    ledger.reserve_attempt({'max_tokens': 100, 'messages': []})
    ledger.record_cost(None)
    assert ledger.attempts == 1
    assert ledger.known_cost_attempts == 0
    assert ledger.unknown_cost_attempts == 1
    assert ledger.reserved_usd > 0
    assert ledger.spent_usd == 0.0


def test_interrupted_request_keeps_reservation_and_unknown_count(monkeypatch):
    ledger = cli_runner.BudgetLedger(max_requests=5, pricing=PRICING)

    def interrupted(url, **kwargs):
        raise KeyboardInterrupt()

    transport = cli_runner._BudgetedTransport(interrupted, ledger)
    with pytest.raises(KeyboardInterrupt):
        transport('http://synthetic', json={'max_tokens': 10})
    assert ledger.attempts == 1
    assert ledger.unknown_cost_attempts == 1


def test_concurrent_reservations_cannot_exceed_request_cap():
    ledger = cli_runner.BudgetLedger(max_requests=1)
    outcomes = []
    barrier = threading.Barrier(2)

    def worker():
        barrier.wait()
        try:
            ledger.reserve_attempt({'max_tokens': 1})
            outcomes.append('allowed')
        except cli_runner.BudgetExceeded:
            outcomes.append('refused')

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(outcomes) == ['allowed', 'refused']
    assert ledger.attempts == 1


def test_missing_pricing_refuses_usd_cap(monkeypatch, tmp_path, capsys):
    live_env(monkeypatch)
    calls = []
    monkeypatch.setattr(requests, 'post', lambda *a, **k: calls.append(1))
    import agent.config
    original = agent.config.load
    monkeypatch.setattr(agent.config, 'load',
                        lambda name: {} if name == 'pricing.yaml' else original(name))
    rc = main(argv(tmp_path, extra=['--max-cost-usd', '1']))
    assert rc == 4
    assert 'verified pricing field' in capsys.readouterr().err
    assert calls == []


def test_unknown_usage_reported_without_invented_cost(tmp_path, monkeypatch, capsys):
    live_env(monkeypatch)
    monkeypatch.setattr(requests, 'post',
                        lambda url, **k: FakeHTTP(response(terminal_message(), usage=None)))
    rc = main(argv(tmp_path, extra=['--max-requests', '1']))
    assert rc == 0
    rep = report(tmp_path)
    assert rep['provider_calls'] == 1
    assert rep['cost_usd'] is None
    assert rep['budget']['known_cost_estimate_usd'] is None
    assert rep['budget']['unknown_cost_attempts'] == 1
    assert rep['budget']['enforcement'] == 'pre-transport-conservative-reservation'


def test_known_usage_estimate_and_tokens_are_reported(tmp_path, monkeypatch):
    live_env(monkeypatch)
    monkeypatch.setattr(requests, 'post',
                        lambda url, **k: FakeHTTP(response(terminal_message())))
    rc = main(argv(tmp_path, extra=['--max-requests', '1']))
    assert rc == 0
    rep = report(tmp_path)
    assert rep['provider_calls'] == 1
    assert rep['cost_usd'] is None
    assert rep['budget']['known_cost_attempts'] == 1
    assert rep['budget']['known_cost_estimate_usd'] > 0
    assert rep['budget']['unknown_cost_attempts'] == 0
    import sqlite3
    con = sqlite3.connect(tmp_path / 'db.sqlite')
    tokens = con.execute('SELECT tokens_in, tokens_out FROM runs').fetchone()
    con.close()
    assert tokens == (10, 5)


def test_offline_path_never_calls_transport(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv('B2_OFFLINE', '1')
    monkeypatch.setattr(requests, 'post',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('network call')))
    contract = tmp_path / 'contract.txt'
    contract.write_text(CONTRACT, encoding='utf-8')
    rc = main(['--contract', str(contract), '--party', 'customer', '--ref', 'OFF-1',
               '--db', str(tmp_path / 'db.sqlite'), '--cache-dir', str(tmp_path / 'cache'),
               '--out', str(tmp_path / 'out')])
    assert rc == 3
    assert 'cache miss' in capsys.readouterr().err


@pytest.mark.parametrize('bad', ['0', '-1', 'nan', 'inf'])
def test_invalid_usd_cap_rejected_by_argument_parser(bad):
    with pytest.raises(SystemExit) as exc:
        main(['--contract', 'x.txt', '--party', 'customer', '--ref', 'X',
              '--max-cost-usd', bad])
    assert exc.value.code == 2


@pytest.mark.parametrize('bad', ['0', '-2', '1.5'])
def test_invalid_request_cap_rejected_by_argument_parser(bad):
    with pytest.raises(SystemExit) as exc:
        main(['--contract', 'x.txt', '--party', 'customer', '--ref', 'X',
              '--max-requests', bad])
    assert exc.value.code == 2
