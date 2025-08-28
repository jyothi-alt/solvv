from sqlalchemy import Column, Integer, String, DateTime
from solvv_api.core.database import Base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    client_type = Column(String, nullable=False)
    gst_number = Column(String, nullable=True)
    description = Column(String, nullable=True)
