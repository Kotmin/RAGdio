from app.core.config import Config
from app.adapters.vectorstores.qdrant_adapter import QdrantVectorStoreAdapter
# from app.adapters.vectorstores.chroma_adapter import ChromaVectorStoreAdapter
from langchain.embeddings.base import Embeddings

from app.services.embedding_factory import EmbeddingAdapterFactory


class VectorStoreFactory:
    """Factory to create vector store adapters dynamically."""

    @staticmethod
    def get_vector_store(embedder: Embeddings):
        backend = Config.VECTOR_BACKEND.lower()
        embedder = EmbeddingAdapterFactory.get_adapter().get_embedder()

        if backend == "qdrant":
            return QdrantVectorStoreAdapter(embedder)
        # elif backend == "chroma":
        #     return ChromaVectorStoreAdapter(embedder)
        else:
            raise ValueError(f"Unsupported vector store backend: {backend}")
