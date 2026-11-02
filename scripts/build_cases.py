#!/usr/bin/env python3
"""Compile only human-authored cases; never fabricate a field or label."""
import argparse,hashlib,json,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def build(root=ROOT,replace=False):
    log=root/'eval_results/test_run_log.jsonl'
    if log.exists() and any(json.loads(x).get('valid') is True and json.loads(x).get('status')=='completed' for x in log.read_text().splitlines() if x.strip()): raise ValueError('case compilation forbidden after frozen test results')
    grouped={'dev':[],'test':[]}
    files=sorted((root/'cases/src').glob('*.yaml'))
    if not files: raise ValueError('no human-authored YAML case files found')
    for p in files:
        if not p.name.startswith(('dev-','test-')): raise ValueError('case filenames must begin dev- or test-')
        data=yaml.safe_load(p.read_text());entries=data if isinstance(data,list) else [data]
        for item in entries:
            if not isinstance(item,dict) or item.get('split') not in grouped: raise ValueError('each case requires a valid split')
            if not p.name.startswith(item['split']+'-'): raise ValueError('file prefix must agree with split')
            grouped[item['split']].append(item)
    for split,items in grouped.items():
        if not items: raise ValueError(f'{split} split is empty')
        items.sort(key=lambda c:(str(type(c.get('id')).__name__),str(c.get('id'))))
        # Keep exact-duplicate cases after their originals, deterministically.
        ordered=[];pending=list(items);available=set()
        while pending:
            ready=[c for c in pending if c.get('duplicate_of') is None or str(c['duplicate_of']) in available]
            if not ready: raise ValueError('duplicate_of is missing, cyclic, or crosses splits')
            for c in ready: ordered.append(c);available.add(str(c.get('id')));pending.remove(c)
        items[:]=ordered
    encoded={k:(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8') for k,v in grouped.items()}
    digest=hashlib.sha256(encoded['test']).hexdigest();frozen=root/'cases/FROZEN.sha256'
    if frozen.exists() and frozen.read_text().split()[0]!=digest:
        devlog=root/'eval_results/dev_run_log.jsonl'
        if devlog.exists() and any(json.loads(x).get('status')=='started' for x in devlog.read_text().splitlines() if x.strip()): raise ValueError('held-out commitment cannot change after dev live runs begin')
        if not replace: raise ValueError('held-out commitment would change; pass --replace-commitment before freeze and publish the new commitment')
    for k,data in encoded.items():
        tmp=root/'cases'/('.'+k+'.json.tmp');tmp.write_bytes(data);tmp.replace(root/'cases'/f'{k}.json')
    frozen.write_text(digest+'  cases/test.json\n')
    return len(grouped['dev']),len(grouped['test'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replace-commitment',action='store_true');a=p.parse_args()
    try: d,t=build(replace=a.replace_commitment);print(f'compiled {d} dev and {t} test cases')
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
