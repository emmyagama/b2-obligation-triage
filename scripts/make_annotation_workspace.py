#!/usr/bin/env python3
import json,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def fence(text):
    longest=max((len(x) for x in __import__('re').findall(r'`+',text)),default=0)
    ticks='`'*max(3,longest+1)
    return ticks+'\n'+text+'\n'+ticks

def build(root=ROOT):
    selected=json.loads((root/'corpus/selection.json').read_text());out=root/'annotation/workspace';out.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(root/'db/b2.sqlite');db.row_factory=sqlite3.Row
    expected={p['document_id']+'.md' for p in selected['picks']}
    stale=[p for p in out.glob('*.md') if p.name not in expected]
    if stale: raise ValueError('workspace contains stale documents; remove or relocate them explicitly')
    for p in selected['picks']:
        did=p['document_id']
        rows=db.execute('SELECT category,answer_text,char_start,char_end FROM clause_labels WHERE document_id=? ORDER BY category,char_start,char_end',(did,)).fetchall()
        lines=['# CUAD annotation workspace','',f"Document ID: {did}",f"Family bucket: {p['family']}",f"Length (characters): {p['char_count']}",'', '## Conflict-candidate labels','']
        if p['conflict_candidate_pairs']:
            for pair in p['conflict_candidate_pairs']:
                lines += ['### '+ ' + '.join(pair)+' (candidate only)','']
                for r in rows:
                    if r['category'] in pair: lines += [f"{r['category']}; offsets {r['char_start']}–{r['char_end']}",'',fence(r['answer_text']),'']
        else: lines.append('No configured conflict-prone pair found among these labels.')
        lines += ['', '## CUAD-labelled clauses','']
        last=None
        for r in rows:
            if r['category']!=last: lines += ['### '+r['category'],''];last=r['category']
            lines += [f"Offsets: {r['char_start']}–{r['char_end']} (end exclusive)", '',fence(r['answer_text']),'']
        (out/(did+'.md')).write_text('\n'.join(lines),encoding='utf-8')
    db.close();return len(expected)
if __name__=='__main__':
    try: print(f'wrote {build()} annotation workspace files')
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
