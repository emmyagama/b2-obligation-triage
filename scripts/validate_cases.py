#!/usr/bin/env python3
"""Validate human-written cases and exact CUAD references; do not judge labels."""
import argparse,collections,datetime,json,sqlite3,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import yaml
from agent.escalation import QUEUES
ROOT=Path(__file__).resolve().parents[1]

def data(path):
    obj=json.loads(path.read_text());return obj if isinstance(obj,list) else obj['cases']
def validate(root=ROOT,strict=False):
    db=sqlite3.connect(root/'db/b2.sqlite');db.row_factory=sqlite3.Row
    cfg=yaml.safe_load((root/'config/splits.yaml').read_text());types={r[0] for r in db.execute('SELECT code FROM obligation_types')}
    if not types:
        taxonomy=yaml.safe_load((root/'guide/obligation_types.yaml').read_text())
        types={x.get('code') for x in taxonomy.get('categories',[]) if x.get('include') is True and x.get('code')}
    if not types: raise ValueError('human-authored obligation types are missing')
    manifest_path=root/'corpus/adversarial/manifest.json'; manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    groups={s:data(root/'cases'/f'{s}.json') for s in ('dev','test')};seen=set();overlap={}
    classes={'clear','conflicting','out_of_scope','adversarial'};roles={'provider','customer','both','unclear'};intakes={'provider','customer','licensee','licensor','other'};kinds={'absolute','relative','recurring','none'}
    for split,cases in groups.items():
        counts=collections.Counter()
        for c in cases:
            ident=str(c.get('id',''))
            if not ident or ident in seen: raise ValueError('case ids must be present and globally unique')
            seen.add(ident)
            if c.get('split')!=split or c.get('class') not in classes or c.get('intake_party') not in intakes: raise ValueError('invalid case split, class, or intake party')
            counts[c['class']]+=1
            did=c.get('document_id');doc=db.execute('SELECT id FROM corpus_documents WHERE id=?',(did,)).fetchone()
            if not doc or not (root/'corpus/documents'/f'{did}.txt').is_file(): raise ValueError('case refers to an unknown document')
            if type(c.get('gold_should_escalate')) is not bool or not isinstance(c.get('gold_escalation_codes'),list) or set(c['gold_escalation_codes'])-QUEUES.keys(): raise ValueError('invalid human escalation label or codes')
            if c['gold_should_escalate'] != bool(c['gold_escalation_codes']): raise ValueError('escalation boolean and codes disagree')
            if not isinstance(c.get('rationale'),str) or not c['rationale'].strip() or type(c.get('difficulty')) is not int: raise ValueError('rationale and integer difficulty required')
            if not isinstance(c.get('gold_obligations'),list): raise ValueError('gold_obligations must be a list authored by the human')
            info=manifest.get(did,{});source_ids=info.get('source_document_ids') or ([info['source_document_id']] if info.get('source_document_id') else [did])
            declared=c.get('source_document_ids') or ([c['source_document_id']] if c.get('source_document_id') else [did])
            if sorted(source_ids)!=sorted(declared): raise ValueError('case source provenance disagrees with mutation manifest')
            overlap.setdefault(split,set()).update(source_ids)
            text=(root/'corpus/documents'/f'{did}.txt').read_text(encoding='utf-8')
            def ref_valid(ref):
                if not isinstance(ref,dict) or not isinstance(ref.get('category'),str) or type(ref.get('char_start')) is not int or type(ref.get('char_end')) is not int: raise ValueError('invalid clause_ref structure')
                ref_doc=ref.get('document_id',did)
                if ref_doc not in [did,*source_ids]: raise ValueError('clause_ref document is outside case provenance')
                row=db.execute('SELECT answer_text FROM clause_labels WHERE document_id=? AND category=? AND char_start=? AND char_end=?',(ref_doc,ref['category'],ref['char_start'],ref['char_end'])).fetchone()
                if not row: raise ValueError('clause_ref does not exist at exact CUAD offsets')
                shift=0
                if ref_doc!=did and info.get('mechanism')=='composite':
                    if ref_doc==source_ids[1]: shift=len((root/'corpus/documents'/f'{source_ids[0]}.txt').read_text(encoding='utf-8'))+len(info['separator'])
                if text[ref['char_start']+shift:ref['char_end']+shift]!=row['answer_text']: raise ValueError('referenced expert clause is not present at its mapped case offset')
                return (ref_doc,ref['category'],ref['char_start'],ref['char_end'])
            refs=[]
            for g in c['gold_obligations']:
                if not isinstance(g,dict) or g.get('type') not in types or g.get('owed_by') not in roles or not isinstance(g.get('clause_category'),str): raise ValueError('invalid obligation type, party, or category')
                ref=g.get('clause_ref');r=ref_valid(ref);refs.append(r)
                if g['clause_category']!=ref['category']: raise ValueError('clause category does not match clause_ref')
                deadline=g.get('deadline')
                if not isinstance(deadline,dict) or deadline.get('kind') not in kinds: raise ValueError('invalid deadline kind')
                if deadline['kind']=='absolute':
                    try: datetime.date.fromisoformat(deadline.get('resolved_date',''))
                    except (TypeError,ValueError): raise ValueError('absolute gold deadline requires an ISO date')
                if deadline.get('resolved_date'):
                    try: datetime.date.fromisoformat(deadline['resolved_date'])
                    except (TypeError,ValueError): raise ValueError('invalid resolved date')
                if deadline.get('offset_days') is not None and type(deadline['offset_days']) is not int: raise ValueError('offset_days must be an integer')
            for ref in c.get('conflict_clause_refs',[]): refs.append(ref_valid(ref))
            if c['class']=='conflicting' and len(set(refs))<2: raise ValueError('conflicting cases require two distinct exact clause refs')
            if c.get('duplicate_of') is not None and c['class']!='adversarial': raise ValueError('duplicate_of requires an adversarial case')
        expected=cfg[split]
        if strict and (dict(counts)!={k:v for k,v in expected.items() if v} or len(cases)!=sum(expected.values())): raise ValueError(f'{split} class counts or size do not match config/splits.yaml')
    for split,cases in groups.items():
        by_id={str(c['id']):c for c in cases}
        for c in cases:
            if c.get('duplicate_of') is not None:
                original=by_id.get(str(c['duplicate_of']))
                if original is None or original is c: raise ValueError('duplicate_of must reference a different case in the same split')
                if c['intake_party']!=original['intake_party'] or c.get('business_context')!=original.get('business_context'): raise ValueError('duplicate intake differs from original')
                if (root/'corpus/documents'/f"{c['document_id']}.txt").read_bytes()!=(root/'corpus/documents'/f"{original['document_id']}.txt").read_bytes(): raise ValueError('duplicate text differs from original')
    sources=overlap['dev'] & overlap['test']
    report={'dev_cases':len(groups['dev']),'test_cases':len(groups['test']),'document_overlap':len(sources),'strict':strict}
    (root/'eval_results').mkdir(parents=True,exist_ok=True);(root/'eval_results/case_validation.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    db.close();return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--strict',action='store_true');a=p.parse_args()
    try:
        r=validate(strict=a.strict);print(f"valid: {r['dev_cases']} dev, {r['test_cases']} test, {r['document_overlap']} shared source documents")
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
