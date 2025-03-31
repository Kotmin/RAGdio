from app.adapters.embeddings.base import EmbeddingAdapter
from langchain.embeddings import HuggingFaceEmbeddings


class HuggingFaceEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name

    def get_embedder(self):
        return HuggingFaceEmbeddings(model_name=self.model_name)
