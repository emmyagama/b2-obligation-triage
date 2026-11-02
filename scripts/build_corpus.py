#!/usr/bin/env python3
"""Select a reproducible CUAD subset. Family groups are project-defined, not official."""
import argparse,hashlib,json,os,re,shutil,sqlite3,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import yaml
from agent.db import initialize
from agent.escalation import CONFLICT_PAIRS
ROOT=Path(__file__).resolve().parents[1]

def stable_id(title): return 'cuad_'+hashlib.sha256(title.encode('utf-8')).hexdigest()[:20]
def parse_family(title):
    matches=list(re.finditer(r'EX-[\w.()]+[-_]',title,re.I))
    if matches: return title[matches[-1].end():], 'last-ex-marker'
    return title.rsplit(' - ',1)[-1], 'fallback-last-dash' if ' - ' in title else 'fallback-full-title'
def family_for(title,cfg):
    raw,method=parse_family(title); norm=raw.replace('_',' ')
    for name in cfg['priority']:
        if name=='other': continue
        if re.search(cfg['rules'][name],norm,re.I): return name,raw,method
    return 'other',raw,method

def load_records(source,cfg):
    obj=json.loads(Path(source).read_text(encoding='utf-8')); out=[];titles=set();ids=set()
    for item in obj['data']:
        title=item['title']
        if title in titles: raise ValueError('duplicate CUAD title')
        titles.add(title);did=stable_id(title)
        if did in ids: raise ValueError('document id hash collision')
        ids.add(did)
        if len(item['paragraphs'])!=1: raise ValueError('expected one CUAD paragraph per title')
        p=item['paragraphs'][0]; text=p['context'];labels=[]; categories=set(); keys=set()
        for qa in p['qas']:
            if '__' not in qa['id']: raise ValueError('CUAD question id has no category suffix')
            cat=qa['id'].rsplit('__',1)[-1]
            for ans in qa['answers']:
                t=ans['text']; start=ans['answer_start'];end=start+len(t)
                if not isinstance(start,int) or start<0 or not t or text[start:end]!=t: raise ValueError('CUAD answer offset mismatch')
                key=(cat,start,end)
                if key in keys: raise ValueError('duplicate exact CUAD clause span')
                keys.add(key);labels.append((cat,t,start,end));categories.add(cat)
        family,raw,method=family_for(title,cfg)
        pairs=[sorted(p) for p in CONFLICT_PAIRS if p<=categories]
        out.append({'id':did,'title':title,'family':family,'source_family':raw,'family_method':method,'char_count':len(text),'text':text,'labels':labels,'conflict_pairs':sorted(pairs)})
    return out

def select(records,n,cfg):
    priority=cfg['priority'];groups={name:[] for name in priority}
    if len(priority)!=len(set(priority)) or not priority or priority[-1]!='other': raise ValueError('family priority must be unique and end with other')
    for r in records: groups[r['family']].append(r)
    for group in groups.values(): group.sort(key=lambda x:(-x['char_count'],x['title']))
    if any(not groups[name] for name in priority): raise ValueError('a configured family bucket is empty; adjust family rules before selection')
    if n < 1 or n > 2*len(priority): raise ValueError('n must be positive and at most two picks per bucket before conflict swaps')
    picks=[]
    for name in priority[:min(n,len(priority))]: picks.append({'record':groups[name][0], 'reason':'longest_per_bucket','original_bucket':name})
    for name in priority:
        if len(picks)>=n: break
        if len(groups[name])>1: picks.append({'record':groups[name][1], 'reason':'second_longest_priority','original_bucket':name})
    if len(picks)!=n: raise ValueError('insufficient eligible second-longest picks')
    before=sum(bool(p['record']['conflict_pairs']) for p in picks);swaps=[]; minimum=cfg['min_conflict_candidates']
    while sum(bool(p['record']['conflict_pairs']) for p in picks)<minimum:
        picked={p['record']['id'] for p in picks}
        options=sorted((r for r in records if r['id'] not in picked and r['conflict_pairs']),key=lambda r:(-r['char_count'],r['title']))
        replaceable=[(i,p) for i,p in enumerate(picks) if p['reason']=='second_longest_priority' and not p['record']['conflict_pairs']]
        if not options or not replaceable: break
        idx,old=max(replaceable,key=lambda t:priority.index(t[1]['original_bucket']))
        new=options[0];swaps.append({'removed':old['record']['id'],'added':new['id'],'displaced_bucket':old['original_bucket'],'reason':'conflict_candidate_coverage'})
        picks[idx]={'record':new,'reason':'conflict_coverage_swap','original_bucket':old['original_bucket']}
    return picks,swaps,{'minimum':minimum,'before':before,'after':sum(bool(p['record']['conflict_pairs']) for p in picks),'shortfall':max(0,minimum-sum(bool(p['record']['conflict_pairs']) for p in picks)),'candidate_not_adjudicated_conflict':True},groups

def build(cuad_dir,n,root=ROOT):
    source=Path(cuad_dir)/'CUADv1.json';cfg=yaml.safe_load((root/'config/family_priority.yaml').read_text())
    records=load_records(source,cfg);picks,swaps,coverage,groups=select(records,n,cfg)
    mutation_manifest=root/'corpus/adversarial/manifest.json'
    if mutation_manifest.exists() and json.loads(mutation_manifest.read_text()): raise ValueError('existing mutations would be overwritten; preserve them before rebuilding')
    if any((root/'cases/src').glob('*.yaml')) or (root/'cases/dev.json').exists() or (root/'cases/test.json').exists(): raise ValueError('cases already exist; refusing to overwrite their source corpus')
    dbpath=root/'db/b2.sqlite'
    if dbpath.exists():
        db=sqlite3.connect(dbpath)
        try:
            for table in ('intakes','runs','human_reviews'):
                if db.execute(f'SELECT count(*) FROM {table}').fetchone()[0]: raise ValueError('database contains workflow or review data; refusing to overwrite')
        finally: db.close()
    corpus=root/'corpus';corpus.mkdir(parents=True,exist_ok=True);(root/'db').mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='b2-build-',dir=root) as tmp:
        tmp=Path(tmp);docs=tmp/'documents';docs.mkdir(); (docs/'NOTICE').write_text('CUAD v1, The Atticus Project, NeurIPS 2021. CC BY 4.0. Source: https://github.com/The-Atticus-Project/cuad . This subset uses project-defined family buckets.\n',encoding='utf-8'); db=initialize(tmp/'b2.sqlite')
        manifest={'source':'CUADv1.json','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'family_definition':'project-defined title-derived buckets; not official CUAD families','family_priority':cfg['priority'],'family_rules':cfg['rules'],'rule':'longest per bucket, then second-longest in priority order; swap only second picks if conflict candidates below minimum; sort ties by title', 'bucket_counts':{k:len(groups[k]) for k in cfg['priority']},'reduced_bucket_coverage':n<len(cfg['priority']),'picks':[],'swaps':swaps,'conflict_coverage':coverage}
        with db:
            for pick in picks:
                r=pick['record'];(docs/(r['id']+'.txt')).write_bytes(r['text'].encode('utf-8'))
                db.execute('INSERT INTO corpus_documents(id,title,contract_family,source_url,char_count,page_count,license) VALUES(?,?,?,?,?,NULL,?)',(r['id'],r['title'],r['family'],'https://github.com/The-Atticus-Project/cuad',r['char_count'],'CC BY 4.0'))
                db.executemany('INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES(?,?,?,?,?)',[(r['id'],*x) for x in r['labels']])
                manifest['picks'].append({'document_id':r['id'],'title':r['title'],'family':r['family'],'source_family':r['source_family'],'family_method':r['family_method'],'char_count':r['char_count'],'reason':pick['reason'],'original_bucket':pick['original_bucket'],'conflict_candidate_pairs':r['conflict_pairs']})
        db.close();(tmp/'selection.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
        # Back up all prior outputs; restore them on any replacement error.
        dest=corpus/'documents';selection=corpus/'selection.json'
        old_docs=tmp/'old-documents';old_db=tmp/'old-b2.sqlite';old_selection=tmp/'old-selection.json'
        moved=[];installed=[]
        try:
            for current,backup in ((dest,old_docs),(dbpath,old_db),(selection,old_selection)):
                if current.exists(): os.replace(current,backup);moved.append((current,backup))
            for source_file,target in ((docs,dest),(tmp/'b2.sqlite',dbpath),(tmp/'selection.json',selection)):
                os.replace(source_file,target);installed.append(target)
        except Exception:
            for target in reversed(installed):
                if target.is_dir(): shutil.rmtree(target)
                elif target.exists(): target.unlink()
            for current,backup in reversed(moved): os.replace(backup,current)
            raise
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cuad-dir',required=True,type=Path);p.add_argument('--n',type=int,default=40);a=p.parse_args()
    try:
        m=build(a.cuad_dir,a.n);c=m['conflict_coverage'];print(f"selected {len(m['picks'])}; conflict candidates {c['after']}, shortfall {c['shortfall']}")
    except Exception as e: print(str(e),file=sys.stderr);sys.exit(1)
