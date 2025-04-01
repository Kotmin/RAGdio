from app.services.embedding_factory import EmbeddingAdapterFactory
from app.services.vectorstore_factory import VectorStoreFactory
from app.services.llm_factory import get_chat_model
from app.services.audio_factory import AudioProcessorFactory

from langchain.schema import Document
from pathlib import Path

class RAGPipelineService:
    def __init__(self):
        self.embedder = EmbeddingAdapterFactory.get_adapter()
        self.vectorstore = VectorStoreFactory.get_vector_store(self.embedder)
        self.llm = get_chat_model()
        self.audio_processor = AudioProcessorFactory.get_audio_processor()

    def ingest_text(self, text: str, metadata: dict = None):
        doc = Document(page_content=text, metadata=metadata or {})
        self.vectorstore.add_documents([doc])

    def query(self, user_input: str) -> dict:
        retriever = self.vectorstore.as_retriever()
        docs = retriever.invoke(user_input)
        if not docs:
            return {"answer": "⚠️ No relevant documents found.", "context_docs": []}

        answer = self.llm.ask(user_input, docs)
        return {
            "answer": answer,
            "context_docs": [d.page_content for d in docs]
        }
    
    def transcribe_and_store(self, file_path: str, metadata: dict = None) -> str:
        """Transcribes audio and stores it in the vector store."""
        transcription = self.audio_processor.transcribe(file_path)
        self.ingest_text(transcription, metadata={"filename": Path(file_path).name, **(metadata or {})})
        return transcription
