
from langchain.embeddings.base import Embeddings

from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.exceptions import UnexpectedResponse

from langchain.schema import Document
from .base import VectorStoreAdapter
from typing import List
import os

import logging
from app.core.config import Config

from app.core.logging_config import logger

class QdrantVectorStoreAdapter(VectorStoreAdapter):
    def __init__(self, embedding_model: Embeddings, collection_name="rag_audio_collection"):
        self.collection_name = collection_name
        self.embedding_model = embedding_model

        # self.client = QdrantClient(
        #     host=Config.QDRANT_HOST,
        #     port=int(Config.QDRANT_PORT),
        # )
        
        self.client = QdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
        )

        # Determine embedding size dynamically
        try:
            dummy_vector = self.embedding_model.embed_query("test")
            embedding_dim = len(dummy_vector)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to determine embedding size: {e}")

        # Check existing collection (if exists)
        try:
            info = self.client.get_collection(self.collection_name)
            # logging.warning(f"⚠️ Could not determine existing vector size for collection '{info}'")
            # existing_dim = info.vectors_size
            # existing_dim = info.config.params.size
            existing_dim = info.config.params.vectors.size


            if existing_dim != embedding_dim:
                msg = (
                    f"❌ Vector dim mismatch in Qdrant collection '{self.collection_name}': "
                    f"expected {existing_dim}, got {embedding_dim} from embedder"
                )
                if Config.DEBUG:
                    raise ValueError(msg)
                else:
                    logger.warning(msg)
                    logger.warning("⚠️ Recreating collection with new embedding size")

                    self.client.recreate_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
                    )
        # except Exception:
        #     if Config.DEBUG:
        #         logging.info(f"🆕 Creating Qdrant collection '{self.collection_name}' with dim {embedding_dim}")
        #     self.client.recreate_collection(
        #         collection_name=self.collection_name,
        #         vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
        #     )
        except UnexpectedResponse as e:
            logger.warning(f"Collection '{self.collection_name}' does not exist, creating it.")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
            )

        
        self.db = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedding_model,
        )

    def add_documents(self, docs: List[Document]) -> None:
        try:
            self.db.add_documents(docs)
        except Exception as e:
            logger.error(f"❌ Failed to add documents to Qdrant: {e}")
            if Config.DEBUG:
                raise

    def as_retriever(self):
        return self.db.as_retriever(search_type="mmr", search_kwargs={"k": 3})