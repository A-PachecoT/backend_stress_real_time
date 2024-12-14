from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class QuestionAnswer(BaseModel):
    question_number: int = Field(..., ge=1)
    answer: str


class QuestionnaireAnswers(BaseModel):
    answers: List[QuestionAnswer]


class QuestionResponseDB(BaseModel):
    id: int
    user_id: int
    question_number: int
    answer_value: str
    timestamp: datetime

    class Config:
        from_attributes = True
