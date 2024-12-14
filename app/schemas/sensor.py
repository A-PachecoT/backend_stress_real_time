from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SensorBase(BaseModel):
    temperatura: float = Field(..., description="Temperatura en grados Celsius")
    ritmo_cardiaco: float = Field(..., description="Ritmo cardiaco en BPM")
    indice_facial: Optional[float] = Field(None, description="Índice facial")


class SensorCreate(SensorBase):
    pass


class SensorResponse(SensorBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
