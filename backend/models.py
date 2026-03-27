from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnalyzeRequest(BaseModel):
    company: str
    role: str
    user_name: str


class AnalyzeResponse(BaseModel):
    business_model: str
    industry: str
    transaction_platform: str


class RunAlgorithmRequest(BaseModel):
    business_model: str
    industry: str
    transaction_platform: str
    role: str
    user_name: str


class RunAlgorithmResponse(BaseModel):
    role_family: str
    tiers: dict[str, str]
    p1: str
    p2: str
    p3: str


class FeedbackRequest(BaseModel):
    company: str
    industry: str
    business_model: str
    transaction_platform: str
    role: str
    role_family: str
    p1: str
    p2: str
    p3: str
    is_correct: bool
    comment: Optional[str] = None
    user_name: str


class FeedbackItem(BaseModel):
    id: str
    company: str
    industry: str
    business_model: str
    transaction_platform: str
    role: str
    role_family: str
    p1: str
    p2: str
    p3: str
    is_correct: bool
    comment: Optional[str]
    user_name: str
    created_at: datetime


class UserSettings(BaseModel):
    user_name: str
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    llm_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
