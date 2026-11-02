"""Bind replay request identity to source text, labels, mutation provenance and embeddings."""
import hashlib,json,sqlite3
from pathlib import Path

def version(root):
    root=Path(root);h=hashlib.sha256()
    for p in (root/'corpus/selection.json',root/'corpus/adversarial/manifest.json',root/'corpus/embeddings/chunks.json',root/'corpus/embeddings/manifest.json'):
        h.update(str(p.relative_to(root)).encode()+b'\0')
        h.update(hashlib.sha256(p.read_bytes()).digest() if p.exists() else b'ABSENT')
    db=sqlite3.connect(root/'db/b2.sqlite')
    for table,query in [('documents','SELECT id,title,contract_family,char_count FROM corpus_documents ORDER BY id'),('labels','SELECT document_id,category,answer_text,char_start,char_end FROM clause_labels ORDER BY document_id,category,char_start,char_end')]:
        h.update(table.encode()+b'\0')
        for row in db.execute(query): h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
    for (did,) in db.execute('SELECT id FROM corpus_documents ORDER BY id'):
        h.update(did.encode()+b'\0');h.update(hashlib.sha256((root/'corpus/documents'/f'{did}.txt').read_bytes()).digest())
    db.close();return 'sha256:'+h.hexdigest()
