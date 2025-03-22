from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain.schema import Document
from typing import List
import os

class VectorStoreAdapter:
    def __init__(self):
        self.collection_name = "rag_audio_collection"
        self.qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", 6333))

        self.embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.client = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)

        # Ensure collection exists
        if not self.client.get_collections().collections or self.collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

        self.db = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedder,
        )

    def add_documents(self, docs: List[Document]):
        self.db.add_documents(docs)

    def as_retriever(self):
        return self.db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
