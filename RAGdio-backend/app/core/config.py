import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """App configuration settings."""

    ASR_MODEL = os.getenv("ASR_MODEL", "whisper-api")  # Default: Whisper
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
