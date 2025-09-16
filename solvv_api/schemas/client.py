from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ClientType(str, Enum):
    retail = "retail"
    corporate = "corporate"

class ClientCreate(BaseModel):
    client_name: str
    client_type: ClientType
    email: EmailStr
    phone_number: Optional[str] = None
    gst_number: Optional[str] = None
    description: Optional[str] = None

class ClientUpdate(BaseModel):
    client_name: Optional[str] = None
    client_type: Optional[ClientType] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    gst_number: Optional[str] = None
    description: Optional[str] = None

class ClientOut(BaseModel):
    client_id: int
    client_name: str
    client_type: ClientType
    email: EmailStr
    phone_number: Optional[str] = None
    gst_number: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None   # ✅ FIX: use datetime
    updated_at: Optional[datetime] = None   # ✅ add updated_at if your model has it

    class Config:
        orm_mode = True  # for SQLAlchemy models
