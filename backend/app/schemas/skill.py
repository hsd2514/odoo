from pydantic import BaseModel
from typing import Literal

class SkillBase(BaseModel):
    name: str
    category: str

class SkillCreate(SkillBase):
    pass

class UserSkillAssign(BaseModel):
    skill_id: int
    type: Literal["offered", "wanted"]

class SkillResponse(SkillBase):
    id: int
    class Config:
        orm_mode = True
