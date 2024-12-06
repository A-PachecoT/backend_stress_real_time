from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.question import QuestionResponse as QuestionResponseModel
from app.schemas.question import QuestionResponse, QuestionResponseCreate, PSS10Result
from app.services.calculation_service import CalculationService

router = APIRouter(prefix="/api/v1/questions", tags=["questions"])


@router.post("/", response_model=QuestionResponse)
async def submit_question(
    question: QuestionResponseCreate, db: AsyncSession = Depends(get_db)
):
    """Submit a question answer"""
    new_response = QuestionResponseModel(
        question_number=question.question_number,
        answer_value=question.answer_value,
        # TODO: Get user_id from auth token
        user_id=1,  # Temporary user_id
    )
    db.add(new_response)
    await db.commit()
    await db.refresh(new_response)
    return new_response


@router.get("/pss10", response_model=PSS10Result)
async def get_pss10_result(db: AsyncSession = Depends(get_db)):
    """Get PSS-10 questionnaire result"""
    # Get the latest 10 responses
    query = (
        select(QuestionResponseModel)
        .order_by(QuestionResponseModel.timestamp.desc())
        .limit(10)
    )

    result = await db.execute(query)
    responses = result.scalars().all()

    if len(responses) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough responses for PSS-10 calculation. Need 10 responses.",
        )

    # Convert to list of answer values
    answer_values = [
        r.answer_value for r in sorted(responses, key=lambda x: x.question_number)
    ]

    # Calculate PSS-10 score
    total_score = CalculationService.calculate_pss10(answer_values)
    stress_level = CalculationService.calculate_stress_level(total_score)

    return PSS10Result(
        total_score=total_score, stress_level=stress_level, timestamp=datetime.now()
    )
