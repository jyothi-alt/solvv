from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# Database URL
DATABASE_URL = "postgresql+psycopg2://postgres:982001@localhost:5432/solvv"

# Initialize FastAPI
app = FastAPI()

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Client Table
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    client_type = Column(String(50), nullable=True)
    gst_number = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)

# Create tables if not exists
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ClientBase(BaseModel):
    name: str
    email: str
    client_type: Optional[str] = None
    gst_number: Optional[str] = None
    description: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientOut(ClientBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Solvv!"}

# CRUD Operations
@app.post("/clients/", response_model=ClientOut)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/", response_model=List[ClientOut])
def read_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@app.get("/clients/{client_id}", response_model=ClientOut)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=ClientOut)
def update_client(client_id: int, updated_client: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in updated_client.dict().items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}
