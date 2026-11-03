"""Synthetic-only v1.1 coverage; the optional full check reads only the base Chroma store."""
import hashlib,json,os,sqlite3
from pathlib import Path
import numpy as np
import pytest,yaml
from agent.db import initialize
from agent.lean_index import LeanIndex,Shards,save,sha
from agent.synthetic import merge_test,document_path
from agent.corpus_version import version
from agent.cache import key_for
from agent.llm import request_object
from agent.taxonomy import load_taxonomy
from scripts.build_embeddings import build
from scripts.make_composite import create as composite
from scripts.make_adversarial import create as mutate
from scripts.pre_push_guard import protected
from tests.test_phase2 import make_root,seed

def provider(text,model): return [float(len(text)),1.0],{}

def test_cosine_rounded_ties_slice_and_checksum(tmp_path):
    docs=tmp_path/'docs';docs.mkdir();(docs/'d.txt').write_text('αβ中文!',encoding='utf-8')
    rows=[{'chunk_id':cid,'doc_id':'d','char_start':0,'char_end':4,'clause_category':None} for cid in ('z','a')]
    save(tmp_path/'i',rows,[[2,0],[1,0]],'fake',document_hashes={'d':sha(docs/'d.txt')})
    idx=LeanIndex(tmp_path/'i',docs,'fake');hits=idx.search([1,0],'d')
    assert [r['chunk_id'] for r in hits]==['a','z'] and all(r['score']==1.0 and r['text']=='αβ中文' for r in hits)
    assert set(json.loads((tmp_path/'i/chunks.json').read_text())[0])=={'chunk_id','doc_id','char_start','char_end','clause_category'}
    assert idx.search([0,0],'d')[0]['score']==0
    with pytest.raises(ValueError): idx.search([1,0,2],'d')
    (docs/'d.txt').write_text('changed')
    with pytest.raises(ValueError,match='content changed'): LeanIndex(tmp_path/'i',docs,'fake')

def test_test_shard_isolation_and_composite_offsets(tmp_path):
    root=make_root(tmp_path);seed(root)
    a=composite(root,['one','two'],split='test');assert composite(root,['one','two'],split='test')==a
    assert composite(root,['two','one'],split='test')!=a
    b=mutate(root,'prompt_injection','one',split='test')
    assert not (root/'corpus/documents'/f'{a}.txt').exists()
    base=sqlite3.connect(root/'db/b2.sqlite');assert not base.execute('select 1 from corpus_documents where id=?',(a,)).fetchone()
    memory=sqlite3.connect(':memory:');base.backup(memory);base.close();merge_test(memory,root)
    text=document_path(root,a).read_text();manifest=json.loads((root/'corpus/synthetic_test/manifest.json').read_text())
    for answer,start,end in memory.execute('select answer_text,char_start,char_end from clause_labels where document_id=?',(a,)): assert text[start:end]==answer
    assert manifest[a]['sources'][1]['char_start']==len('abcdefghijkl')+len(manifest[a]['separator'])
    assert memory.execute('select count(*) from corpus_documents where id=?',(b,)).fetchone()[0]==1
    memory.close()
    (root/'config/model.yaml').write_text('embedding_dimensions: 2\n')
    build(root,provider,'fake',split='dev');base_version=version(root)
    build(root,provider,'fake',split='test');assert version(root)==base_version
    baseidx=LeanIndex(root/'corpus/embeddings',root/'corpus/documents','fake');testidx=LeanIndex(root/'corpus/synthetic_test/index',root/'corpus/synthetic_test/documents','fake')
    assert Shards(baseidx,testidx).search([1,1],a)[0]['document_id']==a
    for p in ('corpus/synthetic_test/documents/x.txt','corpus/synthetic_test/index/vectors.npy','db/test_docs.sqlite','db/test_docs.sqlite-wal'): assert protected(p)

def test_version_and_request_key_binding(tmp_path):
    root=make_root(tmp_path);seed(root);build(root,provider,'fake');v=version(root)
    req=request_object('m',[],[],'auto',0,2,v,'a'*64); req2=request_object('m',[],[],'auto',0,2,v,'b'*64)
    assert key_for(req)!=key_for(req2)
    (root/'corpus/documents/one.txt').write_text('changed')
    assert version(root)!=v

def test_taxonomy_accepts_human_integers_but_not_other_values(tmp_path):
    db=initialize(tmp_path/'base.sqlite');p=tmp_path/'t.yaml'
    def write(val): p.write_text(yaml.safe_dump({'categories':[{'category':'C','include':True,'code':'T','name':'Test','deadline_behaviour':'none','escalates_by_default':val}]}))
    for v in (0,1,False,True): write(v);assert load_taxonomy(db,p)[0][-1]==int(v)
    for v in (2,'1',None):
        write(v)
        with pytest.raises(ValueError): load_taxonomy(db,p)
    db.close()

def test_synthetic_chroma_export_and_all_slices(tmp_path):
    pytest.importorskip('chromadb')
    from agent.chroma_store import build as chroma_build,digest as chroma_digest
    from scripts.export_lean_index import export
    root=make_root(tmp_path);seed(root)
    (root/'config/model.yaml').write_text('embedding_model: fake\n')
    chunks=[{'chunk_id':'a','document_id':'one','clause_category':'C','section_hint':'C','char_start':0,'char_end':3,'text':'abc','embedding':[1.,0.]},
            {'chunk_id':'b','document_id':'two','clause_category':None,'section_hint':'unlabelled paragraph','char_start':1,'char_end':4,'text':'BCD','embedding':[0.,1.]}]
    path=tmp_path/'chroma';stored=chroma_build(path,chunks)
    (root/'corpus/embeddings').mkdir(parents=True,exist_ok=True)
    (root/'corpus/embeddings/manifest.json').write_text(json.dumps({'store':'chroma','model_id':'fake','chunks':len(stored),'content_sha256':chroma_digest(stored)}))
    before={str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in path.rglob('*') if p.is_file()}
    report=export(root,path,expect_chunks=2,queries=2)
    after={str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest() for p in path.rglob('*') if p.is_file()}
    assert before==after and report['verified_chunks']==2 and report['unindexed_base_documents']==0
    idx=LeanIndex(root/'corpus/embeddings',root/'corpus/documents','fake')
    assert idx.search([1,0],'one')[0]['text']=='abc'
    with pytest.raises(ValueError,match='expected'): export(root,path,expect_chunks=14903)

def test_local_chroma_all_14903_slices():
    store=os.environ.get('B2_CHROMA_STORE');base=os.environ.get('B2_BASE_ROOT')
    if not store or not base: pytest.skip('Set B2_CHROMA_STORE and B2_BASE_ROOT for the local full-store verification')
    pytest.importorskip('chromadb')
    from agent.chroma_store import load
    chunks=load(Path(store));root=Path(base);assert len(chunks)==14903
    idx=LeanIndex(root/'corpus/embeddings',root/'corpus/documents')
    metadata={r['chunk_id']:r for r in idx.rows}
    documents={}
    for c in chunks:
        did=c['document_id']
        if did not in documents: documents[did]=(root/'corpus/documents'/f'{did}.txt').read_text(encoding='utf-8')
        row=metadata[c['chunk_id']]
        assert row=={'chunk_id':c['chunk_id'],'doc_id':did,'clause_category':c['clause_category'],'char_start':c['char_start'],'char_end':c['char_end']}
        assert documents[did][row['char_start']:row['char_end']]==c['text']

def test_synthetic_freeze_detects_tampering_and_blocks_reseal(tmp_path):
    from scripts.freeze_test_synthetics import digest,seal
    root=make_root(tmp_path);seed(root);composite(root,['one','two'],split='test')
    build(root,provider,'fake',split='test');sealed=seal(root);assert digest(root)==sealed
    p=next((root/'corpus/synthetic_test/documents').glob('*.txt'));p.write_text(p.read_text()+'x')
    assert digest(root)!=sealed
    (root/'eval_results/dev_run_log.jsonl').write_text('{"status":"started"}\n')
    with pytest.raises(ValueError,match='cannot change'): seal(root)

def test_validation_merges_private_composite_without_touching_base(tmp_path):
    from scripts.validate_cases import validate
    root=make_root(tmp_path);seed(root);did=composite(root,['one','two'],split='test')
    dev={'id':'fixture-dev','split':'dev','class':'clear','document_id':'one','intake_party':'customer','gold_obligations':[],'gold_should_escalate':False,'gold_escalation_codes':[],'rationale':'fixture only','difficulty':1}
    test={'id':'fixture-test','split':'test','class':'conflicting','document_id':did,'source_document_ids':['one','two'],'constructed':True,'intake_party':'customer','gold_obligations':[],'conflict_clause_refs':[{'document_id':'one','category':'C','char_start':0,'char_end':3},{'document_id':'two','category':'C','char_start':0,'char_end':3}],'gold_should_escalate':True,'gold_escalation_codes':['E2_CONFLICTING_CLAUSES'],'rationale':'fixture only','difficulty':2}
    (root/'config/splits.yaml').write_text(yaml.safe_dump({'dev':{'clear':1},'test':{'conflicting':1}}))
    (root/'cases/dev.json').write_text(json.dumps([dev]));(root/'cases/test.json').write_text(json.dumps([test]))
    dbfile=root/'db/b2.sqlite';before=sha(dbfile)
    assert validate(root,strict=True)['document_overlap']==1 and sha(dbfile)==before
    test['constructed']=False;(root/'cases/test.json').write_text(json.dumps([test]))
    with pytest.raises(ValueError,match='constructed'):validate(root,strict=True)
