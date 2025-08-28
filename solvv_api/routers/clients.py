# solvv_api/routers/clients.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from solvv_api.core.database import get_db
from solvv_api.models.client import ClientModel  # SQLAlchemy model
from solvv_api.schemas.client import ClientCreate, ClientResponse

from solvv_api.exceptions.custom_exceptions import (
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidClientTypeException
)
from solvv_api.exceptions.handlers import (
    client_not_found_handler,
    client_already_exists_handler,
    invalid_client_type_handler
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

# ---------------- GET ALL CLIENTS ----------------
@router.get("/", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(ClientModel).all()
    return clients

# ---------------- GET SINGLE CLIENT ----------------
@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise ClientNotFoundException(f"Client with ID {client_id} not found")
    return client

# ---------------- CREATE CLIENT ----------------
@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Check if client with same email already exists
    existing = db.query(ClientModel).filter(ClientModel.email == client.email).first()
    if existing:
        raise ClientAlreadyExistsException(f"Client with email {client.email} already exists")

    # Validate client_type
    valid_types = ["retail", "corporate"]
    if client.client_type not in valid_types:
        raise InvalidClientTypeException(f"Client type must be one of {valid_types}")

    new_client = ClientModel(
        name=client.name,
        email=client.email,
        client_type=client.client_type,
        gst_number=getattr(client, "gst_number", None),
        description=getattr(client, "description", None),
        created_at=datetime.utcnow()
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# ---------------- UPDATE CLIENT ----------------
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, updated: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise ClientNotFoundException(f"Client with ID {client_id} not found")

    # Validate client_type
    valid_types = ["retail", "corporate"]
    if updated.client_type not in valid_types:
        raise InvalidClientTypeException(f"Client type must be one of {valid_types}")

    # Update fields safely
    for key, value in updated.model_dump().items():  # Pydantic v2
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

# ---------------- DELETE CLIENT ----------------
@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise ClientNotFoundException(f"Client with ID {client_id} not found")
    
    db.delete(client)
    db.commit()
    return {"message": f"Client {client_id} deleted successfully"}
