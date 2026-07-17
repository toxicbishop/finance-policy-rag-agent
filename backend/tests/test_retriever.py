import pytest
from unittest.mock import AsyncMock, patch, MagicMock


from backend.embedder import embed


# --- embedder tests ---

@pytest.mark.asyncio
async def test_embed_returns_vector():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "embedding": {"values": [0.1, 0.2, 0.3]}
    }
    mock_response.raise_for_status = MagicMock()

    with patch("backend.embedder.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            import importlib
            import backend.embedder as embedder_module
            importlib.reload(embedder_module)
            result = await embedder_module.embed("What is the reimbursement limit?")

    assert result == [0.1, 0.2, 0.3]


@pytest.mark.asyncio
async def test_embed_raises_without_api_key():
    with patch.dict("os.environ", {}, clear=True):
        import importlib
        import backend.embedder as embedder_module
        importlib.reload(embedder_module)
        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            await embedder_module.embed("test")


# --- retriever tests ---

@pytest.mark.asyncio
async def test_retrieve_returns_matches():
    mock_embed_vec = [0.1] * 768

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "matches": [
            {
                "id": "finance-policy-chunk-0",
                "score": 0.92,
                "metadata": {
                    "text": "Employees must submit reimbursement within 30 days.",
                    "section": "Reimbursement Policy",
                    "chunkId": "finance-policy-chunk-0"
                }
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("backend.embedder.embed", AsyncMock(return_value=mock_embed_vec)), \
         patch("backend.retriever.httpx.AsyncClient") as mock_client, \
         patch.dict("os.environ", {
             "PINECONE_HOST": "https://test.pinecone.io",
             "PINECONE_API_KEY": "test-key"
         }):
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )
        import importlib
        import backend.retriever as retriever_module
        importlib.reload(retriever_module)
        result = await retriever_module.retrieve("reimbursement deadline")

    assert len(result) == 1
    assert result[0]["metadata"]["section"] == "Reimbursement Policy"
    assert result[0]["score"] == 0.92


@pytest.mark.asyncio
async def test_retrieve_raises_without_env_vars():
    with patch.dict("os.environ", {}, clear=True):
        import importlib
        import backend.retriever as retriever_module
        importlib.reload(retriever_module)
        with pytest.raises(ValueError, match="PINECONE_HOST"):
            await retriever_module.retrieve("test question")


@pytest.mark.asyncio
async def test_retrieve_empty_matches():
    mock_response = MagicMock()
    mock_response.json.return_value = {"matches": []}
    mock_response.raise_for_status = MagicMock()

    with patch("backend.embedder.embed", AsyncMock(return_value=[0.0] * 768)), \
         patch("backend.retriever.httpx.AsyncClient") as mock_client, \
         patch.dict("os.environ", {
             "PINECONE_HOST": "https://test.pinecone.io",
             "PINECONE_API_KEY": "test-key"
         }):
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )
        import importlib
        import backend.retriever as retriever_module
        importlib.reload(retriever_module)
        result = await retriever_module.retrieve("something obscure")

    assert result == []
