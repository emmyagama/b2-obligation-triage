from pathlib import Path
import yaml

def load_taxonomy(db, path):
    obj=yaml.safe_load(Path(path).read_text())
    entries=obj.get('categories',[]) if isinstance(obj,dict) else None
    if not isinstance(entries,list) or not entries: raise ValueError('taxonomy is empty or invalid; human authors guide/obligation_types.yaml')
    rows=[]; seen=set()
    for e in entries:
        if not isinstance(e,dict) or not isinstance(e.get('category'),str) or type(e.get('include')) is not bool:
            raise ValueError('taxonomy entries require category and boolean include')
        if e['category'] in seen: raise ValueError('duplicate taxonomy category')
        seen.add(e['category'])
        if not e['include']: continue
        if not all(isinstance(e.get(k),str) and e[k].strip() for k in ('code','name','deadline_behaviour')) or not (type(e.get('escalates_by_default')) is bool or (type(e.get('escalates_by_default')) is int and e['escalates_by_default'] in (0,1))):
            raise ValueError('included taxonomy entry is incomplete')
        if e['deadline_behaviour'] not in ('absolute','relative','recurring','none'): raise ValueError('invalid deadline behaviour')
        rows.append((e['code'],e['name'],e['category'],e['deadline_behaviour'],int(e['escalates_by_default'])))
    if not rows: raise ValueError('taxonomy has no included categories')
    with db:
        for row in rows:
            db.execute('INSERT INTO obligation_types(code,name,cuad_category,deadline_behaviour,escalates_by_default) VALUES(?,?,?,?,?) ON CONFLICT(code) DO UPDATE SET name=excluded.name,cuad_category=excluded.cuad_category,deadline_behaviour=excluded.deadline_behaviour,escalates_by_default=excluded.escalates_by_default',row)
    return rows
