from abc import ABC, abstractmethod
from langchain.embeddings.base import Embeddings


class EmbeddingAdapter(ABC):
    @abstractmethod
    def get_embedder(self) -> Embeddings:
        """Return a Langchain-compatible embedder."""
        pass
