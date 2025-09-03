# solvv_api/models/feedback.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from solvv_api.core.database import Base

class FeedbackForm(Base):
    __tablename__ = "feedback_forms"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    admin_email = Column(String(255), nullable=False)

class FeedbackResponse(Base):
    __tablename__ = "feedback_responses"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("feedback_forms.id"), index=True, nullable=False)
    participant_id = Column(Integer, ForeignKey("participants.id"), index=True, nullable=False)
    response_json = Column(String)  # store serialized answers
    submitted_at = Column(DateTime, default=datetime.utcnow)
