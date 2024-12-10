from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class QuestionResponse(Base):
    __tablename__ = "question_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    question_number = Column(Integer, nullable=False)
    answer_value = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
