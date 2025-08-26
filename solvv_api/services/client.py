from sqlalchemy.orm import Session
from app.models.client import ClientModel
from app.schemas.client import ClientCreate
from solvv_api.core.database import Base
from solvv_api.schemas import Client, ClientCreate


def create_client(db: Session, client: ClientCreate):
    db_client = ClientModel(
        name=client.name,
        email=client.email,
        client_type=client.client_type
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClientModel).offset(skip).limit(limit).all()
