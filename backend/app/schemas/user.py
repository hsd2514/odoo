# schemas/user.py
# Pydantic schemas for User models
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AvailabilityType(str, Enum):
    WEEKENDS = "weekends"
    EVENINGS = "evenings"  
    WEEKDAYS = "weekdays"
    ANYTIME = "anytime"
    CUSTOM = "custom"

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

# Base schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name")
    bio: Optional[str] = Field(None, max_length=500, description="User bio")
    location: Optional[str] = Field(None, max_length=100, description="User location")
    availability: AvailabilityType = Field(default=AvailabilityType.ANYTIME, description="Availability")
    availability_details: Optional[str] = Field(None, max_length=200, description="Availability details")
    is_profile_public: bool = Field(default=True, description="Profile visibility")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    availability: Optional[AvailabilityType] = None
    availability_details: Optional[str] = Field(None, max_length=200)
    is_profile_public: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_banned: bool
    is_email_verified: bool
    total_rating: int
    rating_count: int
    average_rating: float
    profile_photo_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfile(UserResponse):
    """Complete user profile for the user themselves"""
    ban_reason: Optional[str]
    banned_at: Optional[datetime]

class UserPublicProfile(BaseModel):
    """Public profile visible to other users"""
    id: int
    username: str
    full_name: str
    bio: Optional[str]
    location: Optional[str]
    availability: AvailabilityType
    availability_details: Optional[str]
    profile_photo_url: Optional[str]
    average_rating: float
    rating_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserSearchResponse(BaseModel):
    """User info for search results"""
    id: int
    username: str
    full_name: str
    location: Optional[str]
    availability: AvailabilityType
    profile_photo_url: Optional[str]
    average_rating: float
    skills_count: Optional[int] = 0

    class Config:
        from_attributes = True
