from typing import List
from langchain.schema import Document
from app.adapters.llms.base import ChatModelAdapter
from app.core.logging_config import logger
from app.core.config import Config


class DeepSeekChatAdapter(ChatModelAdapter):
    def __init__(self):
        """Lazy-load transformers and model only when this adapter is instantiated."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            import torch
        except ImportError:
            raise ImportError("❌ transformers and torch are required. Install with `pip install transformers torch`")

        self.model_name = "deepseek-ai/deepseek-llm-7b-chat"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        logger.info(f"📦 Loading DeepSeek model: {self.model_name} on {self.device}")

        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map="auto")

            self.pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=0 if self.device == "cuda" else -1,
            )
        except Exception as e:
            logger.exception("❌ Failed to load DeepSeek model")
            raise RuntimeError(f"Failed to load DeepSeek model: {e}")

    def ask(self, query: str, context_docs: List[Document]) -> str:
        rag_mode = Config.LLM_RAG_MODE
        context = "\n".join(doc.page_content for doc in context_docs)

        if not context_docs:
            prompt = query
        elif rag_mode == "rag_strict":
            prompt = f"Answer the following strictly using the given context:\n\n{context}\n\nQuestion: {query}"
        elif rag_mode == "rag_fallback":
            prompt = (
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                "If the documents are not helpful, you may still answer based on your own knowledge."
            )
        else:
            prompt = f"Context:\n{context}\n\nQuestion: {query}"

        logger.info("🧠 Running DeepSeek inference...")
        try:
            outputs = self.pipeline(
                prompt,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
            )
            result = outputs[0]["generated_text"]
            return result.replace(prompt, "").strip()
        except Exception as e:
            logger.exception("❌ DeepSeek inference failed")
            return f"⚠️ DeepSeek failed: {e}"
