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
            temperature=0.2,
            openai_api_key=Config.OPENAI_API_KEY,
            model_name="gpt-4"
        )
        self.chain = load_qa_with_sources_chain(self.llm, chain_type="stuff")

    
    def ask(self, query: str, context_docs: List[Document]) -> str:
        if not context_docs:
            logger.info("No context docs provided. Using raw LLM without RAG.")
            return self.llm.invoke(query).content
        
        for doc in context_docs:
            if "source" not in doc.metadata:
                doc.metadata["source"] = doc.metadata.get("filename", "Unknown Source")

        result = self.chain.invoke({
            "input_documents": context_docs,
            "question": query,
        })
        return result.get("answer", "No answer.")

