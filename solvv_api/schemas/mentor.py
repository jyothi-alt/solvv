from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class MentorBase(BaseModel):
    mentor_name: str
    email: EmailStr
    phone_number: str
    bio: Optional[str] = None

class MentorCreate(MentorBase):
    pass

class MentorUpdate(BaseModel):
    mentor_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    bio: Optional[str]

class MentorOut(MentorBase):
    mentor_id: int
    created_at: datetime

    class Config:
        orm_mode = True