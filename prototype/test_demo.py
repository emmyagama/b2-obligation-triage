"""Minimal offline tests for the prototype demonstration.

No provider credentials, no network: GROQ/GEMINI keys are removed from the
child environment and B2_OFFLINE=1 is enforced (the demo sets it before
importing the baseline package, whose socket guard then rejects TCP).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / 'prototype' / 'run_demo.py'


def run_demo(workdir):
    env = dict(os.environ)
    env['B2_OFFLINE'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONUTF8'] = '1'
    env.pop('GROQ_API_KEY', None)
    env.pop('GEMINI_API_KEY', None)
    return subprocess.run([sys.executable, str(DEMO), '--workdir', str(workdir)],
                          cwd=str(ROOT), env=env, capture_output=True, text=True,
                          timeout=300)


def load_report(workdir):
    return json.loads((Path(workdir) / 'out' / 'report.json').read_text(encoding='utf-8'))


def test_demo_runs_end_to_end_without_credentials(tmp_path):
    workdir = tmp_path / 'ws'
    proc = run_demo(workdir)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert 'DEMO_OK cases=3 exceptions=0 provider_calls=0' in proc.stdout
    report = load_report(workdir)
    assert report['provider_calls'] == 0
    assert report['credentials_present'] == {'GEMINI_API_KEY': False,
                                             'GROQ_API_KEY': False}
    assert report['cache_entries'] == 3  # one scripted response per case
    assert len(report['cases']) == 3
    assert all(c['checks']['exception'] is False for c in report['cases'])
    assert [c['escalated'] for c in report['cases']] == [False, True, False]


def test_demo_metrics_and_honest_labels(tmp_path):
    workdir = tmp_path / 'ws'
    proc = run_demo(workdir)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = load_report(workdir)
    assert report['mode'].startswith('offline synthetic demonstration')
    assert report['model'] == 'scripted-offline-response'
    assert report['prompt_version'] == 'system_v3'
    assert report['embedding'].startswith('demo-local deterministic hash vectors')
    m = report['metrics']
    assert m['exception_rate']['numerator'] == 0
    assert m['obligation_recall']['value'] == 1.0
    assert m['escalation_recall']['value'] == 1.0
    assert m['false_escalation']['value'] == 0.0
    assert m['grounded_rate']['value'] == 1.0
    assert m['deadline_absolute']['value'] == 1.0
    assert m['deadline_relative']['value'] == 1.0
    assert m['deadline_none']['value'] == 1.0
    assert m['cost']['mean_usd'] == 0.0


def test_demo_writes_only_inside_its_workspace(tmp_path):
    workdir = tmp_path / 'ws'
    proc = run_demo(workdir)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=str(ROOT),
                            capture_output=True, text=True)
    assert status.returncode == 0, status.stderr
    for line in status.stdout.splitlines():
        path = line[3:]
        assert path.startswith('prototype/'), f'unexpected repository change: {line}'
    assert (workdir / 'out' / 'report.json').is_file()
    assert not (ROOT / 'eval_results' / 'scratch').exists()
