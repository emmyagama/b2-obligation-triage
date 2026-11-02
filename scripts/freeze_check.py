#!/usr/bin/env python3
"""Fail closed unless the held-out commitment and the code and guide tags match."""
import hashlib,json,re,subprocess,sys,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
def check():
    test=ROOT/'cases/test.json'; commitment=(ROOT/'cases/FROZEN.sha256').read_text().strip()
    match=re.match(r'^([0-9a-f]{64})(?:\s+\*?(?:cases/)?test\.json)?$',commitment)
    if not match or hashlib.sha256(test.read_bytes()).hexdigest()!=match.group(1): raise ValueError('held-out hash mismatch or invalid FROZEN.sha256 format')
    data=json.loads(test.read_text()); cases=data if isinstance(data,list) else data['cases']
    if len(cases)!=30 or len({str(c['id']) for c in cases})!=30: raise ValueError('held-out set must contain 30 unique cases')
    import yaml
    splits=yaml.safe_load((ROOT/'config/splits.yaml').read_text())
    if collections.Counter(c['class'] for c in cases)!=splits['test']: raise ValueError('held-out class counts do not match configured split')
    for tag in ('guide-v1.0','code-frozen'): git('rev-parse','--verify','refs/tags/'+tag)
    # Guard the immutable code, prompts, taxonomy, config, scoring and guide.
    protected=['agent','prompts','config','guide','run_eval.py','check_readme.py','scripts','db/schema.sql','corpus/documents','corpus/embeddings','corpus/selection.json','cases/dev.json','cases/src/dev-*.yaml','cases/FROZEN.sha256']
    if subprocess.run(['git','diff','--quiet','code-frozen','--',*protected],cwd=ROOT).returncode: raise ValueError('protected code differs from code-frozen tag')
    if subprocess.run(['git','diff','--quiet','guide-v1.0','--','guide'],cwd=ROOT).returncode: raise ValueError('guide differs from guide-v1.0 tag')
    untracked=git('ls-files','--others','--exclude-standard','--',*protected)
    if untracked: raise ValueError('untracked protected files present: '+untracked.splitlines()[0])
    t=yaml.safe_load((ROOT/'config/thresholds.yaml').read_text()); report=ROOT/'eval_results/threshold_calibration.md'
    if not report.exists() or t.get('calibration_sha256')!=hashlib.sha256(report.read_bytes()).hexdigest(): raise ValueError('threshold calibration report hash mismatch')
    if any(str(t[k].get('provenance','')).startswith('provisional') for k in ('e1','e5')): raise ValueError('provisional thresholds cannot be frozen')
    print('freeze check passed')
if __name__=='__main__':
    try: check()
    except Exception as e: print('freeze check failed: '+str(e),file=sys.stderr); sys.exit(1)
