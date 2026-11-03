"""Explicit local-only test synthetic paths and isolated database merge."""
import sqlite3
from pathlib import Path
from .db import initialize

def paths(root,split):
    root=Path(root)
    if split=='dev': return root/'db/b2.sqlite',root/'corpus/documents',root/'corpus/adversarial/manifest.json'
    if split=='test': return root/'db/test_docs.sqlite',root/'corpus/synthetic_test/documents',root/'corpus/synthetic_test/manifest.json'
    raise ValueError('split must be dev or test')

def open_output(root,split):
    dbpath,folder,manifest=paths(root,split);folder.mkdir(parents=True,exist_ok=True);manifest.parent.mkdir(parents=True,exist_ok=True)
    if split=='test' and not dbpath.exists():
        dbpath.parent.mkdir(parents=True,exist_ok=True);db=initialize(dbpath)
    else:
        db=sqlite3.connect(dbpath);db.row_factory=sqlite3.Row;db.execute('PRAGMA foreign_keys=ON')
    return db,folder,manifest

def merge_test(db,root):
    path=Path(root)/'db/test_docs.sqlite'
    if not path.exists(): return False
    src=sqlite3.connect(f'file:{path.resolve().as_posix()}?mode=ro',uri=True);src.row_factory=sqlite3.Row
    try:
        with db:
            for r in src.execute('SELECT id,title,contract_family,source_url,char_count,page_count,license FROM corpus_documents ORDER BY id'):
                if db.execute('SELECT 1 FROM corpus_documents WHERE id=?',(r['id'],)).fetchone(): raise ValueError('synthetic and base document IDs collide')
                db.execute('INSERT INTO corpus_documents(id,title,contract_family,source_url,char_count,page_count,license) VALUES(?,?,?,?,?,?,?)',tuple(r))
            for r in src.execute('SELECT document_id,category,answer_text,char_start,char_end FROM clause_labels ORDER BY document_id,category,char_start,char_end'):
                db.execute('INSERT INTO clause_labels(document_id,category,answer_text,char_start,char_end) VALUES(?,?,?,?,?)',tuple(r))
    finally: src.close()
    return True

def document_path(root,did):
    if not isinstance(did,str) or not did or Path(did).name!=did: raise ValueError('unsafe document id')
    base=Path(root)/'corpus/documents'/f'{did}.txt';test=Path(root)/'corpus/synthetic_test/documents'/f'{did}.txt'
    if base.exists() and test.exists(): raise ValueError('document exists in both shards')
    return base if base.exists() else test
