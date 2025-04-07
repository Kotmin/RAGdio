from app.services.audio_processor import AudioProcessor


class WhisperAudioProcessor(AudioProcessor):
    """Whisper ASR implementation."""

    def __init__(self, model_size: str = "small"):
        """Dynamically loads Whisper model when initialized."""
        try:
            import whisper  # Lazy import
        except ModuleNotFoundError:
            raise ImportError(
                "Whisper is not installed. Install it using 'pip install openai-whisper'"
            )

        self.whisper = whisper
        try:
            self.model = whisper.load_model(model_size)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to load Whisper model '{model_size}': {e}")

    def transcribe(self, audio_file: str) -> str:
        """Transcribes audio using Whisper."""
        try:
            result = self.model.transcribe(audio_file)
            return result.get("text", "").strip()
        except Exception as e:
            return f"❌ Whisper transcription error: {e}"
