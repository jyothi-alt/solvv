from sqlalchemy import Column, Integer, String, Enum, Text, TIMESTAMP
from sqlalchemy.sql import func
from solvv_api.schemas.client import ClientType
from solvv_api.core.database import Base
import enum
from sqlalchemy import Column, Integer, String, DateTime, func


class ClientType(enum.Enum):
    retail = "retail"
    corporate = "corporate"




class ClientModel(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_name = Column(String(255), nullable=False)
    client_type = Column(Enum(ClientType), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    gst_number = Column(String(20), unique=True, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())