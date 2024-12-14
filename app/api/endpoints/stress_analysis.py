from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.question import QuestionResponse
from app.models.sensor import Sensor
from app.models.user import User
from app.schemas.stress import StressAnalysisResponse
from app.services.calculation_service import CalculationService

router = APIRouter(prefix="/api/v1/stress", tags=["stress"])


@router.get("/analysis", response_model=StressAnalysisResponse)
async def get_stress_analysis(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get stress analysis combining sensor data and questionnaire responses"""

    # Get latest sensor data
    sensor_query = select(Sensor).order_by(Sensor.timestamp.desc()).limit(1)
    sensor_result = await db.execute(sensor_query)
    latest_sensor = sensor_result.scalar_one_or_none()

    if not latest_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No sensor data available"
        )

    # Get questionnaire responses
    responses_query = (
        select(QuestionResponse)
        .where(QuestionResponse.user_id == current_user.id)
        .order_by(QuestionResponse.question_number)
    )
    responses_result = await db.execute(responses_query)
    responses = responses_result.scalars().all()

    if not responses:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questionnaire responses available",
        )

    # Prepare data for calculation
    sensor_data = [
        {
            "temperatura": latest_sensor.temperatura,
            "ritmo_cardiaco": latest_sensor.ritmo_cardiaco,
            "indice_facial": latest_sensor.indice_facial or 0,
        }
    ]

    pss10_responses = [r.answer_value for r in responses]

    # Calculate stress analysis
    try:
        analysis = await CalculationService.get_stress_analysis(
            sensor_data=sensor_data, pss10_responses=pss10_responses
        )

        return {
            "stress_percentage": round(analysis["stress_percentage"], 2),
            "description": f"Tiene un porcentaje de estrés {analysis['stress_level'].lower()}",
        }

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
