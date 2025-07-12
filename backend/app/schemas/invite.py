from pydantic import BaseModel

class InviteCreate(BaseModel):
    receiver_id: int
    skill_id: int

class InviteUpdate(BaseModel):
    status: str  # pending, accepted, rejected

class InviteResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    skill_id: int
    status: str

    class Config:
        orm_mode = True
