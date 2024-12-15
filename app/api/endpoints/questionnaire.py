from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
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
    # Verificar si el usuario ya respondió algunas preguntas
    for answer in answers.answers:
        query = select(QuestionResponse).where(
            QuestionResponse.user_id == current_user.id,
            QuestionResponse.question_number == answer.question_number,
        )
        result = await db.execute(query)
        existing_response = result.scalar_one_or_none()

        if existing_response:
            # Actualizar respuesta existente
            existing_response.answer_value = answer.answer
        else:
            # Crear nueva respuesta
            new_response = QuestionResponse(
                user_id=current_user.id,
                question_number=answer.question_number,
                answer_value=answer.answer,
            )
            db.add(new_response)

    await db.commit()

    # Obtener todas las respuestas actualizadas
    query = select(QuestionResponse).where(
        QuestionResponse.user_id == current_user.id,
        QuestionResponse.question_number.in_(
            [a.question_number for a in answers.answers]
        ),
    )
    result = await db.execute(query)
    responses = result.scalars().all()

    return responses


@router.get("/answers", response_model=List[QuestionResponseDB])
async def get_answers(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get user's questionnaire answers"""
    query = (
        select(QuestionResponse)
        .where(QuestionResponse.user_id == current_user.id)
        .order_by(QuestionResponse.question_number)
    )

    result = await db.execute(query)
    responses = result.scalars().all()

    return responses
