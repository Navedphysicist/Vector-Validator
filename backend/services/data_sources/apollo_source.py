import httpx
import logging

SOURCE_NAME = "Apollo"
ENV_KEY = "APOLLO_API_KEY"
ENV_ENABLED = "APOLLO_ENABLED"

ENRICH_URL = "https://api.apollo.io/api/v1/organizations/enrich"

logger = logging.getLogger(__name__)


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
