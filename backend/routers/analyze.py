import os
from fastapi import APIRouter, HTTPException
from models import AnalyzeRequest, AnalyzeResponse
from services.search_coordinator import search_company
from services.llm_service import call_llm
from services.prompts import vector_extraction_prompt

router = APIRouter()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    if not LLM_API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key not configured on server")

    # Search for company info across all enabled data sources
    search_results = await search_company(req.company)

    if not search_results:
        raise HTTPException(
            status_code=422,
            detail="No search results found for this company. Please enter vectors manually."
        )

    # Extract vectors via LLM
    prompt = vector_extraction_prompt(req.company, search_results)

    try:
        result = call_llm(LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, prompt)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return AnalyzeResponse(
        business_model=result.get("businessModel", ""),
        industry=result.get("industry", ""),
        transaction_platform=result.get("transactionPlatform", ""),
    )
