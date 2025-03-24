from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.audio import router as audio_router
from app.core.config import Config

# Initialize FastAPI
app = FastAPI(title="RAG Over Audio",
              description="Transcribe audio and use RAG for LLM queries.")


app = FastAPI()

# Allow frontend dev server to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 👈 or ["*"] for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(audio_router, prefix="/api/audio",
                   tags=["Audio Processing"])


@app.get("/")
def health_check():
    return {"status": "OK", "message": "RAGdio: RAG Over Audio is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
