from fastapi import APIRouter, HTTPException
from models import RunAlgorithmRequest, RunAlgorithmResponse
from db import get_settings
from services.role_families import classify_role, ROLE_FAMILIES
from services.algorithm_service import calculate_priority
from services.llm_service import call_llm
from services.prompts import tier_classification_prompt, role_classification_prompt

router = APIRouter()


@router.post("/run-algorithm", response_model=RunAlgorithmResponse)
async def run_algorithm(req: RunAlgorithmRequest):
    # Get user's API keys
    settings = get_settings(req.user_name)
    if not settings:
        raise HTTPException(status_code=400, detail="Please configure your API keys in Settings first")

    llm_key = settings.get("llm_api_key")
    provider = settings.get("llm_provider", "openai")
    model = settings.get("llm_model", "gpt-4o")

    if not llm_key:
        raise HTTPException(status_code=400, detail="LLM API key not configured")

    # Step 1: Classify role → role family
    role_family = classify_role(req.role)

    if not role_family:
        # LLM fallback for ambiguous roles
        try:
            prompt = role_classification_prompt(req.role)
            result = call_llm(provider, model, llm_key, prompt)
            family_name = result.get("roleFamily", "")

            # Find matching family
            for f in ROLE_FAMILIES:
                if f["name"] == family_name:
                    role_family = f
                    break

            if not role_family:
                # Default to Operations / General Mgmt
                role_family = next(f for f in ROLE_FAMILIES if f["name"] == "Operations / General Mgmt")
        except ValueError:
            role_family = next(f for f in ROLE_FAMILIES if f["name"] == "Operations / General Mgmt")

    # Step 2: Classify tiers via LLM
    try:
        prompt = tier_classification_prompt(req.business_model, req.industry, req.transaction_platform)
        tier_result = call_llm(provider, model, llm_key, prompt)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    tiers = {
        "Model": tier_result.get("businessModel", "Common"),
        "Industry": tier_result.get("industry", "Common"),
        "Platform": tier_result.get("transactionPlatform", "Common"),
    }

    # Step 3: Calculate priority (pure logic, no LLM)
    priority = calculate_priority(role_family, tiers)

    return RunAlgorithmResponse(
        role_family=role_family["name"],
        p1=priority[0],
        p2=priority[1],
        p3=priority[2],
    )
