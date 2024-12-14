from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class StressAnalysis(BaseModel):
    timestamp: datetime
    total_stress_index: float = Field(
        ..., description="Total Stress Index (ITE)", ge=0.0, le=1.0
    )
    pss10_score: Optional[int] = Field(
        None, description="PSS-10 questionnaire score", ge=0, le=40
    )
    stress_level: Optional[str] = Field(
        None, description="Stress level interpretation (Bajo, Moderado, Alto)"
    )
    partial_indices: List[float] = Field(
        ..., description="List of partial stress indices (IP)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-12-06T12:00:00",
                "total_stress_index": 0.65,
                "pss10_score": 25,
                "stress_level": "Moderado",
                "partial_indices": [0.58, 0.62, 0.70, 0.65],
            }
        }
