from sqlalchemy.orm import Session
from solvv_api.models.models import Client as ClientModel
from solvv_api.schemas import ClientCreate

def create_client(db: Session, client: ClientCreate):
    db_client = ClientModel(name=client.name, email=client.email)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClientModel).offset(skip).limit(limit).all()

def get_client(db: Session, client_id: int):
    return db.query(ClientModel).filter(ClientModel.id == client_id).first()

def update_client(db: Session, client_id: int, client: ClientCreate):
    db_client = get_client(db, client_id)
    if db_client:
        db_client.name = client.name
        db_client.email = client.email
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client
