# Compte-Rendu : Construction d'un RAG de Recommandation de Films

## 1. Choix du Sujet
J'ai choisi le **Sujet A : Recommandation de Films**. Ce sujet est particulièrement intéressant car il confronte le système RAG à des données tabulaires (CSV) plutôt qu'à des documents textuels classiques, nécessitant une étape de transformation des données en "descriptions textuelles riches".

## 2. Décisions de Conception

### Ingestion et Chunking
Contrairement à des documents longs (PDF), les synopsis de films sont courts. Ma stratégie a été d'adopter un **chunking de 1 document = 1 film**. 
Chaque chunk est construit en concaténant le titre, les genres (extraits du JSON) et le synopsis. Cette approche garantit que l'IA dispose de toutes les métadonnées sémantiques nécessaires pour chaque film lors de la recherche vectorielle.

### Modèle d'Embedding et Gestion de la Langue
Le dataset étant en anglais et les requêtes attendues en français, j'ai opté pour le modèle **`paraphrase-multilingual-mpnet-base-v2`** de Sentence-Transformers. 
- **Avantage** : Il permet de projeter des phrases de langues différentes dans le même espace vectoriel. Une question comme "un film de science-fiction avec des robots" sera naturellement proche de synopsis contenant "sci-fi" et "robots" en anglais.
- **Alternative écartée** : La traduction automatique des requêtes via LLM, qui aurait ajouté de la latence et des coûts d'API inutiles.

### Base Vectorielle
J'ai utilisé **FAISS (IndexFlatL2)** pour sa rapidité et sa simplicité de mise en œuvre sans dépendance à un serveur externe. L'index est persisté sur disque aux côtés d'un fichier JSON de métadonnées pour permettre un rechargement instantané sans ré-indexation.

### Prompt Engineering et Contrôle du LLM
Le prompt système a été conçu pour :
- Forcer le LLM à ne citer que les films présents dans le contexte (prévention des hallucinations).
- Inclure systématiquement la note moyenne pour aider l'utilisateur.
- Respecter les contraintes éthiques (mention de responsabilité à la fin).

## 3. Difficultés Rencontrées
- **Parsing du JSON** : La colonne `genres` du CSV TMDB contient des listes de dictionnaires au format texte. Il a fallu utiliser `json.loads()` pour transformer ces données en chaînes de caractères exploitables.
- **Filtre de langue** : Le filtrage par langue originale ne peut pas se faire directement dans un index vectoriel simple comme IndexFlatL2. J'ai résolu cela en récupérant un plus grand nombre de résultats (Top-K plus large) puis en filtrant les métadonnées en Python avant de passer le contexte final au LLM.

## 4. Conclusion
Le système final est performant (réponse en < 2s) et robuste. L'utilisation d'une recherche vectorielle multilingue s'est avérée être la clé pour rendre un dataset anglophone accessible à un utilisateur francophone de manière fluide.
