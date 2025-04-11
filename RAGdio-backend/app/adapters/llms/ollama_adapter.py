import requests
from typing import List
from langchain.schema import Document
from app.adapters.llms.base import ChatModelAdapter
from app.core.config import Config
from app.core.logging_config import logger


class OllamaChatAdapter(ChatModelAdapter):
    def __init__(self):
        self.model = Config.LOCAL_OLLM_MODEL or "zephyr"
        self.url = Config.LOCAL_OLLM_API_URL or "http://ollama:11434/api/generate"

    def ask(self, query: str, context_docs: List[Document]) -> str:
        rag_mode = Config.LLM_RAG_MODE
        context = "\n".join(doc.page_content for doc in context_docs)

        if not context_docs:
            prompt = query
        elif rag_mode == "rag_fallback":
            prompt = (
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                "If the documents are not helpful, you may still answer based on your own knowledge."
            )
        elif rag_mode == "rag_strict":
            prompt = f"Answer the question strictly based on this context:\n\n{context}\n\nQuestion: {query}"
        else:
            prompt = f"{context}\n\nQuestion: {query}"

        try:
            logger.info(f"🦙 Calling Ollama model '{self.model}' at {self.url}")
            response = requests.post(
                self.url,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=360
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "⚠️ No answer received.")
        except Exception as e:
            logger.exception("❌ Ollama call failed")
            return f"⚠️ Failed to query local LLM: {e}"
