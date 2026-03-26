from fastapi import APIRouter, HTTPException
from models import UserSettings
from db import upsert_settings, get_settings

router = APIRouter()


@router.post("/settings")
async def save_settings(settings: UserSettings):
    upsert_settings(settings.user_name, settings.model_dump(exclude={"user_name"}))
    return {"status": "saved"}


@router.get("/settings/{user_name}")
async def read_settings(user_name: str):
    data = get_settings(user_name)
    if not data:
        raise HTTPException(status_code=404, detail="User settings not found")

    # Mask API keys before returning
    result = {
        "user_name": data["user_name"],
        "llm_provider": data["llm_provider"],
        "llm_model": data["llm_model"],
        "has_llm_key": bool(data.get("llm_api_key")),
        "has_tavily_key": bool(data.get("tavily_api_key")),
    }
    return result
