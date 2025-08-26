from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class Client(BaseModel):
    id: int = Field(..., gt=0, description="Client ID must be positive")
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^(?:\+91)?[6-9]\d{9}$')

    @validator('name')
    def name_must_be_alphabetic(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError('Name must only contain letters and spaces')
        return v


class ClientBase(BaseModel):
    name: str
    email: str
    client_type: Optional[str] = None
    gst_number: Optional[str] = None
    description: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
         from_attributes = True
