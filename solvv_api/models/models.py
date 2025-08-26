from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from solvv_api.core.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    client_type = Column(String(50))
    gst_number = Column(String(50))
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
