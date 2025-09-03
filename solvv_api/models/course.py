# solvv_api/models/course.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from solvv_api.core.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), index=True)

    enrollments = relationship("Enrollment", back_populates="course")
