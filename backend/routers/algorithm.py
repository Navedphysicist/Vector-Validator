import os
from fastapi import APIRouter, HTTPException
from models import RunAlgorithmRequest, RunAlgorithmResponse
from services.role_families import classify_role, ROLE_FAMILIES
from services.algorithm_service import calculate_priority
from services.llm_service import call_llm
from services.prompts import tier_classification_prompt, role_classification_prompt

router = APIRouter()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")


@router.post("/run-algorithm", response_model=RunAlgorithmResponse)
async def run_algorithm(req: RunAlgorithmRequest):
    if not LLM_API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key not configured on server")

    # Step 1: Classify role → role family
    role_family = classify_role(req.role)

    if not role_family:
        # LLM fallback for ambiguous roles
        try:
            prompt = role_classification_prompt(req.role)
            result = call_llm(LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, prompt)
            family_name = result.get("roleFamily", "")

            # Find matching family
            for f in ROLE_FAMILIES:
                if f["name"] == family_name:
                    role_family = f
                    break

            if not role_family:
                role_family = next(f for f in ROLE_FAMILIES if f["name"] == "Operations / General Mgmt")
        except ValueError:
            role_family = next(f for f in ROLE_FAMILIES if f["name"] == "Operations / General Mgmt")

    # Step 2: Classify tiers via LLM
    try:
        prompt = tier_classification_prompt(req.business_model, req.industry, req.transaction_platform)
        tier_result = call_llm(LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, prompt)
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
        tiers=tiers,
        p1=priority[0],
        p2=priority[1],
        p3=priority[2],
    )
