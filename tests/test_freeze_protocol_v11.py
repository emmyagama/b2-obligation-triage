import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import freeze_check_v11 as guard
from scripts import freeze_select as selector


def git(root, *args):
    subprocess.run(
        ['git', *args], cwd=root, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def make_repo(root):
    root.mkdir()
    (root / 'scripts').mkdir()
    (root / 'scripts' / 'placeholder.py').write_text('value = 1\n', encoding='utf-8')
    (root / 'guide').mkdir()
    (root / 'guide' / 'guide.md').write_text('guide\n', encoding='utf-8')
    (root / 'config').mkdir()
    (root / 'config' / 'splits.yaml').write_text(
        yaml.safe_dump({'test': {'clear': 30}, 'dev': {'clear': 1}}),
        encoding='utf-8',
    )
    (root / 'eval_results').mkdir()
    report = root / 'eval_results' / 'threshold_calibration.md'
    report.write_text('synthetic calibration\n', encoding='utf-8')
    (root / 'config' / 'thresholds.yaml').write_text(
        yaml.safe_dump({
            'e1': {'value': 0.0, 'provenance': 'dev-sweep'},
            'e5': {'value': 0.5, 'provenance': 'dev-sweep'},
            'calibration_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
        }),
        encoding='utf-8',
    )

    cases = [{'id': f'clear-{i}', 'class': 'clear'} for i in range(30)]
    raw = json.dumps(cases)
    (root / 'cases').mkdir()
    (root / 'cases' / 'test.json').write_text(raw, encoding='utf-8')
    (root / 'cases' / 'FROZEN.sha256').write_text(
        hashlib.sha256(raw.encode()).hexdigest() + '  cases/test.json\n',
        encoding='utf-8',
    )
    (root / 'cases' / 'dev.json').write_text(
        json.dumps([{'id': 'dev-clear-0', 'class': 'clear'}]),
        encoding='utf-8',
    )
    (root / 'cases' / 'FROZEN-SYNTHETIC.sha256').write_text(
        'a' * 64 + '  local-test-synthetic-shard\n', encoding='utf-8'
    )

    git(root, 'init', '-q', '-b', 'main')
    git(root, 'config', 'user.name', 'Synthetic')
    git(root, 'config', 'user.email', 'synthetic@example.invalid')
    git(root, 'config', 'commit.gpgsign', 'false')
    git(root, 'add', '.')
    git(root, 'commit', '-q', '-m', 'synthetic v1.1 freeze')
    git(root, 'tag', 'guide-v1.0')
    git(root, 'tag', 'code-frozen-v1.1')


def test_v11_guard_accepts_tagged_tree_and_rejects_protected_change(tmp_path, monkeypatch):
    root = tmp_path / 'repo'
    make_repo(root)
    monkeypatch.setattr('scripts.freeze_test_synthetics.digest', lambda _: 'a' * 64)

    guard.check(root)

    (root / 'scripts' / 'placeholder.py').write_text('value = 2\n', encoding='utf-8')
    with pytest.raises(ValueError, match='protected v1.1 code differs'):
        guard.check(root)


def test_selector_uses_v11_only_after_tag_exists(tmp_path, monkeypatch):
    root = tmp_path / 'repo'
    root.mkdir()
    git(root, 'init', '-q', '-b', 'main')
    git(root, 'config', 'user.name', 'Synthetic')
    git(root, 'config', 'user.email', 'synthetic@example.invalid')
    git(root, 'commit', '-q', '--allow-empty', '-m', 'empty')

    monkeypatch.setattr(selector, 'ROOT', root)
    assert selector.active() == 'scripts/freeze_check.py'

    git(root, 'tag', 'code-frozen-v1.1')
    assert selector.active() == 'scripts/freeze_check_v11.py'
