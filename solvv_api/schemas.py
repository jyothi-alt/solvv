from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
