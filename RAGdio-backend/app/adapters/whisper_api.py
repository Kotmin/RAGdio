import os
from app.core.config import Config
import tempfile
from openai import OpenAI
from pydub import AudioSegment
from app.services.audio_processor import AudioProcessor

from app.core.logging_config import logger

class WhisperAPIAudioProcessor(AudioProcessor):
    """Whisper API ASR implementation."""

    SUPPORTED_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}
    MAX_FILE_SIZE_MB = 25  # Whisper API Limit

    def __init__(self):
        """Initialize OpenAI Whisper API client."""
        self.client = OpenAI()

    def _get_file_size_mb(self, file_path: str) -> float:
        """Returns file size in MB."""
        return os.path.getsize(file_path) / (1024 * 1024)

    def _is_supported_format(self, file_path: str) -> bool:
        """Checks if file extension is supported."""
        return file_path.split(".")[-1].lower() in self.SUPPORTED_FORMATS

    def _split_audio(self, file_path: str, chunk_size_ms: int = 60_000) -> list:
        """Splits an audio file into smaller chunks that Whisper can process."""
        audio = AudioSegment.from_file(file_path)
        chunks = [audio[i:i + chunk_size_ms]
                  for i in range(0, len(audio), chunk_size_ms)]

        temp_files = []
        for i, chunk in enumerate(chunks):
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp3")
            chunk.export(temp_file.name, format="mp3")
            temp_files.append(temp_file.name)

        return temp_files

    def transcribe(self, audio_file: str) -> str:
        """Transcribes audio using Whisper API with error handling & chunking."""
        try:
            logger.info(f"Using Whisper API")
            if not self._is_supported_format(audio_file):
                raise ValueError(
                    f"Unsupported file format. Supported formats: {self.SUPPORTED_FORMATS}")

            file_size = self._get_file_size_mb(audio_file)
            if file_size > self.MAX_FILE_SIZE_MB:
                print(
                    f"File too large ({file_size:.2f}MB). Splitting into chunks...")
                chunks = self._split_audio(audio_file)
            else:
                chunks = [audio_file]

            full_transcription = []
            for chunk in chunks:
                try:
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=open(chunk, "rb"),
                        response_format="srt",
                        temperature=0.3
                    )
                    # full_transcription.append(transcription.text)
                    full_transcription.append(transcription)
                except Exception as e:
                    print(f"Error processing chunk {chunk}: {e}")

            return "\n".join(full_transcription)

        except ValueError as ve:
            return f"ValueError: {ve}"
        except Exception as e:
            return f"Unexpected error: {e}"
