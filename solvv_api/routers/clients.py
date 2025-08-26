from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from solvv_api.core.database import SessionLocal
from solvv_api.schemas import Client, ClientCreate
from solvv_api.models.models import Client as ClientModel
from solvv_api.exceptions.custom_exceptions import (
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidClientTypeException
)

router = APIRouter(prefix="/clients", tags=["Clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Client
@router.post("/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Validate phone number if provided
    if client.phone:
        if not re.match(INDIAN_PHONE_REGEX, client.phone):
            raise HTTPException(
                status_code=422,
                detail="Phone number must be a valid Indian number in +91XXXXXXXXXX format."
            )
    try:
        db_client = ClientModel(
            name=client.name,
            email=client.email,
            phone=client.phone,
            client_type=client.client_type,
            gst_number=client.gst_number,
            description=client.description
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return {"message": f"Client {db_client.id} created successfully"}
    except ValidationError as e:
        errors = [f"{err['loc'][-1]}: {err['msg']}" for err in e.errors()]
        raise HTTPException(status_code=422, detail=errors)

# Get All Clients
@router.get("/", response_model=List[Client])
def get_clients(db: Session = Depends(get_db)):
    return db.query(ClientModel).all()

# Get Client by ID
@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Update Client
@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, updated_client: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.name = updated_client.name
    client.email = updated_client.email
    client.client_type = updated_client.client_type
    client.gst_number = updated_client.gst_number
    client.description = updated_client.description

    db.commit()
    db.refresh(client)
    return client

# Delete Client
@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message": f"Client {client_id} deleted successfully"}
