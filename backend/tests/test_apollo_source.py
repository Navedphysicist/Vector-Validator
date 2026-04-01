import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.data_sources.apollo_source import (
    SOURCE_NAME,
    ENV_KEY,
    ENV_ENABLED,
    search_company,
)


def test_source_constants():
    assert SOURCE_NAME == "Apollo"
    assert ENV_KEY == "APOLLO_API_KEY"
    assert ENV_ENABLED == "APOLLO_ENABLED"


def _make_mock_client(search_response, enrich_response):
    """Helper to create a mock httpx client with search (POST) and enrich (GET) responses."""
    mock_client = AsyncMock()

    mock_search = MagicMock()
    mock_search.json.return_value = search_response
    mock_search.raise_for_status = MagicMock()
    mock_client.post.return_value = mock_search

    mock_enrich = MagicMock()
    mock_enrich.json.return_value = enrich_response
    mock_enrich.raise_for_status = MagicMock()
    mock_client.get.return_value = mock_enrich

    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    return mock_client


@pytest.mark.asyncio
async def test_search_company_returns_formatted_profile():
    search_resp = {
        "organizations": [{"primary_domain": "myollie.com"}]
    }
    enrich_resp = {
        "organization": {
            "name": "Ollie Pets",
            "industry": "Consumer Goods",
            "subindustry": "Pet Food",
            "short_description": "Ollie is a DTC dog food company delivering freshly-cooked meals.",
            "keywords": ["subscription", "pet food", "DTC", "e-commerce"],
            "technology_names": ["Shopify", "Stripe", "React"],
            "estimated_num_employees": 150,
            "annual_revenue_printed": "$50M",
            "website_url": "https://www.myollie.com",
        }
    }
    mock_client = _make_mock_client(search_resp, enrich_resp)

    with patch("services.data_sources.apollo_source.httpx.AsyncClient", return_value=mock_client):
        results = await search_company("Ollie Pets", "fake-apollo-key")

    assert len(results) == 1
    result = results[0]
    assert result["source"] == "apollo"
    assert "Ollie Pets" in result["title"]
    assert "Consumer Goods" in result["content"]
    assert "Pet Food" in result["content"]
    assert "subscription" in result["content"]
    assert "Shopify" in result["content"]
    # Verify two-step: POST for search, GET for enrich
    mock_client.post.assert_called_once()
    mock_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_search_company_returns_empty_on_no_search_results():
    search_resp = {"organizations": []}
    enrich_resp = {}  # should not be called
    mock_client = _make_mock_client(search_resp, enrich_resp)

    with patch("services.data_sources.apollo_source.httpx.AsyncClient", return_value=mock_client):
        results = await search_company("Nonexistent Corp", "fake-apollo-key")

    assert results == []
    mock_client.post.assert_called_once()
    mock_client.get.assert_not_called()  # enrich should not be called


@pytest.mark.asyncio
async def test_search_company_returns_empty_on_no_domain():
    search_resp = {"organizations": [{"primary_domain": None}]}
    enrich_resp = {}
    mock_client = _make_mock_client(search_resp, enrich_resp)

    with patch("services.data_sources.apollo_source.httpx.AsyncClient", return_value=mock_client):
        results = await search_company("No Domain Co", "fake-apollo-key")

    assert results == []
    mock_client.get.assert_not_called()


@pytest.mark.asyncio
async def test_search_company_handles_partial_data():
    """Apollo may return an org with only some fields populated."""
    search_resp = {"organizations": [{"primary_domain": "tinystartup.com"}]}
    enrich_resp = {
        "organization": {
            "name": "Tiny Startup",
            "industry": "Technology",
            "subindustry": None,
            "short_description": None,
            "keywords": None,
            "technology_names": None,
            "estimated_num_employees": None,
            "annual_revenue_printed": None,
            "website_url": None,
        }
    }
    mock_client = _make_mock_client(search_resp, enrich_resp)

    with patch("services.data_sources.apollo_source.httpx.AsyncClient", return_value=mock_client):
        results = await search_company("Tiny Startup", "fake-apollo-key")

    assert len(results) == 1
    assert "Technology" in results[0]["content"]
