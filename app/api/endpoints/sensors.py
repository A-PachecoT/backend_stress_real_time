from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorResponse

router = APIRouter(prefix="/api/v1/sensors", tags=["sensors"])


@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_reading(
    sensor_data: SensorCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new sensor reading"""
    new_sensor = Sensor(
        temperatura=sensor_data.temperatura,
        ritmo_cardiaco=sensor_data.ritmo_cardiaco,
        indice_facial=sensor_data.indice_facial,
        timestamp=datetime.now(),
    )
    db.add(new_sensor)
    await db.commit()
    await db.refresh(new_sensor)
    return new_sensor


@router.get("/latest", response_model=List[SensorResponse])
async def get_latest_readings(minutes: int = 5, db: AsyncSession = Depends(get_db)):
    """Get sensor readings from the last X minutes"""
    time_threshold = datetime.now() - timedelta(minutes=minutes)

    query = (
        select(Sensor)
        .where(Sensor.timestamp >= time_threshold)
        .order_by(Sensor.timestamp.desc())
    )

    result = await db.execute(query)
    readings = result.scalars().all()

    if not readings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sensor readings found in the specified time range",
        )

    return readings
