from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]

def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

def initialize(path):
    db = connect(path)
    db.executescript((ROOT / 'db/schema.sql').read_text())
    db.commit()
    return db
