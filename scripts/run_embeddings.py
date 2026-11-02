import os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ['B2_OFFLINE'] = '0'
try:
    from agent.config import load
    from scripts.build_embeddings import build
    cfg = load('model.yaml')
    adapter = cfg.get('embedding_adapter')
    module, name = adapter.rsplit(':', 1)
    import importlib
    mod = importlib.import_module(module)
    provider = getattr(mod, name)
    batch_provider = getattr(mod, 'embed_batch', None)
    count, dim = build(ROOT, provider, cfg.get('embedding_model'), batch_provider=batch_provider)
    print(f'embedded {count} chunks, dimension {dim}')
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
