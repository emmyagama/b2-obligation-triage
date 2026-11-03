#!/usr/bin/env python3
"""Scan authored prompts, code, tool descriptions and docs; never open test gold."""
import json,re,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def words(s): return re.findall(r"[\w]+",s.lower())
def grams(s):
    w=words(s); return {' '.join(w[i:i+8]) for i in range(len(w)-7)}
def check(root):
    corpus=set(); identifiers=set()
    for f in (root/'corpus/documents').rglob('*'):
        if f.is_file() and f.suffix.lower() in ('.txt','.md'):
            if f.stem.startswith(('adv_', 'composite_')): continue
            corpus |= grams(f.read_text(encoding='utf-8')); identifiers.add(f.stem)
    db=root/'db/b2.sqlite'
    if db.exists():
        conn=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
        try: identifiers.update(str(r[0]) for r in conn.execute('SELECT id FROM corpus_documents'))
        finally: conn.close()
    # Dev IDs are permitted; held-out cases are never opened by this tool.
    dev=root/'cases/dev.json'
    if dev.exists():
        data=json.loads(dev.read_text(encoding='utf-8')); data=data if isinstance(data,list) else data['cases']
        identifiers.update(str(c['id']) for c in data if len(str(c['id']))>=4 and not str(c['id']).isdigit())
    identifiers={x for x in identifiers if len(x)>=4}
    files=[]
    for folder in ('agent','prompts','scripts','guide','config','reviews','db','handoff'):
        files.extend(f for f in (root/folder).rglob('*') if f.is_file() and f.suffix in ('.py','.md','.yaml','.sql'))
    files += [root/'config/tool_descriptions.yaml',root/'run_eval.py',root/'check_readme.py']
    files += [root/'annotation/README-annotating.md']
    # OpenCode's historical integration log is preserved verbatim and may
    # contain identifiers; it is not a model prompt or generated documentation.
    files += [p for p in root.glob('*.md') if p.is_file() and p.name!='INTEGRATION-LOG.md']
    for p in files:
        if not p.exists(): continue
        text=p.read_text(encoding='utf-8')
        if re.search(r'\b(?:CUAD_[A-Za-z0-9_]*[0-9][A-Za-z0-9_]*|case[_ -]?\d+)\b',text,re.I): raise ValueError(f'identifier pattern in {p.relative_to(root)}')
        for ident in identifiers:
            if re.search(r'(?<![\w])'+re.escape(ident)+r'(?![\w])',text,re.I): raise ValueError(f'document or case id in {p.relative_to(root)}')
        if grams(text)&corpus: raise ValueError(f'corpus text in {p.relative_to(root)}')
    print('prompt hygiene passed')
if __name__=='__main__':
    try: check(ROOT)
    except Exception as e: print(str(e),file=sys.stderr); sys.exit(1)
