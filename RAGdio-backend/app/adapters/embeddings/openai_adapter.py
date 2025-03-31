from app.adapters.embeddings.base import EmbeddingAdapter
from langchain.embeddings import OpenAIEmbeddings
from app.core.config import Config


class OpenAIEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.model_name = model_name

    def get_embedder(self):
        return OpenAIEmbeddings(
            model=self.model_name,
            openai_api_key=Config.OPENAI_API_KEY
        )
