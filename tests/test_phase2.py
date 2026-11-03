import csv,json,shutil,sqlite3
from pathlib import Path
import pytest,yaml
from agent.db import initialize,connect
from agent.tools import get_clause,ClauseNotFound
from scripts.build_corpus import build as build_corpus,select
from scripts.make_annotation_workspace import build as workspace
from scripts.make_adversarial import create as mutate
from scripts.make_composite import create as composite
from scripts.build_embeddings import chunk_document,build as embed_build
from scripts.build_cases import build as cases_build
from scripts.validate_cases import validate
from reviews.make_packet import choose,packet
from reviews.ingest_verdicts import ingest
from reviews.agreement import agreement


def make_root(tmp_path):
    root=tmp_path/'repo';root.mkdir();
    for p in ('db','corpus/documents','corpus/adversarial/source','cases/src','guide','config','eval_results','annotation'): (root/p).mkdir(parents=True,exist_ok=True)
    return root

def fixture_cuad(title,txt):
    return {'title':title,'paragraphs':[{'context':txt,'qas':[{'id':title+'__Category','answers':[{'text':txt[:3],'answer_start':0},{'text':txt[:6],'answer_start':0}]}]}]}

def test_full_span_uniqueness(db):
    with db:
        db.execute("INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES('d','cat','abc',0,3)")
        db.execute("INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES('d','cat','abcdef',0,6)")
    assert len(get_clause(db,'d','cat'))==2
    with pytest.raises(sqlite3.IntegrityError): db.execute("INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES('d','cat','abcdef',0,6)")

# test_core defines db as a module-local fixture; provide one for this module.
@pytest.fixture
def db(tmp_path):
    d=initialize(tmp_path/'db.sqlite')
    with d: d.execute("INSERT INTO corpus_documents(id,title) VALUES('d','Fixture')")
    yield d;d.close()

def test_selection_and_workspace_are_deterministic(tmp_path):
    root=make_root(tmp_path);source=tmp_path/'input';source.mkdir()
    cfg={'priority':['licence','other'],'rules':{'licence':'licen'},'min_conflict_candidates':0}
    (root/'config/family_priority.yaml').write_text(yaml.safe_dump(cfg,sort_keys=False))
    docs=[fixture_cuad('A - license', 'abcdef xyz 1234'),fixture_cuad('B - license','abcdef xyz'),fixture_cuad('C - miscellaneous','abcdef 123')]
    (source/'CUADv1.json').write_text(json.dumps({'data':docs}))
    first=build_corpus(source,3,root); selection=(root/'corpus/selection.json').read_bytes()
    assert len(first['picks'])==3 and workspace(root)==3
    d=connect(root/'db/b2.sqlite')
    with d:
        assert d.execute('SELECT count(*) FROM clause_labels').fetchone()[0]==6
    d.close()  # Windows: sqlite must release db/b2.sqlite before the rebuild's os.replace
    assert build_corpus(source,3,root)==first and (root/'corpus/selection.json').read_bytes()==selection

def seed(root):
    db=initialize(root/'db/b2.sqlite')
    with db:
        db.execute("INSERT INTO corpus_documents(id,title,char_count) VALUES('one','A',12),('two','B',12)")
        db.execute("INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES('one','C','abc',0,3),('one','C','abcdef',0,6),('two','C','ABC',0,3)")
        db.execute("INSERT INTO obligation_types(code,name,deadline_behaviour) VALUES('T','Fixture','none')")
    db.close();(root/'corpus/documents/one.txt').write_text('abcdefghijkl');(root/'corpus/documents/two.txt').write_text('ABCDEFGHIJKL')

def test_mutators_preserve_offsets_and_drop_overlaps(tmp_path):
    root=make_root(tmp_path);seed(root)
    ids={k:mutate(root,k,'one',0,3) for k in ('redacted','prompt_injection','truncated','exact_duplicate')}
    ids['empty']=mutate(root,'empty')
    supplied=tmp_path/'excerpt.txt';supplied.write_text('Ein Auszug.');ids['non_english']=mutate(root,'non_english','one',non_english_file=supplied)
    db=connect(root/'db/b2.sqlite')
    assert len((root/'corpus/documents'/f"{ids['redacted']}.txt").read_text(encoding='utf-8'))==12  # Windows: default locale encoding mangles U+2588
    assert db.execute('SELECT count(*) FROM clause_labels WHERE document_id=?',(ids['redacted'],)).fetchone()[0]==0
    assert len(get_clause(db,ids['exact_duplicate'],'C'))==2
    with pytest.raises(ClauseNotFound):get_clause(db,ids['non_english'],'C')
    assert (root/'corpus/documents'/f"{ids['empty']}.txt").read_text()==''
    assert mutate(root,'exact_duplicate','one')==ids['exact_duplicate'];db.close()

def test_composite_has_shifted_labels_and_provenance(tmp_path):
    root=make_root(tmp_path);seed(root);did=composite(root,['one','two'])
    manifest=json.loads((root/'corpus/adversarial/manifest.json').read_text());text=(root/'corpus/documents'/f'{did}.txt').read_text();db=connect(root/'db/b2.sqlite')
    for r in db.execute('SELECT answer_text,char_start,char_end FROM clause_labels WHERE document_id=?',(did,)):
        assert text[r['char_start']:r['char_end']]==r['answer_text']
    assert manifest[did]['source_document_ids']==['one','two'];db.close()

def test_chunks_and_embedding_replay_are_deterministic(tmp_path):
    root=make_root(tmp_path);seed(root);text='abcdefghijkl';labels=[{'category':'C','answer_text':'abc','char_start':0,'char_end':3}]
    one=chunk_document('one',text,labels,max_chars=5,overlap=1);two=chunk_document('one',text,labels,max_chars=5,overlap=1)
    assert one==two and all(c['text']==text[c['char_start']:c['char_end']] and len(c['text'])<=5 for c in one)
    calls=[]
    def provider(text,model): calls.append(text);return [1.,0.],{'latency_ms':1}
    count,dim=embed_build(root,provider,'fake');assert count>0 and dim==2 and calls
    def fail(*_): raise AssertionError('cached chunks must not invoke provider')
    assert embed_build(root,fail,'fake')==(count,dim)

def test_case_compilation_exact_refs_and_overlap(tmp_path):
    root=make_root(tmp_path);seed(root)
    (root/'config/splits.yaml').write_text(yaml.safe_dump({'dev':{'clear':1},'test':{'clear':1}}))
    def item(split):
        return {'id':split,'split':split,'class':'clear','document_id':'one','intake_party':'customer','gold_obligations':[{'type':'T','owed_by':'customer','clause_category':'C','deadline':{'kind':'none'},'clause_ref':{'category':'C','char_start':0,'char_end':3}}],'gold_should_escalate':False,'gold_escalation_codes':[],'rationale':'fixture only','difficulty':1}
    for split in ('dev','test'): (root/'cases/src'/f'{split}-fixture.yaml').write_text(yaml.safe_dump(item(split)))
    assert cases_build(root)==(1,1);assert validate(root,strict=True)['document_overlap']==1
    changed=item('test');changed['gold_obligations'][0]['clause_ref']['char_end']=4
    (root/'cases/src/test-fixture.yaml').write_text(yaml.safe_dump(changed))
    with pytest.raises(ValueError,match='commitment'):cases_build(root)
    cases_build(root,replace=True)
    with pytest.raises(ValueError,match='exact CUAD offsets'):validate(root,strict=True)

def test_review_ingestion_and_agreement(tmp_path):
    root=make_root(tmp_path);seed(root);db=connect(root/'db/b2.sqlite')
    with db:
        db.execute("INSERT INTO intakes(external_ref,document_id,intake_party,channel,received_at) VALUES('x','one','customer','test','now')")
        db.execute("INSERT INTO runs(intake_id,model,prompt_version,schema_version,corpus_version,status) VALUES(1,'m','p','s','c','escalated')")
        db.execute("INSERT INTO decisions(run_id,escalated) VALUES(1,1)")
        db.execute("INSERT INTO escalations(decision_id,reason_code,queue,created_at) VALUES(1,'E1_NO_OBLIGATION','legal-ops','now')")
    assert choose(db)==[1] and 'E1_NO_OBLIGATION' in packet(db,[1],'reviewer-1',7)
    paths=[]
    for i in range(3):
        path=tmp_path/f'v{i}.csv';paths.append(path)
        with path.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['escalation_id','reviewer_id','reviewer_role','verdict','note','human_obligation_count']);w.writeheader();w.writerow({'escalation_id':1,'reviewer_id':f'r{i}','reviewer_role':'reviewer','verdict':'agree','note':'','human_obligation_count':0})
    assert ingest(db,paths)==3
    result=agreement(db);assert result['pairwise_percent_agreement']==100 and result['fleiss_kappa'] is None
    assert db.execute('SELECT human_obligation_count FROM escalations').fetchone()[0]==0
    with pytest.raises(sqlite3.IntegrityError):ingest(db,[paths[0]])
    db.close()

def test_conflict_coverage_swaps_second_pick_only():
    def rec(did,family,length,flag):return {'id':did,'family':family,'title':did,'char_count':length,'conflict_pairs':[['a','b']] if flag else []}
    cfg={'priority':['a','b','other'],'rules':{'a':'a','b':'b'},'min_conflict_candidates':1}
    records=[rec('a1','a',100,False),rec('a2','a',80,False),rec('b1','b',90,False),rec('b2','b',20,True),rec('c1','other',60,False)]
    picks,swaps,coverage,_=select(records,4,cfg)
    assert coverage['after']==1 and len(swaps)==1
    assert {p['record']['id'] for p in picks}>={'a1','b1','c1','b2'}
    assert swaps[0]['removed']=='a2' and swaps[0]['added']=='b2'

def test_corpus_builder_refuses_to_destroy_authored_cases(tmp_path):
    root=make_root(tmp_path);src=tmp_path/'input';src.mkdir()
    cfg={'priority':['licence','other'],'rules':{'licence':'licen'},'min_conflict_candidates':0}
    (root/'config/family_priority.yaml').write_text(yaml.safe_dump(cfg))
    (src/'CUADv1.json').write_text(json.dumps({'data':[fixture_cuad('A - license','abcdef'),fixture_cuad('B - other','abcdef')]}))
    (root/'cases/src/dev-existing.yaml').write_text('human case content')
    with pytest.raises(ValueError,match='cases already exist'): build_corpus(src,2,root)

def test_review_incomplete_and_disagreement_require_notes(tmp_path):
    root=make_root(tmp_path);seed(root);db=connect(root/'db/b2.sqlite')
    with db:
        db.execute("INSERT INTO intakes(external_ref,document_id,intake_party,channel,received_at) VALUES('x','one','customer','test','now')")
        db.execute("INSERT INTO runs(intake_id,model,prompt_version,schema_version,corpus_version,status) VALUES(1,'m','p','s','c','escalated')")
        db.execute("INSERT INTO decisions(run_id,escalated) VALUES(1,1)")
        db.execute("INSERT INTO escalations(decision_id,reason_code,queue,created_at) VALUES(1,'E1_NO_OBLIGATION','legal-ops','now')")
    path=tmp_path/'bad.csv'
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['escalation_id','reviewer_id','reviewer_role','verdict','note','human_obligation_count']);w.writeheader();w.writerow({'escalation_id':1,'reviewer_id':'r','reviewer_role':'paralegal','verdict':'disagree','note':'','human_obligation_count':''})
    with pytest.raises(ValueError,match='requires a note'): ingest(db,[path])
    with pytest.raises(ValueError,match='three distinct reviewers'):agreement(db)
    assert db.execute('select count(*) from human_reviews').fetchone()[0]==0;db.close()

def test_build_cases_dev_only_does_not_raise(tmp_path):
    root=make_root(tmp_path);seed(root)
    (root/'config/splits.yaml').write_text(yaml.safe_dump({'dev':{'clear':1},'test':{'clear':1}}))
    def item(sid): return {'id':sid,'split':sid,'class':'clear','document_id':'one','intake_party':'customer','gold_obligations':[{'type':'T','owed_by':'customer','clause_category':'C','deadline':{'kind':'none'},'clause_ref':{'category':'C','char_start':0,'char_end':3}}],'gold_should_escalate':False,'gold_escalation_codes':[],'rationale':'x','difficulty':1}
    (root/'cases/src/dev-only.yaml').write_text(yaml.safe_dump(item('dev')))
    assert cases_build(root)==(1,0)
    (root/'cases/dev.json').unlink(); (root/'cases/test.json').unlink(missing_ok=True)
    with pytest.raises(ValueError,match='test split is empty'): cases_build(root,strict=True)
