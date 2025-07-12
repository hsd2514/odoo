# schemas/swap.py
# Pydantic schemas for Swap models
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SwapStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class SwapType(str, Enum):
    SKILL_FOR_SKILL = "skill_for_skill"
    SKILL_FOR_TIME = "skill_for_time"
    TIME_FOR_SKILL = "time_for_skill"

# Base schemas
class SwapBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Swap title")
    description: Optional[str] = Field(None, max_length=1000, description="Swap description")
    swap_type: SwapType = Field(default=SwapType.SKILL_FOR_SKILL, description="Type of swap")
    estimated_duration_hours: Optional[int] = Field(None, ge=1, le=200, description="Estimated duration in hours")
    preferred_method: str = Field(default="online", description="Preferred communication method")
    meeting_location: Optional[str] = Field(None, max_length=200, description="Meeting location if in-person")

class SwapCreate(SwapBase):
    requested_user_id: int = Field(..., description="ID of the user being requested")
    offered_skill_id: int = Field(..., description="ID of skill being offered")
    requested_skill_id: int = Field(..., description="ID of skill being requested")
    proposed_start_date: Optional[datetime] = Field(None, description="Proposed start date")

class SwapUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    estimated_duration_hours: Optional[int] = Field(None, ge=1, le=200)
    preferred_method: Optional[str] = Field(None, max_length=50)
    meeting_location: Optional[str] = Field(None, max_length=200)
    proposed_start_date: Optional[datetime] = None

class SwapStatusUpdate(BaseModel):
    status: SwapStatus = Field(..., description="New status for the swap")
    reason: Optional[str] = Field(None, max_length=500, description="Reason for status change")

# Response schemas
class UserBasicInfo(BaseModel):
    id: int
    username: str
    full_name: str
    profile_photo_url: Optional[str]
    average_rating: float

    class Config:
        from_attributes = True

class SkillBasicInfo(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True

class SwapResponse(SwapBase):
    id: int
    requester_id: int
    requested_user_id: int
    offered_skill_id: int
    requested_skill_id: int
    status: SwapStatus
    proposed_start_date: Optional[datetime]
    actual_start_date: Optional[datetime]
    completion_date: Optional[datetime]
    response_deadline: Optional[datetime]
    requester_progress: int
    requested_user_progress: int
    is_flagged: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SwapListResponse(BaseModel):
    id: int
    title: str
    status: SwapStatus
    swap_type: SwapType
    requester: UserBasicInfo
    requested_user: UserBasicInfo
    offered_skill: SkillBasicInfo
    requested_skill: SkillBasicInfo
    created_at: datetime
    response_deadline: Optional[datetime]
    estimated_duration_hours: Optional[int]

    class Config:
        from_attributes = True

class SwapDetailResponse(SwapResponse):
    requester: UserBasicInfo
    requested_user: UserBasicInfo
    offered_skill: SkillBasicInfo
    requested_skill: SkillBasicInfo
    cancelled_by_user: Optional[UserBasicInfo]
    rejection_reason: Optional[str]
    cancellation_reason: Optional[str]
    admin_notes: Optional[str]

    class Config:
        from_attributes = True

class SwapProgressUpdate(BaseModel):
    progress: int = Field(..., ge=0, le=100, description="Progress percentage (0-100)")

class SwapAcceptRequest(BaseModel):
    proposed_start_date: Optional[datetime] = None
    meeting_location: Optional[str] = Field(None, max_length=200)

class SwapRejectRequest(BaseModel):
    rejection_reason: Optional[str] = Field(None, max_length=500, description="Reason for rejection")

class SwapCancelRequest(BaseModel):
    cancellation_reason: Optional[str] = Field(None, max_length=500, description="Reason for cancellation")

class SwapStatsResponse(BaseModel):
    swap_counts: dict
    success_rate_percentage: float
    total_swaps: int
