# schemas/feedback.py
# Pydantic schemas for Feedback models
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    SWAP_FEEDBACK = "swap_feedback"
    GENERAL_FEEDBACK = "general_feedback"
    SKILL_FEEDBACK = "skill_feedback"

# Base schemas
class FeedbackBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5 stars")
    title: Optional[str] = Field(None, max_length=200, description="Feedback title")
    comment: Optional[str] = Field(None, max_length=1000, description="Feedback comment")
    feedback_type: FeedbackType = Field(default=FeedbackType.SWAP_FEEDBACK, description="Type of feedback")
    communication_rating: Optional[int] = Field(None, ge=1, le=5, description="Communication rating")
    punctuality_rating: Optional[int] = Field(None, ge=1, le=5, description="Punctuality rating")
    skill_rating: Optional[int] = Field(None, ge=1, le=5, description="Skill quality rating")
    overall_experience_rating: Optional[int] = Field(None, ge=1, le=5, description="Overall experience rating")
    is_public: bool = Field(default=True, description="Whether feedback is public")

class FeedbackCreate(FeedbackBase):
    receiver_id: int = Field(..., description="ID of user receiving feedback")
    swap_id: Optional[int] = Field(None, description="ID of related swap (if applicable)")

class FeedbackUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    comment: Optional[str] = Field(None, max_length=1000)
    communication_rating: Optional[int] = Field(None, ge=1, le=5)
    punctuality_rating: Optional[int] = Field(None, ge=1, le=5)
    skill_rating: Optional[int] = Field(None, ge=1, le=5)
    overall_experience_rating: Optional[int] = Field(None, ge=1, le=5)
    is_public: Optional[bool] = None

class UserBasicInfo(BaseModel):
    id: int
    username: str
    full_name: str
    profile_photo_url: Optional[str]

    class Config:
        from_attributes = True

class FeedbackResponse(FeedbackBase):
    id: int
    giver_id: int
    receiver_id: int
    swap_id: Optional[int]
    is_verified: bool
    is_flagged: bool
    helpful_votes: int
    not_helpful_votes: int
    average_detailed_rating: float
    helpfulness_score: float
    response: Optional[str]
    response_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FeedbackListResponse(BaseModel):
    id: int
    rating: int
    title: Optional[str]
    comment: Optional[str]
    feedback_type: FeedbackType
    giver: UserBasicInfo
    helpful_votes: int
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackSummary(BaseModel):
    user_id: int
    total_feedback: int
    average_rating: float
    rating_distribution: Dict[str, int]
    recent_feedback: List[FeedbackListResponse]
