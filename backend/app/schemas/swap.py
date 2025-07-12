from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SwapCreate(BaseModel):
    receiver_id: int
    skill_offered: int
    skill_requested: int
    scheduled_time: Optional[datetime]

class SwapUpdate(BaseModel):
    status: str  # pending, accepted, rejected, completed

class SwapResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    skill_offered: int
    skill_requested: int
    status: str
    scheduled_time: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
