from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SwapDetailResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    sender_name: str
    receiver_name: str
    skill_offered: int
    skill_offered_name: str
    skill_requested: int
    skill_requested_name: str
    status: str
    scheduled_time: Optional[datetime]
    created_at: datetime
    message: Optional[str] = None

    class Config:
        orm_mode = True
from typing import Optional

class SwapCreate(BaseModel):
    receiver_id: int
    skill_offered: int
    skill_requested: int
    scheduled_time: Optional[datetime]
    message: Optional[str] = None

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
    message: Optional[str] = None

    class Config:
        orm_mode = True
