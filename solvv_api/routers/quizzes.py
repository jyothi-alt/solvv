from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.models import Quiz as QuizModel
from schemas import Quiz, QuizCreate

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Quiz)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = QuizModel(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.get("/", response_model=List[Quiz])
def get_quizzes(db: Session = Depends(get_db)):
    return db.query(QuizModel).all()

@router.get("/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.put("/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, updated_quiz: QuizCreate, db: Session = Depends(get_db)):
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    for key, value in updated_quiz.dict().items():
        setattr(quiz, key, value)
    db.commit()
    db.refresh(quiz)
    return quiz

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db.delete(quiz)
    db.commit()
    return {"message": f"Quiz {quiz_id} deleted successfully"}
