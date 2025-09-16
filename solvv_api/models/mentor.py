from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from solvv_api.core.database import Base

class MentorModel(Base):
    __tablename__ = "mentors"

    mentor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mentor_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())