# solvv_api/models/resource.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from solvv_api.core.database import Base

class CourseResource(Base):
    __tablename__ = "course_resources"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
