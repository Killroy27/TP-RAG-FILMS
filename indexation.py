import pandas as pd
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import DATA_DIR, MOVIES_CSV, INDEX_FILE, METADATA_FILE, EMBEDDING_MODEL

def parse_genres(genres_str):
    """Extrait les noms des genres du format JSON."""
    try:
        genres = json.loads(genres_str)
        return ", ".join([g['name'] for g in genres])
    except:
        return ""

def main():
    print(f"--- Indexation des films ---")
    
    if not MOVIES_CSV.exists():
        print(f"Erreur: {MOVIES_CSV} non trouvé.")
        return

    # 1. Chargement des données
    print("Chargement du dataset...")
    df = pd.read_csv(MOVIES_CSV)
    
    # Nettoyage de base
    df = df.dropna(subset=['title', 'overview'])
    
    # 2. Préparation du texte pour l'embedding (Chunking : 1 film = 1 chunk)
    print("Préparation des textes...")
    df['parsed_genres'] = df['genres'].apply(parse_genres)
    
    # Construction d'une description riche
    df['rich_text'] = df.apply(
        lambda x: f"Titre: {x['title']}. Genres: {x['parsed_genres']}. Synopsis: {x['overview']}", 
        axis=1
    )
    
    texts = df['rich_text'].tolist()
    
    # 3. Création des métadonnées
    print("Création des métadonnées...")
    metadata = []
    for idx, row in df.iterrows():
        metadata.append({
            "id": idx,
            "title": row['title'],
            "genres": row['parsed_genres'],
            "vote_average": row['vote_average'],
            "release_date": row['release_date'],
            "original_language": row['original_language'],
            "overview": row['overview']
        })

    # 4. Génération des Embeddings
    print(f"Génération des embeddings avec {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Convertir en float32 pour FAISS
    embeddings = np.array(embeddings).astype('float32')

    # 5. Création de l'index FAISS
    print("Création de l'index FAISS...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # 6. Sauvegarde
    print(f"Sauvegarde de l'index et des métadonnées dans {DATA_DIR}...")
    faiss.write_index(index, str(INDEX_FILE))
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

    print(f"Indexation terminée : {len(metadata)} films indexés.")

if __name__ == "__main__":
    main()
