import pytest
from unittest.mock import MagicMock
from app.adapters.local_asr import LocalASRProcessor


@pytest.fixture
def local_asr():
    """Fixture to initialize LocalASRProcessor with a mocked pipeline."""
    processor = LocalASRProcessor()
    processor.pipeline = MagicMock(
        return_value={"text": "Test transcription."})
    return processor


def test_local_asr_transcription(local_asr):
    """Tests if LocalASRProcessor transcribes correctly."""
    result = local_asr.transcribe("fake_audio_path.mp3")
    assert result == "Test transcription.", "Transcription did not match expected output."
