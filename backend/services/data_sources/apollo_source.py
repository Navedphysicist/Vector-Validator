import httpx
import logging

SOURCE_NAME = "Apollo"
ENV_KEY = "APOLLO_API_KEY"
ENV_ENABLED = "APOLLO_ENABLED"

SEARCH_URL = "https://api.apollo.io/api/v1/mixed_companies/search"
ENRICH_URL = "https://api.apollo.io/api/v1/organizations/enrich"

logger = logging.getLogger(__name__)


async def search_domain(company_name: str, api_key: str) -> str | None:
    """Search Apollo for a company by name, return primary domain if found."""
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": api_key,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(SEARCH_URL, headers=headers, json={
            "q_organization_name": company_name,
            "page": 1,
            "per_page": 1,
        })
        response.raise_for_status()
        orgs = response.json().get("organizations", [])

    if not orgs:
        logger.info(f"Apollo search: no organization found for '{company_name}'")
        return None

    domain = orgs[0].get("primary_domain")
    if not domain:
        logger.info(f"Apollo search: no domain found for '{company_name}'")
        return None

    logger.info(f"Apollo search: found domain '{domain}' for '{company_name}'")
    return domain


async def enrich_by_domain(domain: str, api_key: str) -> list[dict]:
    """Enrich company data using Apollo.io API with a known domain."""
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": api_key,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(ENRICH_URL, headers=headers, params={"domain": domain})
        response.raise_for_status()
        data = response.json()

    org = data.get("organization")
    if not org:
        return []

    content = _format_org(org)
    name = org.get("name", domain)

    return [
        {
            "title": f"Apollo.io Company Profile - {name}",
            "content": content,
            "source": "apollo",
        }
    ]


def _format_org(org: dict) -> str:
    """Format Apollo org data into a natural language block for LLM consumption."""
    parts = []

    industry = org.get("industry")
    subindustry = org.get("subindustry")
    if industry:
        ind_str = f"Industry: {industry}"
        if subindustry:
            ind_str += f". Sub-industry: {subindustry}"
        parts.append(ind_str)

    description = org.get("short_description")
    if description:
        parts.append(f"Description: {description}")

    keywords = org.get("keywords")
    if keywords and isinstance(keywords, list):
        parts.append(f"Keywords: {', '.join(keywords)}")

    tech = org.get("technology_names")
    if tech and isinstance(tech, list):
        parts.append(f"Technologies: {', '.join(tech)}")

    employees = org.get("estimated_num_employees")
    if employees:
        parts.append(f"Employees: {employees}")

    revenue = org.get("annual_revenue_printed")
    if revenue:
        parts.append(f"Revenue: {revenue}")

    return ". ".join(parts) + "." if parts else ""
