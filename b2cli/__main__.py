"""b2cli - B2 local contract-obligation triage CLI (post-signature, not legal advice)."""
import argparse
import os
import sys
from pathlib import Path

VERSION = '0.1.0'

EPILOG = """\
examples (POSIX / Windows use the same arguments):
  python -m b2cli --contract ./contract.txt --party customer --ref ACME-2026-01
  python -m b2cli --contract C:\\docs\\contract.txt --party provider --ref ACME-2026-01 \\
      --context "renewal year 2" --db b2cli_data/b2.sqlite --out b2cli_data/out

offline (default): responses are read from --cache-dir; a cache miss exits 3
and no network connection is attempted. live mode requires --live plus
--acknowledge-live, an explicit provider key in the environment (or --env-file),
and is only for functionality checks - it is not an accuracy claim.

WARNING: this tool does not provide legal advice. Escalated items require a human.
"""


def build_parser():
    p = argparse.ArgumentParser(
        prog='b2cli', description='B2 post-signature contract-obligation triage (local, SQLite-backed).',
        epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--version', action='version', version=f'b2cli {VERSION}')
    p.add_argument('--contract', required=False, type=Path, help='contract .txt file (UTF-8; cp1252 fallback; max 2 MB)')
    p.add_argument('--party', choices=['provider', 'customer', 'licensee', 'licensor', 'other'],
                   help='which side you are (stored as the intake party)')
    p.add_argument('--context', default='', help='optional business context')
    p.add_argument('--ref', help='explicit external reference / idempotency key')
    p.add_argument('--live', action='store_true', help='enable real provider calls (requires --acknowledge-live)')
    p.add_argument('--acknowledge-live', action='store_true',
                   help='acknowledge that the contract text will be sent to the configured LLM provider')
    p.add_argument('--env-file', type=Path, help='optional KEY=VALUE file providing provider credentials (never printed)')
    p.add_argument('--db', type=Path, default=Path('b2cli_data/b2.sqlite'), help='sqlite database path')
    p.add_argument('--cache-dir', type=Path, default=Path('b2cli_data/cache'), help='response cache directory')
    p.add_argument('--out', type=Path, default=Path('b2cli_data/out'), help='report output directory')
    p.add_argument('--max-cost-usd', type=float, help='hard spend cap enforced during live calls')
    p.add_argument('--max-requests', type=int, help='hard request cap enforced during live calls')
    p.add_argument('--verbose', action='store_true')
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if not args.contract or not args.party or not args.ref:
        print('b2cli: --contract, --party and --ref are required', file=sys.stderr)
        return 2

    if args.live:
        if not args.acknowledge_live:
            print('b2cli: --live requires --acknowledge-live.', file=sys.stderr)
            print('privacy: live mode transmits the contract text to the configured LLM provider API.',
                  file=sys.stderr)
            print('the contract must not be confidential unless you accept that transmission.', file=sys.stderr)
            return 1
        if os.environ.get('B2_OFFLINE') == '1':
            print('b2cli: refusing --live while B2_OFFLINE=1 is set in the environment.', file=sys.stderr)
            return 1
    else:
        # Must be set before the agent package is imported so its socket-level
        # guard is active for the whole process.
        os.environ['B2_OFFLINE'] = '1'

    from agent.cache import CacheMiss
    from b2cli.runner import BudgetExceeded, PathRefused, run_cli
    try:
        return run_cli(args)
    except CacheMiss as exc:
        print(f'b2cli: cache miss - offline replay cannot continue ({exc})', file=sys.stderr)
        return 3
    except BudgetExceeded as exc:
        print(f'b2cli: budget cap enforced - {exc}', file=sys.stderr)
        return 4
    except PathRefused as exc:
        print(f'b2cli: refused path - {exc}', file=sys.stderr)
        return 5
    except Exception as exc:  # surfaced without any key material
        print(f'b2cli: error: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
