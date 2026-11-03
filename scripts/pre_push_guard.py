#!/usr/bin/env python3
"""Check all outgoing commit trees, not just the current index."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,stderr=subprocess.DEVNULL,text=True)
def protected(p):
    
    if p=='cases/test.json' or p.startswith(('cases/src/test-','cache/llm/','reviews/packets/','corpus/synthetic_test/','db/test_docs.sqlite')): return True
    if p.startswith('eval_results/'):
        rel=p[len('eval_results/'):]
        return not (rel in ('targets.md','threshold_calibration.md','test_run_log.jsonl') or rel.startswith(('run_dev_','summary_dev','metrics_dev','rounds/')))
    return False
def valid_log():
    path=ROOT/'eval_results/test_run_log.jsonl'
    if not path.exists(): return False
    try:
        commitment=(ROOT/'cases/FROZEN.sha256').read_text().split()[0]
        git('rev-parse','--verify','refs/tags/code-frozen')
        for line in path.read_text().splitlines():
            r=json.loads(line)
            if r.get('valid') is True and r.get('status')=='completed' and r.get('mode')=='live' and r.get('cases')==30 and r.get('case_sha256')==commitment: return True
    except (ValueError,IndexError,FileNotFoundError,subprocess.CalledProcessError): return False
    return False
def main():
    if valid_log():
        subprocess.run([sys.executable,str(ROOT/'scripts/freeze_check.py')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        print('pre-push guard passed: valid completed live run recorded'); return
    # Pre-push stdin lines are local_ref local_sha remote_ref remote_sha.
    # If no hook data is provided, conservatively check all commits not on remotes.
    lines=sys.stdin.read().splitlines(); ranges=[]
    for line in lines:
        parts=line.split()
        if len(parts)!=4: raise ValueError('invalid pre-push input')
        _,local,_,remote=parts
        if set(local)=={'0'}: continue
        ranges += [local] + (['^'+remote] if set(remote)!={'0'} else ['--not','--remotes'])
    if not lines: ranges=['HEAD','--not','--remotes']
    commits=git('rev-list',*ranges).splitlines()
    for commit in commits:
        paths=git('ls-tree','-r','--name-only',commit).splitlines()
        bad=[p for p in paths if protected(p)]
        if bad: raise ValueError('protected paths in outgoing commit '+commit[:12]+': '+', '.join(bad[:5]))
    # Also catch staged or local tracked secrets even before a commit.
    bad=[p for p in git('ls-files').splitlines() if protected(p)]
    if bad: raise ValueError('protected paths tracked before freeze: '+', '.join(bad[:5]))
    print('pre-push guard passed: no protected paths in outgoing history')
if __name__=='__main__':
    try: main()
    except Exception as e: print('pre-push guard: '+str(e),file=sys.stderr); sys.exit(1)
