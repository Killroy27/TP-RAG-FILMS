from rank_bm25 import BM25Okapi
from rag.vectorstore import get_vector_store, search_semantic
import re

_bm25 = None
_tokenized_corpus = None

def get_bm25():
    global _bm25, _tokenized_corpus
    if _bm25 is None:
        _, metadata, _ = get_vector_store()
        if not metadata:
            return None
        
        # Préparer le corpus pour BM25 (Titre + Synopsis + Genres)
        corpus = [f"{m['title']} {m['overview']} {m['genres']}" for m in metadata]
        _tokenized_corpus = [re.sub(r'[^\w\s]', '', doc.lower()).split() for doc in corpus]
        _bm25 = BM25Okapi(_tokenized_corpus)
    return _bm25

def search_bm25(query, k=5):
    bm25 = get_bm25()
    if bm25 is None:
        return []
    
    _, metadata, _ = get_vector_store()
    tokenized_query = re.sub(r'[^\w\s]', '', query.lower()).split()
    scores = bm25.get_scores(tokenized_query)
    
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    
    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            results.append({
                "movie": metadata[idx],
                "score": float(scores[idx]),
                "type": "bm25"
            })
    return results

def hybrid_search(query, k=5, lang_filter=None):
    search_k = k * 3
    
    # 1. Recherche BM25 (Mots-clés exacts)
    bm25_results = search_bm25(query, k=search_k)
    
    # 2. Recherche Sémantique (Sens global)
    semantic_results = search_semantic(query, k=search_k)
    for res in semantic_results:
        res["type"] = "semantic"

    # 3. Fusion simple (Priorité Sémantique mais inclusion BM25 si unique)
    # Dans un vrai système pro on utiliserait RRF (Reciprocal Rank Fusion)
    all_results = semantic_results + bm25_results
    
    # Déduplication par ID de film
    seen_ids = set()
    unique_results = []
    for res in all_results:
        movie_id = res['movie']['id']
        if movie_id not in seen_ids:
            # Filtrage par langue
            movie = res['movie']
            if lang_filter:
                if lang_filter == "fr" and movie['original_language'] != "fr":
                    continue
                if lang_filter == "intl" and movie['original_language'] == "fr":
                    continue
            
            unique_results.append(res)
            seen_ids.add(movie_id)
            
        if len(unique_results) >= k:
            break
            
    return unique_results
