import httpx


async def search_company(company_name: str, api_key: str) -> str:
    """Search for company information using Tavily API. Returns formatted results string."""
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
        return ""

    formatted = []
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        formatted.append(f"Title: {title}\nContent: {content}")

    return "\n\n---\n\n".join(formatted)
