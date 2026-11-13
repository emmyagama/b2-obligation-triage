#!/usr/bin/env python3
"""Select the preserved v1.0 guard or the separately versioned v1.1 guard."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _has_tag(tag):
    return subprocess.run(
        ['git', 'rev-parse', '--verify', 'refs/tags/' + tag],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def active():
    return 'scripts/freeze_check_v11.py' if _has_tag('code-frozen-v1.1') else 'scripts/freeze_check.py'


def run():
    subprocess.run([sys.executable, str(ROOT / active())], cwd=ROOT, check=True)


if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
