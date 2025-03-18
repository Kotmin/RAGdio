from langchain.schema import Document
from langchain.llms import OpenAIWhisper
from app.services.audio_processor import AudioProcessor

class LangChainAudioProcessor(AudioProcessor):
    """LangChain-powered ASR adapter, using OpenAI Whisper."""

    def __init__(self, model_size: str = "base"):
        """Initialize LangChain Whisper model."""
        self.model = OpenAIWhisper(model_name=model_size)

    def transcribe(self, audio_file: str) -> str:
        """Transcribes audio via LangChain model."""
        doc = Document(page_content="")
        transcription = self.model.transcribe(audio_file, doc)
        return transcription.page_content
