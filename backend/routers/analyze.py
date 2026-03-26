from fastapi import APIRouter, HTTPException
from models import AnalyzeRequest, AnalyzeResponse
from db import get_settings
from services.tavily_service import search_company
from services.llm_service import call_llm
from services.prompts import vector_extraction_prompt

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    # Get user's API keys
    settings = get_settings(req.user_name)
    if not settings:
        raise HTTPException(status_code=400, detail="Please configure your API keys in Settings first")

    tavily_key = settings.get("tavily_api_key")
    llm_key = settings.get("llm_api_key")
    provider = settings.get("llm_provider", "openai")
    model = settings.get("llm_model", "gpt-4o")

    if not tavily_key:
        raise HTTPException(status_code=400, detail="Tavily API key not configured")
    if not llm_key:
        raise HTTPException(status_code=400, detail="LLM API key not configured")

    # Search for company info
    tavily_results = await search_company(req.company, tavily_key)

    if not tavily_results:
        raise HTTPException(
            status_code=422,
            detail="No search results found for this company. Please enter vectors manually."
        )

    # Extract vectors via LLM
    prompt = vector_extraction_prompt(req.company, tavily_results)

    try:
        result = call_llm(provider, model, llm_key, prompt)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return AnalyzeResponse(
        business_model=result.get("businessModel", ""),
        industry=result.get("industry", ""),
        transaction_platform=result.get("transactionPlatform", ""),
    )
