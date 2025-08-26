from sqlalchemy import Column, Integer, String, Enum
from solvv_api.core.database import Base
from solvv_api.schemas import Client, ClientCreate


import enum

class ClientTypeEnum(str, enum.Enum):
    retail = "retail"
    corporate = "corporate"

class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    client_type = Column(Enum(ClientTypeEnum), nullable=False)
