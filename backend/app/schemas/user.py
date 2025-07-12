from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    name: str
    email: EmailStr
    location: Optional[str]
    availability: Optional[str]
    is_public: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    availability: Optional[str]
    is_public: Optional[bool]
    photo_url: Optional[str]

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True
