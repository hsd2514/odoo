from pydantic import BaseModel
from typing import Optional

class FeedbackCreate(BaseModel):
    swap_id: int
    to_user: int
    rating: int
    comment: Optional[str]

class FeedbackResponse(BaseModel):
    id: int
    from_user: int
    to_user: int
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode = True
