from langchain.schema import Document
from typing import List


def transcript_to_documents(text: str, metadata: dict = None) -> List[Document]:
    if not text.strip():
        return []
    return [Document(page_content=text.strip(), metadata=metadata or {})]
