import os
import logging
from services.data_sources import tavily_source, apollo_source
from services.llm_service import call_llm
from services.prompts import domain_extraction_prompt

logger = logging.getLogger(__name__)


async def search_company(company_name: str) -> str:
    """
    1. Run Tavily to get web results
    2. Use LLM to extract company domain from Tavily results
    3. If Apollo is enabled, enrich using that domain
    4. Merge both, deduplicate, and format for LLM
    """
    all_results = []
    tavily_formatted = ""

    # Step 1: Tavily search
    tavily_enabled = os.getenv(tavily_source.ENV_ENABLED, "false").lower() == "true"
    tavily_key = os.getenv(tavily_source.ENV_KEY, "")

    if tavily_enabled and tavily_key:
        try:
            tavily_results = await tavily_source.search_company(company_name, tavily_key)
            all_results.extend(tavily_results)
            tavily_formatted = _format_results(tavily_results)
        except Exception as e:
            logger.warning(f"Tavily search failed: {e}")

    # Step 2: LLM extracts domain from Tavily results, then Apollo enriches
    apollo_enabled = os.getenv(apollo_source.ENV_ENABLED, "false").lower() == "true"
    apollo_key = os.getenv(apollo_source.ENV_KEY, "")

    if apollo_enabled and apollo_key and tavily_formatted:
        domain = _extract_domain_via_llm(company_name, tavily_formatted)
        if domain:
            logger.info(f"LLM extracted domain for '{company_name}': {domain}")
            try:
                apollo_results = await apollo_source.enrich_by_domain(domain, apollo_key)
                all_results.extend(apollo_results)
            except Exception as e:
                logger.warning(f"Apollo enrich failed: {e}")

    deduped = _deduplicate(all_results)
    return _format_results(deduped)


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


def _deduplicate(results: list[dict]) -> list[dict]:
    """Remove results with duplicate titles. First occurrence wins."""
    seen_titles = set()
    deduped = []
    for r in results:
        title = r.get("title", "")
        if title not in seen_titles:
            seen_titles.add(title)
            deduped.append(r)
    return deduped


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
