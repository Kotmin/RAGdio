from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.audio import router as audio_router
from app.routers.llm import router as llm_router
from app.core.config import Config
from app.core.logging_config import logger


# Initialize FastAPI
app = FastAPI(title="RAG Over Audio",
              description="Transcribe audio and use RAG for LLM queries.")


app = FastAPI()

# Allow frontend dev server to call API
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],
    allow_origins=["*"],  # 👈 or ["*"] for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(audio_router, prefix="/api/audio",
                   tags=["Audio Processing"])

app.include_router(llm_router, prefix="/api/llm")

@app.get("/")
def health_check():
    return {"status": "OK", "message": "RAGdio: RAG Over Audio is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
