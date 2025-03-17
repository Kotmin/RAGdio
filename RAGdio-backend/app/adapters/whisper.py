import whisper
from app.services.audio_processor import AudioProcessor


class WhisperAudioProcessor(AudioProcessor):
    """Whisper ASR implementation."""

    def __init__(self, model_size: str = "base"):
        """Loads Whisper model (default: 'base')."""
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_file: str) -> str:
        """Transcribes audio using Whisper."""
        result = self.model.transcribe(audio_file)
        return result["text"]
