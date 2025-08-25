from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.models import Feedback as FeedbackModel
from schemas import Feedback, FeedbackCreate

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Feedback)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = FeedbackModel(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/", response_model=List[Feedback])
def get_feedbacks(db: Session = Depends(get_db)):
    return db.query(FeedbackModel).all()

@router.get("/{feedback_id}", response_model=Feedback)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.put("/{feedback_id}", response_model=Feedback)
def update_feedback(feedback_id: int, updated_feedback: FeedbackCreate, db: Session = Depends(get_db)):
    feedback = db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    for key, value in updated_feedback.dict().items():
        setattr(feedback, key, value)
    db.commit()
    db.refresh(feedback)
    return feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(feedback)
    db.commit()
    return {"message": f"Feedback {feedback_id} deleted successfully"}
