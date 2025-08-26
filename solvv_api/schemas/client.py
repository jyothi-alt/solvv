from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from solvv_api.core.database import Base
from solvv_api.schemas import Client, ClientCreate



class ClientTypeEnum(str, Enum):
    retail = "retail"
    corporate = "corporate"

class ClientCreate(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    client_type: ClientTypeEnum

class Client(BaseModel):
    id: int
    name: str
    email: EmailStr
    client_type: ClientTypeEnum

    class Config:
        orm_mode = True
