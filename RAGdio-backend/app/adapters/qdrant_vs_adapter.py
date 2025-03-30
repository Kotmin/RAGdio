from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.schema import Document

class HuggingFaceEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        self.embedder = HuggingFaceEmbeddings(model_name=model_name)

    def embed_documents(self, docs: List[Document]) -> List[List[float]]:
        return self.embedder.embed_documents([doc.page_content for doc in docs])


class QdrantVectorStoreAdapter(VectorStoreAdapter):
    def __init__(
        self,
        embedding_adapter: EmbeddingAdapter,
        collection_name: str = "rag_audio_collection",
        host: str = "localhost",
        port: int = 6333,
    ):
        self.collection_name = collection_name
        self.embedding_adapter = embedding_adapter

        self.client = QdrantClient(host=host, port=port)
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

        self.db = Qdrant(
            client=self.client,
            collection_name=collection_name,
            embeddings=self.embedding_adapter.embedder,  # langchain expects this
        )

    def add_documents(self, docs: List[Document]) -> None:
        self.db.add_documents(docs)

    def as_retriever(self):
        return self.db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
