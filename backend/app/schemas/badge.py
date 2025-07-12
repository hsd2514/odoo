from pydantic import BaseModel
from typing import Optional

class BadgeBase(BaseModel):
    skill_id: Optional[int]
    badge_type: str  # learned, mentor, rated_5star

class BadgeCreate(BadgeBase):
    user_id: int

class BadgeResponse(BadgeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
