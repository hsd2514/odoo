
from typing import Literal, Optional
from enum import Enum
from pydantic import BaseModel


# Match the SkillLevel enum from models
class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

# UserSkillCreate schema
class UserSkillCreate(BaseModel):
    skill_id: int
    type: Literal["offered", "wanted"]
    level: SkillLevel = SkillLevel.beginner

# UserSkillUpdate schema
class UserSkillUpdate(BaseModel):
    type: Optional[Literal["offered", "wanted"]] = None
    level: Optional[SkillLevel] = None

# UserSkillResponse schema
class UserSkillResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    type: str
    level: SkillLevel
    is_approved: Optional[bool] = True
    can_teach_remotely: Optional[bool] = False
    proficiency_level: Optional[SkillLevel] = None
    class Config:
        orm_mode = True

# SkillRequestCreate schema
class SkillRequestCreate(BaseModel):
    skill_id: int
    message: Optional[str] = None

# SkillRequestUpdate schema
class SkillRequestUpdate(BaseModel):
    message: Optional[str] = None
    is_active: Optional[bool] = None

# SkillRequestResponse schema
class SkillRequestResponse(BaseModel):
    id: int
    user_id: int
    skill_id: int
    message: Optional[str]
    is_active: bool = True
    class Config:
        orm_mode = True



# SkillBase and related schemas
class SkillBase(BaseModel):
    name: str
    category: str

class SkillCreate(SkillBase):
    pass

class UserSkillAssign(BaseModel):
    skill_id: int
    type: Literal["offered", "wanted"]
    level: SkillLevel = SkillLevel.beginner

class SkillResponse(SkillBase):
    id: int
    class Config:
        orm_mode = True
