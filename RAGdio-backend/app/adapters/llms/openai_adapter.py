from typing import List
# from langchain_community.chat_models.openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from .base import ChatModelAdapter
from app.core.config import Config

from app.core.logging_config import logger

class OpenAIChatAdapter(ChatModelAdapter):
    def __init__(self):
        self.llm = ChatOpenAI(
            # temperature=0.2,
            openai_api_key=Config.OPENAI_API_KEY,
            # model_name="gpt-4",
            model_name="o3-mini",
        )
        self.chain = load_qa_with_sources_chain(self.llm, chain_type="stuff")

    
    def ask(self, query: str, context_docs: List[Document]) -> str:
        rag_mode = Config.LLM_RAG_MODE

        if not context_docs:
            logger.info("No context docs provided. Using raw LLM without RAG.")
            return self.llm.invoke(query).content

        # If fallback mode is enabled, append prompt hint
        if rag_mode == "rag_fallback":
            query += "\n\nIf the documents are not helpful, you may still answer based on your own knowledge."

        for doc in context_docs:
            if "source" not in doc.metadata:
                doc.metadata["source"] = doc.metadata.get("filename", "Unknown Source")

        try:
            result = self.chain.invoke({
                "input_documents": context_docs,
                "question": query,
            })

            logger.debug(f"QA Chain result: {result}")

            return result.get("answer") or result.get("output_text") or "No answer."

        except Exception as e:
            logger.exception("Error during OpenAI QA chain invocation")
            return "⚠️ Failed to get an answer from the model."


