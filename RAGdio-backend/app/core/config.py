import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """App configuration settings."""

    ASR_MODEL = os.getenv("ASR_MODEL", "whisper-api")  # alt: Whisper
    VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "qdrant")
    EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "huggingface") #alt: openai
    LLM_PROVIDER_TYPE = os.getenv("LLM_PROVIDER_TYPE", "openai") # alt: local, ollama, deepseek
    LLM_RAG_MODE = os.getenv("LLM_RAG_MODE", "rag_fallback")  # rag_fallback or rag_strict
    LOCAL_OLLM_API_URL = os.getenv("LOCAL_OLLM_API_URL", "http://localhost:11434/api/generate") 
    LOCAL_OLLM_MODEL = os.getenv("LOCAL_OLLM_MODEL", "zephyr")


    DEBUG = os.getenv("DEBUG", "False").lower(
    ) == "true"  # Convert string to bool


    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    @classmethod
    def validate(cls):
        """Ensures required env variables are set when needed."""
        if cls.ASR_MODEL == "whisper_api" and not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required for Whisper API but not set!")
        if cls.EMBEDDING_BACKEND == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required for OpenAI Embeddings API but not set!")
        
    


Config.validate()
