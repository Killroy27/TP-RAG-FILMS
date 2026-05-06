import sys
import os
from pathlib import Path

# Ajouter le chemin pour les modules
sys.path.append(str(Path(__file__).parent))

from agents.orchestrator import process_message
from rag.vectorstore import get_vector_store

def main():
    print("================================================")
    print("MovieBot - CLI Interface")
    print("================================================")
    print("Chargement des ressources techniques...")
    
    try:
        get_vector_store()
        print("Système opérationnel. Tapez 'exit' pour quitter.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation : {e}")
        return

    while True:
        try:
            question = input("\nRecherche > ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("Fin de session.")
                break
                
            if not question:
                continue

            # Détection simple de filtre de langue
            lang_filter = None
            if question.upper().endswith(" FR"):
                lang_filter = "fr"
                question = question[:-3].strip()
            elif question.upper().endswith(" VO"):
                lang_filter = "intl"
                question = question[:-3].strip()

            response = process_message(question, lang_filter=lang_filter)
            
            print("\n" + "-"*50)
            print(response["answer"])
            print("-"*50)

        except KeyboardInterrupt:
            print("\nFin de session.")
            break
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()
