from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.question import QuestionResponse
from app.models.user import User
from app.schemas.questionnaire import QuestionnaireAnswers, QuestionResponseDB

router = APIRouter(prefix="/api/v1/questionnaire", tags=["questionnaire"])


@router.post("/answers", response_model=List[QuestionResponseDB])
async def submit_answers(
    answers: QuestionnaireAnswers,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit questionnaire answers"""
    responses = []

    for answer in answers.answers:
        response = QuestionResponse(
            user_id=current_user.id,
            question_number=answer.question_number,
            answer_value=answer.answer,
        )
        responses.append(response)
        db.add(response)

    await db.commit()

    # Refresh all responses to get their IDs and timestamps
    for response in responses:
        await db.refresh(response)

    return responses
