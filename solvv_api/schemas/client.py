from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import Optional

class ClientTypeEnum(str, Enum):
    retail = "retail"
    corporate = "corporate"

class ClientCreate(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    client_type: ClientTypeEnum
    gst_number: Optional[str] = None
    description: Optional[str] = None

class ClientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    client_type: ClientTypeEnum
    gst_number: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True
