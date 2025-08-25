from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models.models import Manager as ManagerModel
from schemas import Manager, ManagerCreate

router = APIRouter(prefix="/managers", tags=["Managers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Manager)
def create_manager(manager: ManagerCreate, db: Session = Depends(get_db)):
    db_manager = ManagerModel(**manager.dict())
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)
    return db_manager

@router.get("/", response_model=List[Manager])
def get_managers(db: Session = Depends(get_db)):
    return db.query(ManagerModel).all()

@router.get("/{manager_id}", response_model=Manager)
def get_manager(manager_id: int, db: Session = Depends(get_db)):
    manager = db.query(ManagerModel).filter(ManagerModel.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager

@router.put("/{manager_id}", response_model=Manager)
def update_manager(manager_id: int, updated_manager: ManagerCreate, db: Session = Depends(get_db)):
    manager = db.query(ManagerModel).filter(ManagerModel.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    for key, value in updated_manager.dict().items():
        setattr(manager, key, value)
    db.commit()
    db.refresh(manager)
    return manager

@router.delete("/{manager_id}")
def delete_manager(manager_id: int, db: Session = Depends(get_db)):
    manager = db.query(ManagerModel).filter(ManagerModel.id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    db.delete(manager)
    db.commit()
    return {"message": f"Manager {manager_id} deleted successfully"}
