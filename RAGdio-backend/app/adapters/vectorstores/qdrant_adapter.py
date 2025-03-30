from langchain.vectorstores import Qdrant
from langchain.embeddings.base import Embeddings
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain.schema import Document
from .base import VectorStoreAdapter
from typing import List
import os


class QdrantVectorStoreAdapter(VectorStoreAdapter):
    def __init__(self, embedding_model: Embeddings, collection_name="rag_audio_collection"):
        self.collection_name = collection_name
        self.client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
        )

        self.embedding_model = embedding_model

        existing_collections = self.client.get_collections().collections
        if self.collection_name not in [c.name for c in existing_collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

        self.db = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model,
        )

    def add_documents(self, docs: List[Document]) -> None:
        self.db.add_documents(docs)

    def as_retriever(self):
        return self.db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
