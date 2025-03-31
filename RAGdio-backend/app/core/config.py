import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """App configuration settings."""

    ASR_MODEL = os.getenv("ASR_MODEL", "whisper-api")  # alt: Whisper
    VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "qdrant")
    EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "huggingface")
    LLM_PROVIDER_TYPE = os.getenv("EMBEDDING_BACKEND", "openai") # alt: local
    DEBUG = os.getenv("DEBUG", "False").lower(
    ) == "true"  # Convert string to bool
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    @classmethod
    def validate(cls):
        """Ensures required env variables are set when needed."""
        if cls.ASR_MODEL == "whisper_api" and not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is required for Whisper API but not set!")


Config.validate()
