import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.data_sources.tavily_source import (
    SOURCE_NAME,
    ENV_KEY,
    ENV_ENABLED,
    search_company,
)


def test_source_constants():
    assert SOURCE_NAME == "Tavily"
    assert ENV_KEY == "TAVILY_API_KEY"
    assert ENV_ENABLED == "TAVILY_ENABLED"


@pytest.mark.asyncio
async def test_search_company_returns_list_of_dicts():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {"title": "About Acme Corp", "content": "Acme is a SaaS company..."},
            {"title": "Acme Corp Overview", "content": "Acme provides cloud solutions..."},
        ]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("services.data_sources.tavily_source.httpx.AsyncClient", return_value=mock_client):
        results = await search_company("Acme Corp", "fake-key")

    assert len(results) == 2
    assert results[0]["title"] == "About Acme Corp"
    assert results[0]["content"] == "Acme is a SaaS company..."
    assert results[0]["source"] == "tavily"
    assert results[1]["source"] == "tavily"


@pytest.mark.asyncio
async def test_search_company_returns_empty_list_on_no_results():
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("services.data_sources.tavily_source.httpx.AsyncClient", return_value=mock_client):
        results = await search_company("Unknown Co", "fake-key")

    assert results == []
