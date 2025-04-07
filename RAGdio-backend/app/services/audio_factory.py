from app.services.audio_processor import AudioProcessor
from app.adapters.whisper_api import WhisperAPIAudioProcessor
from app.adapters.local_asr import LocalASRProcessor
from app.core.config import Config
from app.core.logging_config import logger

try:
    from app.adapters.whisper import WhisperAudioProcessor
    whisper_available = True
except ImportError:
    whisper_available = False


class AudioProcessorFactory:
    """Factory to create ASR models dynamically."""

    @staticmethod
    def get_audio_processor() -> AudioProcessor:
        model_name = Config.ASR_MODEL.lower()

        if model_name == "whisper":
            if not whisper_available:
                raise ValueError(
                    "Whisper is not installed. Set ASR_MODEL=whisper_api or install Whisper.")
            return WhisperAudioProcessor(model_size="large")
        elif model_name == "whisper-api":
            return WhisperAPIAudioProcessor()
        elif model_name == "wav2vec":
            try:
                from app.adapters.wav2vec_asr import Wav2VecASRProcessor
            except ImportError as e:
                logger.error("❌ Failed to import Wav2VecASRProcessor. Install 'transformers' and 'torchaudio'")
                raise e

            return Wav2VecASRProcessor()
        elif model_name == "local":
            return LocalASRProcessor(model_name="openai/whisper-small")
        else:
            raise ValueError(f"Unsupported ASR model: {model_name}")
