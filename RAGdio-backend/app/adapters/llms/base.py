# app/adapters/llms/base.py

from abc import ABC, abstractmethod
from typing import List
from langchain.schema import Document

class ChatModelAdapter(ABC):
    @abstractmethod
    def ask(self, query: str, context_docs: List[Document]) -> str:
        """Generate answer given user query and context documents."""
        pass
