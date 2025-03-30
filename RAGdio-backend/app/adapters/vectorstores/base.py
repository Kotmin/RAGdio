from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document


class VectorStoreAdapter(ABC):
    @abstractmethod
    def add_documents(self, docs: List[Document]) -> None:
        """Add documents to the vector store."""

    @abstractmethod
    def as_retriever(self):
        """Return retriever instance (Langchain compatible)."""
