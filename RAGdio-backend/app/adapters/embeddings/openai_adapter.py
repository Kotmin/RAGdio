from app.adapters.embeddings.base import EmbeddingAdapter
from app.core.config import Config


class OpenAIEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.model_name = model_name

    def get_embedder(self):
        try:
            from langchain_community.embeddings import OpenAIEmbeddings
        except ImportError:
            raise ImportError(
                "OpenAIEmbeddings requires `openai`. Install it with `pip install openai`."
            )
        
        return OpenAIEmbeddings(
            model=self.model_name,
            openai_api_key=Config.OPENAI_API_KEY
        )
