from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SensorBase(BaseModel):
    temperatura: float = Field(
        ..., description="Temperature in Celsius", ge=35.0, le=42.0
    )
    ritmo_cardiaco: float = Field(..., description="Heart rate in BPM", ge=40, le=200)


class SensorCreate(SensorBase):
    pass


class SensorResponse(SensorBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
