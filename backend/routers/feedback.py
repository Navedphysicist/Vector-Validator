from fastapi import APIRouter, HTTPException
from models import FeedbackRequest
from db import insert_feedback, get_feedback

router = APIRouter()


@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    data = req.model_dump()
    row = insert_feedback(data)
    return {"status": "saved", "id": str(row["id"])}


@router.get("/feedback")
async def read_feedback(limit: int = 100):
    rows = get_feedback(limit)
    # Convert UUID and datetime to strings for JSON serialization
    for row in rows:
        row["id"] = str(row["id"])
        row["created_at"] = row["created_at"].isoformat()
    return rows
