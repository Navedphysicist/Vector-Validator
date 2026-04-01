import httpx

SOURCE_NAME = "Tavily"
ENV_KEY = "TAVILY_API_KEY"
ENV_ENABLED = "TAVILY_ENABLED"


async def search_company(company_name: str, api_key: str) -> list[dict]:
    """Search for company information using Tavily API. Returns list of result dicts."""
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": f"{company_name} company business model industry overview",
        "search_depth": "advanced",
        "max_results": 5,
        "include_raw_content": False,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    results = data.get("results", [])
    if not results:
        return []

    return [
        {
            "title": r.get("title", ""),
            "content": r.get("content", ""),
            "source": "tavily",
        }
        for r in results
    ]
