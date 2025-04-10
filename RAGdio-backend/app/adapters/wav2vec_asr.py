import os
import warnings
import numpy as np
from pathlib import Path
from pydub import AudioSegment
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch

from app.services.audio_processor import AudioProcessor
from app.core.logging_config import logger


class Wav2VecASRProcessor(AudioProcessor):
    """Offline Wav2Vec2 ASR processor (English + Polish capable)."""

    SUPPORTED_INPUT_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}

    # def __init__(self, model_name="facebook/wav2vec2-large-xlsr-53"):
    def __init__(self, model_name="facebook/wav2vec2-large-xlsr-960h"):
        self.model_dir = Path("/app/models") / model_name.replace("/", "-")
        if not self.model_dir.exists():
            # fallback for dev/local
            fallback = Path("./models") / model_name.replace("/", "-")
            if fallback.exists():
                self.model_dir = fallback
            else:
                raise FileNotFoundError(f"❌ Model not found at {self.model_dir} or {fallback}")

        logger.info(f"✅ Using Wav2Vec2 model from: {self.model_dir}")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.processor = Wav2Vec2Processor.from_pretrained(str(self.model_dir))
        self.model = Wav2Vec2ForCTC.from_pretrained(str(self.model_dir)).to(self.device)

    def _load_audio_as_array(self, input_path: str) -> np.ndarray:
        """Loads audio from any supported format and returns float32 numpy array."""
        ext = Path(input_path).suffix.lower().replace('.', '')
        if ext not in self.SUPPORTED_INPUT_FORMATS:
            raise ValueError(
                f"Unsupported file format '{ext}'. Supported formats: {self.SUPPORTED_INPUT_FORMATS}"
            )

        audio = AudioSegment.from_file(input_path, format=ext)
        audio = audio.set_frame_rate(16000).set_channels(1)

        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        samples /= np.iinfo(audio.array_type).max  # normalize to [-1, 1]
        return samples

    def transcribe(self, audio_file: str) -> str:
        """Transcribe audio using Wav2Vec2."""
        try:
            logger.info(f"🔊 Transcribing with Wav2Vec2: {audio_file}")
            speech_array = self._load_audio_as_array(audio_file)

            inputs = self.processor(
                speech_array,
                sampling_rate=16000,
                return_tensors="pt",
                padding=True
            ).input_values.to(self.device)

            with torch.no_grad():
                logits = self.model(inputs).logits

            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]

            logger.info(f"📝 Transcription complete for: {audio_file}")
            return transcription.strip()

        except Exception as e:
            logger.exception(f"❌ Wav2Vec2 transcription failed for {audio_file}")
            return f"Wav2Vec2 error: {e}"
