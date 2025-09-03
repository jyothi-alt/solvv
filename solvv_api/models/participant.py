from sqlalchemy import Column, Integer, String, DateTime
from solvv_api.core.database import Base
from datetime import datetime

class ParticipantModel(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
