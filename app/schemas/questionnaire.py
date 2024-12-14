from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class QuestionAnswer(BaseModel):
    question_number: int = Field(..., ge=1, le=20)
    answer: int = Field(..., ge=0, le=4)


class QuestionnaireAnswers(BaseModel):
    answers: List[QuestionAnswer]


class QuestionResponseDB(BaseModel):
    id: int
    user_id: int
    question_number: int
    answer_value: int
    timestamp: datetime

    class Config:
        from_attributes = True
