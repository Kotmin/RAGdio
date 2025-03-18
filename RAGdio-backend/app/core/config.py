import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """App configuration settings."""

    ASR_MODEL = os.getenv("ASR_MODEL", "whisper")  # Default: Whisper
    DEBUG = os.getenv("DEBUG", "False").lower(
    ) == "true"  # Convert string to bool
