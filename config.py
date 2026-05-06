from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# === File Paths ===
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INDEX_FILE = DATA_DIR / "faiss_index.bin"
METADATA_FILE = DATA_DIR / "metadata.json"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# === Model Configuration ===
# Multilingual embedding model
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"

# LLM Provider Configuration
LLM_PROVIDER = "groq"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

# === Paramètres RAG ===
TOP_K_RESULTS = 5
BM25_WEIGHT = 0.3
SEMANTIC_WEIGHT = 0.7
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# === API ===
API_HOST = "0.0.0.0"
API_PORT = 8001
CORS_ORIGINS = ["*"]
