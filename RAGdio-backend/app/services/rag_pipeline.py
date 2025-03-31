from app.services.embedding_factory import EmbeddingAdapterFactory
from app.services.vectorstore_factory import VectorStoreFactory
from app.services.llm_factory import get_chat_model
from langchain.schema import Document

class RAGPipelineService:
    def __init__(self):
        self.embedder = EmbeddingAdapterFactory.get_adapter()
        self.vectorstore = VectorStoreFactory.get_vector_store(self.embedder)
        self.llm = get_chat_model()

    def ingest_text(self, text: str, metadata: dict = None):
        doc = Document(page_content=text, metadata=metadata or {})
        self.vectorstore.add_documents([doc])

    def query(self, user_input: str) -> dict:
        retriever = self.vectorstore.as_retriever()
        docs = retriever.get_relevant_documents(user_input)
        answer = self.llm.ask(user_input, docs)
        return {
            "answer": answer,
            "context_docs": [d.page_content for d in docs]
        }
