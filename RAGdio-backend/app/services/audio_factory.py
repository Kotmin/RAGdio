from app.services.audio_processor import AudioProcessor
from app.adapters.whisper import WhisperAudioProcessor
from app.adapters.whisper_api import WhisperAPIAudioProcessor  # New API-based Whisper
from app.adapters.local_asr import LocalASRProcessor  # Placeholder for local ASR
from app.core.config import Config

class AudioProcessorFactory:
    """Factory to create ASR models dynamically."""

    @staticmethod
    def get_audio_processor() -> AudioProcessor:
        model_name = Config.ASR_MODEL.lower()

        if model_name == "whisper":
            return WhisperAudioProcessor()  # Local Whisper Model
        elif model_name == "whisper_api":
            return WhisperAPIAudioProcessor()  # Whisper API
        elif model_name == "local":
            return LocalASRProcessor()  # Future local ASR
        else:
            raise ValueError(f"Unsupported ASR model: {model_name}")
