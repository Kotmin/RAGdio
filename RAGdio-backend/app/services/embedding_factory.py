from app.adapters.embeddings.base import EmbeddingAdapter
from app.adapters.embeddings.huggingface_adapter import HuggingFaceEmbeddingAdapter
from app.adapters.embeddings.openai_adapter import OpenAIEmbeddingAdapter
from app.core.config import Config


class EmbeddingAdapterFactory:
    @staticmethod
    def get_adapter() -> EmbeddingAdapter:
        backend = Config.EMBEDDING_BACKEND.lower()

        if backend == "huggingface":
            return HuggingFaceEmbeddingAdapter()
        elif backend == "openai":
            return OpenAIEmbeddingAdapter()
        else:
            raise ValueError(f"Unsupported embedding backend: {backend}")
