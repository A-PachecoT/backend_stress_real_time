from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class QuestionResponse(Base):
    __tablename__ = "question_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_number = Column(Integer)  # 1-10 for PSS-10
    answer_value = Column(Integer)  # 0-4 (nunca-siempre)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
