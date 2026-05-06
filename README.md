# MovieBot - RAG de Recommandation de Films

Ce projet est un système de Retrieval-Augmented Generation (RAG) permettant de recommander des films à partir du dataset TMDB 5000. Réalisé dans le cadre d'un TP sur la construction d'un RAG sans frameworks de haut niveau.

## Fonctionnalités
- Recherche Vectorielle : Utilisation de FAISS pour l'indexation sémantique.
- Multilingue : Support des requêtes en français sur un catalogue anglophone.
- Génération : Réponses structurées via l'API Groq (Llama 3).
- Interface Double : Support CLI (ligne de commande) et Interface Web.
- Filtrage : Gestion de la langue originale des films.

## 🚀 Installation

1. **Prérequis** : Python 3.10+
2. **Installation des dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuration** : Créez un fichier `.env` à la racine avec votre clé Groq :
   ```text
   GROQ_API_KEY=votre_cle_ici
   ```
4. **Données** : Placez le fichier `tmdb_5000_movies.csv` dans le dossier `data/`.
5. **Indexation** (à faire une fois) :
   ```bash
   python indexation.py
   ```

## 🛠️ Utilisation

### Interface CLI (TP)
```bash
python rag.py
```

### Interface Web (Bonus)
```bash
python backend/app.py
```
Puis ouvrez [http://localhost:8001](http://localhost:8001) dans votre navigateur.

## 📁 Structure du Projet
- `indexation.py` : Script d'ingestion et de création de l'index vectoriel.
- `rag.py` : Interface en ligne de commande.
- `rag_core.py` : Logique centrale du RAG (recherche + LLM).
- `backend/` : Serveur FastAPI pour l'interface Web.
- `frontend/` : Interface utilisateur élégante (HTML/CSS/JS).
