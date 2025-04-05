import os
import tempfile
from pathlib import Path

import torch
import torchaudio
from pydub import AudioSegment
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

from app.core.logging_config import logger
from app.services.audio_processor import AudioProcessor


class Wav2VecASRProcessor(AudioProcessor):
    """
    Offline ASR using Wav2Vec2 (facebook/wav2vec2-large-xlsr-53).
    Handles English, Polish and more via PyDub + Transformers.
    """

    MODEL_NAME = "facebook/wav2vec2-large-xlsr-53"
    SUPPORTED_FORMATS = {"mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"}

    def __init__(self):
        logger.info(f"📥 Loading Wav2Vec2 model: {self.MODEL_NAME}")
        self.processor = Wav2Vec2Processor.from_pretrained(self.MODEL_NAME)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.MODEL_NAME)
        self.model.eval()

    def _convert_to_wav(self, input_path: str) -> str:
        """Converts input audio to 16kHz mono WAV format for Wav2Vec."""
        ext = input_path.split(".")[-1].lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: .{ext}")

        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1).set_frame_rate(16000)

        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio.export(temp_wav.name, format="wav")
        logger.debug(f"Converted '{input_path}' to WAV at {temp_wav.name}")
        return temp_wav.name

    def transcribe(self, audio_file: str, language: str = "en") -> str:
        """Transcribes audio using local Wav2Vec2 model."""
        try:
            wav_path = self._convert_to_wav(audio_file)
            waveform, sample_rate = torchaudio.load(wav_path)

            if sample_rate != 16000:
                raise RuntimeError("Audio sample rate must be 16kHz")

            inputs = self.processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt")
            with torch.no_grad():
                logits = self.model(**inputs).logits

            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]

            logger.info(f"✅ Transcription complete (chars: {len(transcription.strip())})")
            os.remove(wav_path)
            return transcription.strip()

        except Exception as e:
            logger.exception("Wav2Vec2 transcription failed")
            return f"[Wav2Vec2 error] {e}"
