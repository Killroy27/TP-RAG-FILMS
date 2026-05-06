from rag.chain import query_rag
from rag.vectorstore import get_stats

def classify_query(message):
    msg = message.lower()
    if any(word in msg for word in ["bonjour", "salut", "hello"]):
        return "greeting"
    if any(word in msg for word in ["aide", "help", "comment"]):
        return "help"
    return "rag"

def handle_greeting():
    return {
        "answer": "Bonjour. Je suis votre assistant de recommandation cinématographique. Comment puis-je vous aider ?",
        "sources": []
    }

def handle_help():
    return {
        "answer": "Je peux vous aider à trouver des films par genre, ambiance ou thématique. Précisez votre recherche pour obtenir des recommandations pertinentes.",
        "sources": []
    }

def process_message(message, lang_filter=None, history=None):
    q_type = classify_query(message)
    if q_type == "greeting":
        return handle_greeting()
    elif q_type == "help":
        return handle_help()
    else:
        return query_rag(message, lang_filter=lang_filter, history=history)
