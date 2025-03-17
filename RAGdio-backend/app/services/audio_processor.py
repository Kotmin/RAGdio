from abc import ABC, abstractmethod

class AudioProcessor(ABC):
    """Abstract class for audio processing models."""

    @abstractmethod
    def transcribe(self, audio_file: str) -> str:
        """Transcribes an audio file and returns text."""
        pass
