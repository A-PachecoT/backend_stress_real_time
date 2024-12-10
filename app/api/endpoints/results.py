from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.sensor import Sensor
from app.models.question import QuestionResponse
from app.schemas.stress import StressAnalysis
from app.services.calculation_service import CalculationService

router = APIRouter(prefix="/api/v1/results", tags=["results"])


@router.get("/", response_model=StressAnalysis)
async def get_results(minutes: int = 30, db: AsyncSession = Depends(get_db)):
    """Get stress analysis results"""
    # Get recent sensor readings
    time_threshold = datetime.now() - timedelta(minutes=minutes)
    sensor_query = (
        select(Sensor)
        .where(Sensor.timestamp >= time_threshold)
        .order_by(Sensor.timestamp.desc())
    )

    sensor_result = await db.execute(sensor_query)
    sensor_readings = sensor_result.scalars().all()

    if not sensor_readings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sensor readings found in the specified time range",
        )

    # Get latest PSS-10 responses if available
    pss10_query = (
        select(QuestionResponse).order_by(QuestionResponse.timestamp.desc()).limit(10)
    )

    pss10_result = await db.execute(pss10_query)
    pss10_responses = pss10_result.scalars().all()

    # Prepare data for analysis
    sensor_data = [
        {"ritmo_cardiaco": reading.ritmo_cardiaco, "temperatura": reading.temperatura}
        for reading in sensor_readings
    ]

    pss10_values = None
    if len(pss10_responses) == 10:
        pss10_values = [
            r.answer_value
            for r in sorted(pss10_responses, key=lambda x: x.question_number)
        ]

    # Get stress analysis
    analysis = await CalculationService.get_stress_analysis(
        sensor_data=sensor_data, pss10_responses=pss10_values
    )

    return StressAnalysis(**analysis)
