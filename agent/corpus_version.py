"""Hash only committed base inputs, never embargoed test synthetic files."""
import hashlib,json,sqlite3
from pathlib import Path

def version(root):
    root=Path(root);folder=root/'corpus/embeddings';h=hashlib.sha256()
    def add(label,data):
        label=label.encode();h.update(len(label).to_bytes(8,'big'));h.update(label);h.update(len(data).to_bytes(8,'big'));h.update(data)
    m=json.loads((folder/'manifest.json').read_text())
    add('index-parameters',json.dumps({k:m[k] for k in ('format','model_id','dimensions','dtype','chunking')},sort_keys=True,separators=(',',':')).encode())
    add('chunks', (folder/'chunks.json').read_bytes());add('vectors', (folder/'vectors.npy').read_bytes())
    provenance=root/'corpus/adversarial/manifest.json';add('base-provenance',provenance.read_bytes() if provenance.exists() else b'ABSENT')
    db=sqlite3.connect(root/'db/b2.sqlite')
    try:
        for name,q in [('documents','SELECT id,title,contract_family,char_count FROM corpus_documents ORDER BY id'),('labels','SELECT document_id,category,answer_text,char_start,char_end FROM clause_labels ORDER BY document_id,category,char_start,char_end')]:
            add(name,json.dumps(db.execute(q).fetchall(),ensure_ascii=False,separators=(',',':')).encode())
        for (did,) in db.execute('SELECT id FROM corpus_documents ORDER BY id'):
            add('document:'+did,(root/'corpus/documents'/f'{did}.txt').read_bytes())
    finally: db.close()
    return 'sha256:'+h.hexdigest()
