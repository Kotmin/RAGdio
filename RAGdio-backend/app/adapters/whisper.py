from app.services.audio_processor import AudioProcessor


class WhisperAudioProcessor(AudioProcessor):
    """Whisper ASR implementation."""

    def __init__(self, model_size: str = "base"):
        """Dynamically loads Whisper model when initialized."""
        try:
            import whisper  # Lazy import
        except ModuleNotFoundError:
            raise ImportError(
                "Whisper is not installed. Install it using 'pip install openai-whisper'"
            )

        self.whisper = whisper
        self.model = self.whisper.load_model(model_size)

    def transcribe(self, audio_file: str) -> str:
        """Transcribes audio using Whisper."""
        result = self.model.transcribe(audio_file)
        return result["text"]
