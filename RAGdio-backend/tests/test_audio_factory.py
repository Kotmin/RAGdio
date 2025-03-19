import pytest
from app.services.audio_factory import AudioProcessorFactory
from app.adapters.whisper_api import WhisperAPIAudioProcessor
from app.adapters.local_asr import LocalASRProcessor
from app.core.config import Config


def test_factory_creates_whisper_api(mocker):
    """Tests if the factory correctly selects Whisper API processor."""
    mocker.patch.object(Config, "ASR_MODEL", "whisper_api")
    processor = AudioProcessorFactory.get_audio_processor()
    assert isinstance(
        processor, WhisperAPIAudioProcessor), "Factory did not return Whisper API processor."


def test_factory_creates_local_asr(mocker):
    """Tests if the factory correctly selects Local ASR processor."""
    mocker.patch.object(Config, "ASR_MODEL", "local")
    processor = AudioProcessorFactory.get_audio_processor()
    assert isinstance(
        processor, LocalASRProcessor), "Factory did not return Local ASR processor."


def test_factory_invalid_model(mocker):
    """Tests if the factory raises an error for an unsupported ASR model."""
    mocker.patch.object(Config, "ASR_MODEL", "invalid_model")
    with pytest.raises(ValueError, match="Unsupported ASR model"):
        AudioProcessorFactory.get_audio_processor()
