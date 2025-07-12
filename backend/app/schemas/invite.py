from pydantic import BaseModel

from datetime import datetime
from typing import Optional

class InviteCreate(BaseModel):
    receiver_id: int
    skill_id: int
    message: Optional[str] = None

class InviteUpdate(BaseModel):
    status: str  # pending, accepted, rejected

class InviteResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    skill_id: int
    sender_name: Optional[str] = None
    receiver_name: Optional[str] = None
    skill_name: Optional[str] = None
    message: Optional[str] = None
    status: str
    created_at: datetime
    rating: Optional[int] = None
    feedback: Optional[str] = None

    class Config:
        orm_mode = True
