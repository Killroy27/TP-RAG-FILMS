from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, TOP_K_RESULTS
from rag.retriever import hybrid_search

SYSTEM_PROMPT = """Tu es un expert en cinéma et un assistant de recommandation de films. 
Tu réponds en français de manière précise et professionnelle.

Base tes recommandations UNIQUEMENT sur le contexte des films fournis ci-dessous.
Pour chaque film recommandé :
1. Cite le titre et l'année de sortie.
2. Indique le score de pertinence (Match %).
3. Explique pourquoi ce film correspond à la recherche en te basant sur le synopsis.

Si aucun film ne correspond, suggère à l'utilisateur de reformuler sa recherche.

IMPORTANT : Termine ta réponse par la mention :
"Note : Cette recommandation est basée sur l'analyse sémantique du catalogue TMDB."
"""

def query_rag(question, lang_filter=None, history=None):
    # 1. Recherche
    results = hybrid_search(question, k=TOP_K_RESULTS, lang_filter=lang_filter)
    
    if not results:
        return {
            "answer": "Aucun résultat trouvé pour cette recherche. Veuillez essayer d'autres critères.",
            "sources": []
        }

    # 2. Contexte
    context = ""
    for i, res in enumerate(results, 1):
        m = res['movie']
        context += f"--- Film {i}: {m['title']} ({m['release_date'][:4]}) ---\n"
        context += f"Note: {m['vote_average']}/10 | Genres: {m['genres']}\n"
        context += f"Synopsis: {m['overview']}\n\n"

    # 3. Construction des messages avec historique
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if history:
        # On ajoute les 4 derniers messages pour garder du contexte sans saturer le prompt
        for msg in history[-4:]:
            messages.append({"role": "user" if msg["is_user"] else "assistant", "content": msg["text"]})
    
    # On ajoute la question actuelle enrichie du contexte
    prompt = f"Contexte des films disponibles :\n{context}\n\nQuestion de l'utilisateur : {question}"
    messages.append({"role": "user", "content": prompt})

    # 4. LLM
    client = Groq(api_key=GROQ_API_KEY)
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        temperature=0.7,
    )
    
    return {
        "answer": chat_completion.choices[0].message.content,
        "sources": [r['movie'] for r in results]
    }
