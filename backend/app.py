from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import sys
import os

# Ajouter le parent au path pour les imports modulaires
sys.path.append(str(Path(__file__).parent.parent))

from config import API_HOST, API_PORT, CORS_ORIGINS
from agents.orchestrator import process_message
from rag.vectorstore import get_stats

app = FastAPI(title="MovieBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    lang_filter: Optional[str] = None
    history: Optional[list] = None

@app.on_event("startup")
async def startup():
    # Initialiser les ressources
    from rag.vectorstore import get_vector_store
    get_vector_store()

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = process_message(
            request.message, 
            lang_filter=request.lang_filter,
            history=request.history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def status():
    stats = get_stats()
    return {
        "status": "online",
        "total_movies": stats["total_movies"],
        "index_ready": stats["index_ready"]
    }

# Servir le frontend
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

@app.get("/")
async def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/css/{file_path:path}")
async def serve_css(file_path: str):
    return FileResponse(str(FRONTEND_DIR / "css" / file_path))

@app.get("/js/{file_path:path}")
async def serve_js(file_path: str):
    return FileResponse(str(FRONTEND_DIR / "js" / file_path))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
