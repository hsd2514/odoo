from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    name: str
    email: EmailStr
    location: Optional[str]
    availability: Optional[str]
    is_public: Optional[bool] = True
    skills_offered: Optional[List[str]] = []
    skills_wanted: Optional[List[str]] = []


class UserCreate(UserBase):
    password: str

# Login schema for /auth/login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    availability: Optional[str]
    is_public: Optional[bool]
    photo_url: Optional[str]
    skills_offered: Optional[List[str]] = []
    skills_wanted: Optional[List[str]] = []

class UserResponse(UserBase):
    id: int
    rating: Optional[float] = None
    skills_offered: Optional[List[str]] = []
    skills_wanted: Optional[List[str]] = []
    class Config:
        orm_mode = True
