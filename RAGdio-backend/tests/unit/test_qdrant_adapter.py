from unittest.mock import patch, MagicMock
from app.adapters.vectorstores.qdrant_adapter import QdrantVectorStoreAdapter
from langchain.schema import Document


@patch("app.adapters.vectorstores.qdrant_adapter.Qdrant")
@patch("app.adapters.vectorstores.qdrant_adapter.QdrantClient")
def test_add_documents(mock_qdrant_client_class, mock_qdrant_class):
    mock_qdrant_client = MagicMock()
    mock_qdrant_client.get_collections.return_value.collections = []
    mock_qdrant_client_class.return_value = mock_qdrant_client

    mock_embedder = MagicMock()
    mock_embedder.embed_documents.return_value = [[0.1] * 768]

    mock_qdrant = MagicMock()
    mock_qdrant_class.return_value = mock_qdrant

    adapter = QdrantVectorStoreAdapter(mock_embedder)
    doc = Document(page_content="Hello test doc")

    adapter.add_documents([doc])
    mock_qdrant.add_documents.assert_called_once()
