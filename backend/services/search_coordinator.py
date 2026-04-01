import os
import logging
from services.data_sources import tavily_source, apollo_source
from services.llm_service import call_llm
from services.prompts import domain_extraction_prompt

logger = logging.getLogger(__name__)


async def search_company(company_name: str) -> str:
    """
    Apollo-first sequential fallback:
    1. Apollo name search → domain
    2. If no domain: Tavily web search → LLM extracts domain
    3. If domain found: Apollo enrich → return Apollo data only
    4. If no Apollo data: return Tavily web search results as fallback
    """
    apollo_enabled = os.getenv(apollo_source.ENV_ENABLED, "false").lower() == "true"
    apollo_key = os.getenv(apollo_source.ENV_KEY, "")
    tavily_enabled = os.getenv(tavily_source.ENV_ENABLED, "false").lower() == "true"
    tavily_key = os.getenv(tavily_source.ENV_KEY, "")

    domain = None
    tavily_results = None  # cached so we don't call Tavily twice

    # Level 1: Apollo name search for domain
    if apollo_enabled and apollo_key:
        try:
            domain = await apollo_source.search_domain(company_name, apollo_key)
        except Exception as e:
            logger.warning(f"Apollo domain search failed: {e}")

    # Level 2: Tavily + LLM for domain (only if Level 1 failed)
    if not domain and tavily_enabled and tavily_key:
        try:
            tavily_results = await tavily_source.search_company(company_name, tavily_key)
            if tavily_results:
                tavily_formatted = _format_results(tavily_results)
                domain = _extract_domain_via_llm(company_name, tavily_formatted)
        except Exception as e:
            logger.warning(f"Tavily domain lookup failed: {e}")

    # Level 3: Apollo enrich with domain
    if domain and apollo_enabled and apollo_key:
        try:
            apollo_results = await apollo_source.enrich_by_domain(domain, apollo_key)
            if apollo_results:
                logger.info(f"Using Apollo data for '{company_name}' (domain: {domain})")
                return _format_results(apollo_results)
        except Exception as e:
            logger.warning(f"Apollo enrich failed: {e}")

    # Level 4: Fallback to Tavily web search results
    if tavily_results:
        logger.info(f"Falling back to Tavily results for '{company_name}'")
        return _format_results(tavily_results)

    # Tavily not yet fetched — fetch now as last resort
    if tavily_enabled and tavily_key:
        try:
            tavily_results = await tavily_source.search_company(company_name, tavily_key)
            if tavily_results:
                logger.info(f"Falling back to Tavily results for '{company_name}'")
                return _format_results(tavily_results)
        except Exception as e:
            logger.warning(f"Tavily fallback failed: {e}")

    return ""


def _extract_domain_via_llm(company_name: str, search_results: str) -> str | None:
    """Use LLM to extract the company's website domain from search results."""
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-4o")
    api_key = os.getenv("LLM_API_KEY", "")

    if not api_key:
        return None

    try:
        prompt = domain_extraction_prompt(company_name, search_results)
        result = call_llm(provider, model, api_key, prompt)
        domain = result.get("domain", "")
        if domain and domain != "unknown":
            return domain
    except Exception as e:
        logger.warning(f"LLM domain extraction failed: {e}")

    return None


def _format_results(results: list[dict]) -> str:
    """Format results into the string format expected by the LLM prompt."""
    if not results:
        return ""

    formatted = []
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        formatted.append(f"Title: {title}\nContent: {content}")

    return "\n\n---\n\n".join(formatted)
