from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    with (ROOT/'config'/name).open() as f: return yaml.safe_load(f)
