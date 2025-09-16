from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from solvv_api.core.database import get_db
from solvv_api.models.mentor import MentorModel
from solvv_api.schemas.mentor import MentorCreate, MentorOut, MentorUpdate

router = APIRouter(prefix="/mentors", tags=["Mentors"])

@router.post("/", response_model=MentorOut)
def create_mentor(mentor: MentorCreate, db: Session = Depends(get_db)):
    db_mentor = db.query(MentorModel).filter(MentorModel.email == mentor.email).first()
    if db_mentor:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_mentor = MentorModel(**mentor.dict())
    db.add(new_mentor)
    db.commit()
    db.refresh(new_mentor)
    return new_mentor

@router.get("/", response_model=List[MentorOut])
def get_all_mentors(db: Session = Depends(get_db)):
    mentors = db.query(MentorModel).all()
    return mentors

@router.get("/search", response_model=List[MentorOut])
def search_mentor(q: Optional[str] = Query(None, description="Search term for mentor name or email"), 
                  db: Session = Depends(get_db)):
    query = db.query(MentorModel)
    if q:
        query = query.filter((MentorModel.mentor_name.ilike(f"%{q}%")) | (MentorModel.email.ilike(f"%{q}%")))
    results = query.all()
    return results

@router.get("/{mentor_id}", response_model=MentorOut)
def get_single_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(MentorModel).filter(MentorModel.mentor_id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor

@router.put("/{mentor_id}", response_model=MentorOut)
def update_mentor(mentor_id: int, mentor_update: MentorUpdate, db: Session = Depends(get_db)):
    mentor = db.query(MentorModel).filter(MentorModel.mentor_id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    for key, value in mentor_update.dict(exclude_unset=True).items():
        setattr(mentor, key, value)
    db.commit()
    db.refresh(mentor)
    return mentor

@router.delete("/{mentor_id}")
def delete_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(MentorModel).filter(MentorModel.mentor_id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    db.delete(mentor)
    db.commit()
    return {"detail": "Mentor deleted successfully"}