from sqlalchemy import Column, Integer, String, Enum, DateTime
from solvv_api.core.database import Base
from solvv_api.schemas.client import ClientTypeEnum

class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    client_type = Column(Enum(ClientTypeEnum), nullable=False)
    gst_number = Column(String(20), nullable=True)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime)
