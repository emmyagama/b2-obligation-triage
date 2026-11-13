#!/usr/bin/env python3
"""Fail closed for v1.1 without changing the preserved v1.0 freeze protocol.

The v1.0 guard remains in `scripts/freeze_check.py` and still validates the
original `code-frozen` tag from an immutable baseline checkout. This guard is
selected only when the separate `code-frozen-v1.1` tag exists.
"""
import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = 'code-frozen-v1.1'
GUIDE_TAG = 'guide-v1.0'
PROTECTED = [
    'agent', 'prompts', 'config', 'guide', 'run_eval.py', 'check_readme.py',
    'scripts', 'db/schema.sql', 'db/b2.sqlite',
    'corpus/adversarial/manifest.json', 'cases/FROZEN-SYNTHETIC.sha256',
    'corpus/documents', 'corpus/embeddings', 'corpus/selection.json',
    'cases/dev.json', 'cases/src/dev-*.yaml', 'cases/FROZEN.sha256',
]


def _git(root, *args):
    return subprocess.check_output(
        ['git', *args], cwd=root, stderr=subprocess.DEVNULL, text=True
    ).strip()


def check(root=ROOT):
    root = Path(root)
    sys.path.insert(0, str(root))

    test = root / 'cases/test.json'
    commitment = (root / 'cases/FROZEN.sha256').read_text().strip()
    match = re.match(r'^([0-9a-f]{64})(?:\s+\*?(?:cases/)?test\.json)?$', commitment)
    if not match or hashlib.sha256(test.read_bytes()).hexdigest() != match.group(1):
        raise ValueError('held-out hash mismatch or invalid FROZEN.sha256 format')

    data = json.loads(test.read_text())
    cases = data if isinstance(data, list) else data['cases']
    if len(cases) != 30 or len({str(c['id']) for c in cases}) != 30:
        raise ValueError('held-out set must contain 30 unique cases')

    import yaml
    splits = yaml.safe_load((root / 'config/splits.yaml').read_text())
    if collections.Counter(c['class'] for c in cases) != splits['test']:
        raise ValueError('held-out class counts do not match configured split')

    dev_path = root / 'cases/dev.json'
    dev_obj = json.loads(dev_path.read_text())
    dev = dev_obj if isinstance(dev_obj, list) else dev_obj['cases']
    if (len(dev) != sum(splits['dev'].values())
            or len({str(c['id']) for c in dev}) != len(dev)
            or collections.Counter(c['class'] for c in dev) != splits['dev']):
        raise ValueError('dev split is empty or does not match configured counts')

    from scripts.freeze_test_synthetics import digest as synthetic_digest
    expected = (root / 'cases/FROZEN-SYNTHETIC.sha256').read_text().split()[0]
    if expected != synthetic_digest(root):
        raise ValueError('local test synthetic commitment mismatch')

    for tag in (GUIDE_TAG, TAG):
        _git(root, 'rev-parse', '--verify', 'refs/tags/' + tag)

    if subprocess.run(['git', 'diff', '--quiet', TAG, '--', *PROTECTED],
                      cwd=root).returncode:
        raise ValueError('protected v1.1 code differs from ' + TAG + ' tag')
    if subprocess.run(['git', 'diff', '--quiet', GUIDE_TAG, '--', 'guide'],
                      cwd=root).returncode:
        raise ValueError('guide differs from ' + GUIDE_TAG + ' tag')

    untracked = _git(root, 'ls-files', '--others', '--exclude-standard', '--', *PROTECTED)
    if untracked:
        raise ValueError('untracked protected files present: ' + untracked.splitlines()[0])

    thresholds = yaml.safe_load((root / 'config/thresholds.yaml').read_text())
    report = root / 'eval_results/threshold_calibration.md'
    if (not report.exists()
            or thresholds.get('calibration_sha256')
            != hashlib.sha256(report.read_bytes()).hexdigest()):
        raise ValueError('threshold calibration report hash mismatch')
    if any(str(thresholds[k].get('provenance', '')).startswith('provisional')
           for k in ('e1', 'e5')):
        raise ValueError('provisional thresholds cannot be frozen')

    print('v1.1 freeze check passed')


if __name__ == '__main__':
    try:
        check()
    except Exception as e:
        print('v1.1 freeze check failed: ' + str(e), file=sys.stderr)
        sys.exit(1)
