from fastapi import APIRouter, HTTPException, status
from typing import Optional

router = APIRouter(prefix="/api/v1/questions", tags=["questions"])


@router.post("/")
async def submit_question():
    """Submit a question answer"""
    # TODO: Implement question submission
    pass


@router.get("/")
async def get_questions():
    """Get all questions"""
    # TODO: Implement getting questions
    pass
