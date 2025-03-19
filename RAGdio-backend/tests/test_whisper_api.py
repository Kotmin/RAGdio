import pytest
from unittest.mock import MagicMock, patch
from app.adapters.whisper_api import WhisperAPIAudioProcessor


@pytest.fixture
def whisper_api():
    """Fixture to initialize Whisper API processor with a mocked OpenAI client."""
    processor = WhisperAPIAudioProcessor()
    processor.client.audio.transcriptions.create = MagicMock(
        return_value=MagicMock(text="Whisper test transcription."))
    return processor


def test_whisper_api_transcription(whisper_api):
    """Tests if WhisperAPIAudioProcessor correctly transcribes audio."""
    result = whisper_api.transcribe("fake_audio.mp3")
    assert result == "Whisper test transcription.", "Whisper API transcription failed."


def test_whisper_api_large_file_handling(mocker):
    """Tests handling of files larger than 25MB (Mock File Size)."""
    mocker.patch("os.path.getsize", return_value=30 *
                 1024 * 1024)  # Mock file size: 30MB
    whisper_api = WhisperAPIAudioProcessor()
    with patch.object(whisper_api, "_split_audio", return_value=["chunk1.mp3", "chunk2.mp3"]):
        transcription = whisper_api.transcribe("large_file.mp3")
        assert "Whisper test transcription." in transcription, "Failed to transcribe large file chunks."
