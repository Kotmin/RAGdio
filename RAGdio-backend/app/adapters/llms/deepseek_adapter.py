
from typing import List
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from langchain.schema import Document
from app.adapters.llms.base import ChatModelAdapter
from app.core.logging_config import logger
from app.core.config import Config


class DeepSeekChatAdapter(ChatModelAdapter):
    def __init__(self):
        model_name = "deepseek-ai/deepseek-llm-7b-chat"

        logger.info(f"📦 Loading DeepSeek model: {model_name}")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

        self.pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

    def ask(self, query: str, context_docs: List[Document]) -> str:
        rag_mode = Config.LLM_RAG_MODE
        context = "\n".join(doc.page_content for doc in context_docs)

        if rag_mode == "rag_strict":
            prompt = query
        elif rag_mode == "rag_fallback":
            prompt = (
                f"Context:\n{context}\n\nQuestion: {query}\n\n"
                "If the documents are not helpful, answer based on your own knowledge."
            )
        else:
            prompt = f"Context:\n{context}\n\nQuestion: {query}"

        logger.info("🧠 Running DeepSeek inference...")
        outputs = self.pipeline(prompt, max_new_tokens=512, do_sample=True, temperature=0.7)
        return outputs[0]["generated_text"].replace(prompt, "").strip()