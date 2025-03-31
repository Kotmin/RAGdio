from app.adapters.embeddings.base import EmbeddingAdapter



class HuggingFaceEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name

    def get_embedder(self):
        try:
            from langchain.embeddings import HuggingFaceEmbeddings
        except ImportError:
            raise ImportError(
                "HuggingFaceEmbeddings requires `sentence-transformers`. "
                "Install it with `pip install sentence-transformers`."
            )
        return HuggingFaceEmbeddings(model_name=self.model_name)


