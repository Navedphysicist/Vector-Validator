import pytest
from unittest.mock import AsyncMock, patch
from services.search_coordinator import search_company, _deduplicate, _format_results


def test_deduplicate_removes_exact_title_matches():
    results = [
        {"title": "About Acme", "content": "Content A", "source": "tavily"},
        {"title": "About Acme", "content": "Content B", "source": "apollo"},
        {"title": "Acme Overview", "content": "Content C", "source": "tavily"},
    ]
    deduped = _deduplicate(results)
    assert len(deduped) == 2
    titles = [r["title"] for r in deduped]
    assert "About Acme" in titles
    assert "Acme Overview" in titles


def test_format_results_produces_expected_string():
    results = [
        {"title": "Title One", "content": "Content one here", "source": "tavily"},
        {"title": "Title Two", "content": "Content two here", "source": "apollo"},
    ]
    formatted = _format_results(results)
    assert "Title: Title One" in formatted
    assert "Content: Content one here" in formatted
    assert "Title: Title Two" in formatted
    assert "Content: Content two here" in formatted
    assert "---" in formatted


def test_format_results_empty_list():
    assert _format_results([]) == ""


@pytest.mark.asyncio
async def test_search_company_calls_enabled_sources():
    """When both sources are enabled, both get called and results are merged."""
    tavily_results = [{"title": "Tavily Result", "content": "From web", "source": "tavily"}]
    apollo_results = [{"title": "Apollo Result", "content": "From apollo", "source": "apollo"}]

    mock_tavily = AsyncMock(return_value=tavily_results)
    mock_apollo = AsyncMock(return_value=apollo_results)

    mock_tavily_mod = type("MockModule", (), {
        "SOURCE_NAME": "Tavily",
        "ENV_KEY": "TAVILY_API_KEY",
        "ENV_ENABLED": "TAVILY_ENABLED",
        "search_company": mock_tavily,
    })()
    mock_apollo_mod = type("MockModule", (), {
        "SOURCE_NAME": "Apollo",
        "ENV_KEY": "APOLLO_API_KEY",
        "ENV_ENABLED": "APOLLO_ENABLED",
        "search_company": mock_apollo,
    })()

    env = {
        "TAVILY_ENABLED": "true",
        "TAVILY_API_KEY": "tvly-fake",
        "APOLLO_ENABLED": "true",
        "APOLLO_API_KEY": "ap-fake",
    }

    with patch("services.search_coordinator.SOURCES", [mock_tavily_mod, mock_apollo_mod]):
        with patch.dict("os.environ", env, clear=False):
            result = await search_company("Acme Corp")

    assert "Tavily Result" in result
    assert "Apollo Result" in result
    mock_tavily.assert_called_once_with("Acme Corp", "tvly-fake")
    mock_apollo.assert_called_once_with("Acme Corp", "ap-fake")


@pytest.mark.asyncio
async def test_search_company_skips_disabled_sources():
    """When a source is disabled, it should not be called."""
    tavily_results = [{"title": "Tavily Only", "content": "Web data", "source": "tavily"}]
    mock_tavily = AsyncMock(return_value=tavily_results)
    mock_apollo = AsyncMock(return_value=[])

    mock_tavily_mod = type("MockModule", (), {
        "SOURCE_NAME": "Tavily",
        "ENV_KEY": "TAVILY_API_KEY",
        "ENV_ENABLED": "TAVILY_ENABLED",
        "search_company": mock_tavily,
    })()
    mock_apollo_mod = type("MockModule", (), {
        "SOURCE_NAME": "Apollo",
        "ENV_KEY": "APOLLO_API_KEY",
        "ENV_ENABLED": "APOLLO_ENABLED",
        "search_company": mock_apollo,
    })()

    env = {
        "TAVILY_ENABLED": "true",
        "TAVILY_API_KEY": "tvly-fake",
        "APOLLO_ENABLED": "false",
        "APOLLO_API_KEY": "ap-fake",
    }

    with patch("services.search_coordinator.SOURCES", [mock_tavily_mod, mock_apollo_mod]):
        with patch.dict("os.environ", env, clear=False):
            result = await search_company("Acme Corp")

    assert "Tavily Only" in result
    mock_tavily.assert_called_once()
    mock_apollo.assert_not_called()


@pytest.mark.asyncio
async def test_search_company_skips_source_without_api_key():
    """Source enabled but no API key set — should be skipped."""
    mock_tavily = AsyncMock(return_value=[{"title": "T", "content": "C", "source": "tavily"}])

    mock_tavily_mod = type("MockModule", (), {
        "SOURCE_NAME": "Tavily",
        "ENV_KEY": "TAVILY_API_KEY",
        "ENV_ENABLED": "TAVILY_ENABLED",
        "search_company": mock_tavily,
    })()
    mock_apollo_mod = type("MockModule", (), {
        "SOURCE_NAME": "Apollo",
        "ENV_KEY": "APOLLO_API_KEY",
        "ENV_ENABLED": "APOLLO_ENABLED",
        "search_company": AsyncMock(),
    })()

    env = {
        "TAVILY_ENABLED": "true",
        "TAVILY_API_KEY": "tvly-fake",
        "APOLLO_ENABLED": "true",
        # APOLLO_API_KEY intentionally missing
    }

    with patch("services.search_coordinator.SOURCES", [mock_tavily_mod, mock_apollo_mod]):
        with patch.dict("os.environ", env, clear=True):
            result = await search_company("Acme Corp")

    mock_apollo_mod.search_company.assert_not_called()


@pytest.mark.asyncio
async def test_search_company_handles_source_error_gracefully():
    """If one source throws, the other results still come through."""
    mock_tavily = AsyncMock(side_effect=Exception("Tavily is down"))
    mock_apollo = AsyncMock(return_value=[{"title": "Apollo OK", "content": "Data", "source": "apollo"}])

    mock_tavily_mod = type("MockModule", (), {
        "SOURCE_NAME": "Tavily",
        "ENV_KEY": "TAVILY_API_KEY",
        "ENV_ENABLED": "TAVILY_ENABLED",
        "search_company": mock_tavily,
    })()
    mock_apollo_mod = type("MockModule", (), {
        "SOURCE_NAME": "Apollo",
        "ENV_KEY": "APOLLO_API_KEY",
        "ENV_ENABLED": "APOLLO_ENABLED",
        "search_company": mock_apollo,
    })()

    env = {
        "TAVILY_ENABLED": "true",
        "TAVILY_API_KEY": "tvly-fake",
        "APOLLO_ENABLED": "true",
        "APOLLO_API_KEY": "ap-fake",
    }

    with patch("services.search_coordinator.SOURCES", [mock_tavily_mod, mock_apollo_mod]):
        with patch.dict("os.environ", env, clear=False):
            result = await search_company("Acme Corp")

    assert "Apollo OK" in result


@pytest.mark.asyncio
async def test_search_company_returns_empty_when_all_disabled():
    env = {}  # no sources enabled

    with patch("services.search_coordinator.SOURCES", []):
        with patch.dict("os.environ", env, clear=True):
            result = await search_company("Acme Corp")

    assert result == ""
