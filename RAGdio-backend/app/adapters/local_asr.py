from langchain.schema import Document
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from app.services.audio_processor import AudioProcessor


class LocalASRProcessor(AudioProcessor):
    """Local ASR using Hugging Face / LangChain."""

    def __init__(self, model_name: str = "openai/whisper-small"):
        """Loads a local ASR model via Hugging Face Transformers."""
        self.model_name = model_name
        self.pipeline = pipeline(
            "automatic-speech-recognition", model=model_name)
        self.llm = HuggingFacePipeline(pipeline=self.pipeline)

    def transcribe(self, audio_file: str) -> str:
        """Transcribes audio using a locally hosted ASR model."""
        try:
            doc = Document(page_content="")
            transcription = self.llm.transcribe(audio_file, doc)
            return transcription.page_content

        except Exception as e:
            return f"Local ASR error: {e}"
