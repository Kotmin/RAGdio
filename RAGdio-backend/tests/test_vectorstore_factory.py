from unittest.mock import MagicMock, patch
from app.services.vectorstore_factory import VectorStoreFactory



def test_vector_factory_returns_qdrant_adapter(monkeypatch):
    monkeypatch.setenv("VECTOR_BACKEND", "qdrant")

    # Re-import config so it picks up new env (pytest-style dynamic patch)
    from app.core.config import Config
    Config.VECTOR_BACKEND = "qdrant"

    mock_embedder = MagicMock()
    
    with patch("app.services.vectorstore_factory.QdrantVectorStoreAdapter") as MockAdapter:
        instance = MockAdapter.return_value  # The mock adapter instance
        adapter = VectorStoreFactory.get_vector_store(mock_embedder)

        # Ensure constructor was called with embedder
        MockAdapter.assert_called_once_with(mock_embedder)

        # Ensure returned object is the mock instance
        assert adapter == instance

