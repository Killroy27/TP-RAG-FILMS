import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from config import INDEX_FILE, METADATA_FILE, EMBEDDING_MODEL

_index = None
_metadata = None
_model = None

def get_vector_store():
    global _index, _metadata, _model
    if _index is None:
        if INDEX_FILE.exists():
            _index = faiss.read_index(str(INDEX_FILE))
        if METADATA_FILE.exists():
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                _metadata = json.load(f)
        if _model is None:
            _model = SentenceTransformer(EMBEDDING_MODEL)
    return _index, _metadata, _model

def search_semantic(query, k=5):
    index, metadata, model = get_vector_store()
    if index is None or not metadata:
        return []
    
    query_vector = model.encode([query]).astype('float32')
    distances, indices = index.search(query_vector, k)
    
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(metadata):
            results.append({
                "movie": metadata[idx],
                "score": float(dist)
            })
    return results

def get_stats():
    _, metadata, _ = get_vector_store()
    return {
        "total_movies": len(metadata) if metadata else 0,
        "index_ready": _index is not None
    }
