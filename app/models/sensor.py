from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Sensor(Base):
    __tablename__ = "sensores"

    id = Column(Integer, primary_key=True, index=True)
    temperatura = Column(Float)
    ritmo_cardiaco = Column(Float)
    indice_facial = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
