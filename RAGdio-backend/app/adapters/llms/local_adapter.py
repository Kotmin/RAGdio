from typing import List
from abc import ABC, abstractmethod
from langchain.schema import Document
from app.adapters.llms.base import ChatModelAdapter
from app.core.config import Config
from app.core.logging_config import logger
import requests


class LocalLLMBaseAdapter(ChatModelAdapter, ABC):
    """Abstract base for simple HTTP-style local models."""

    def __init__(self):
        self.url = self.get_endpoint()

    @abstractmethod
    def get_endpoint(self) -> str:
        """Return model-specific endpoint URL."""
        ...

    def ask(self, query: str, context_docs: List[Document]) -> str:
        rag_mode = Config.LLM_RAG_MODE
        context = "\n".join(doc.page_content for doc in context_docs)

        if rag_mode == "rag_strict":
            full_prompt = query
        elif rag_mode == "rag_fallback":
            full_prompt = (
                f"Context:\n{context}\n\nQuestion: {query}\n\n"
                "If the documents are not helpful, you may still answer based on your own knowledge."
            )
        else: 
            full_prompt = f"Context:\n{context}\n\nQuestion: {query}"

        try:
            logger.info(f"📡 Calling local model at {self.url}")
            res = requests.post(self.url, json={"prompt": full_prompt}, timeout=20)
            res.raise_for_status()
            return res.json().get("response", "⚠️ No answer received.")
        except Exception as e:
            logger.exception("Error in LocalLLMBaseAdapter")
            return f"⚠️ Local model failed: {e}"
