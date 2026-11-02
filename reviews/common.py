import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def default_review_db():
    manifest=ROOT/'reviews/packets/manifest.json'
    if not manifest.exists(): raise ValueError('review packet manifest not found; pass --db explicitly')
    path=Path(json.loads(manifest.read_text())['run_database'])
    if not path.is_file(): raise ValueError('review packet database is unavailable; pass --db explicitly')
    return path
