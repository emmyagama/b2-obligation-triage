"""B1-compatible local sentence-transformers embedding adapter for B2."""
import os
from functools import lru_cache

MODEL_ID = "all-MiniLM-L6-v2"
DIMENSIONS = 384

@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer
    # Offline environments may point at an exported local copy of the same
    # model (verified by weights hash); default remains the hub model id.
    return SentenceTransformer(os.environ.get("B2_EMBEDDING_MODEL_PATH") or MODEL_ID)

def embed(text, model_id):
    if model_id != MODEL_ID:
        raise ValueError(f"Expected embedding model {MODEL_ID}, got {model_id}")
    m = _model()
    vec = m.encode(text, normalize_embeddings=False).tolist()
    meta = {"adapter": "b1_embedder", "model": MODEL_ID, "dimensions": len(vec)}
    return vec, meta

def embed_batch(texts, model_id):
    if model_id != MODEL_ID:
        raise ValueError(f"Expected embedding model {MODEL_ID}, got {model_id}")
    m = _model()
    vecs = m.encode(texts, normalize_embeddings=False, show_progress_bar=False).tolist()
    meta = {"adapter": "b1_embedder", "model": MODEL_ID, "dimensions": len(vecs[0]) if vecs else DIMENSIONS}
    return vecs, meta
