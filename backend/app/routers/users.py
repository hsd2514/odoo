# routers/users.py
# FastAPI routes for users
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User, UserRole, AvailabilityType
from app.schemas.user import (
    UserCreate, UserResponse, UserUpdate, UserProfile, 
    UserPublicProfile, UserSearchResponse
)
from app.utils.auth import get_current_user, get_password_hash
from app.utils.hashing import verify_password

router = APIRouter(prefix="/users", tags=["users"])

# =============== USER REGISTRATION & PROFILE ===============

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        bio=user.bio,
        location=user.location,
        availability=user.availability,
        availability_details=user.availability_details,
        is_profile_public=user.is_profile_public
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's complete profile"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile"""
    # Check if username is being changed and is available
    if user_update.username and user_update.username != current_user.username:
        existing_username = db.query(User).filter(User.username == user_update.username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/upload-photo")
async def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload profile photo"""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # In a real application, you would upload to cloud storage (AWS S3, etc.)
    # For now, we'll just simulate saving the file path
    file_path = f"/uploads/profiles/{current_user.id}_{file.filename}"
    
    current_user.profile_photo_url = file_path
    db.commit()
    
    return {"message": "Profile photo uploaded successfully", "url": file_path}

# =============== USER DISCOVERY & SEARCH ===============

@router.get("/search", response_model=List[UserSearchResponse])
async def search_users(
    skill_name: Optional[str] = Query(None, description="Search by skill name"),
    location: Optional[str] = Query(None, description="Filter by location"),
    availability: Optional[AvailabilityType] = Query(None, description="Filter by availability"),
    has_skills: bool = Query(True, description="Only users with skills"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search for users by skills, location, or availability"""
    query = db.query(User).filter(
        User.is_active == True,
        User.is_banned == False,
        User.is_profile_public == True
    )
    
    if location:
        query = query.filter(User.location.ilike(f"%{location}%"))
    
    if availability:
        query = query.filter(User.availability == availability)
    
    # If searching by skill, join with UserSkill table
    if skill_name:
        from app.models.skill import UserSkill, Skill
        query = query.join(UserSkill).join(Skill).filter(
            Skill.name.ilike(f"%{skill_name}%"),
            UserSkill.is_approved == True
        )
    elif has_skills:
        from app.models.skill import UserSkill
        query = query.join(UserSkill).filter(UserSkill.is_approved == True)
    
    users = query.distinct().offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}/profile", response_model=UserPublicProfile)
async def get_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    """Get a user's public profile"""
    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True,
        User.is_banned == False
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_profile_public:
        raise HTTPException(status_code=403, detail="User profile is private")
    
    return user

@router.get("/", response_model=List[UserSearchResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all active public users (for browsing)"""
    users = db.query(User).filter(
        User.is_active == True,
        User.is_banned == False,
        User.is_profile_public == True,
        User.id != current_user.id  # Exclude current user
    ).offset(skip).limit(limit).all()
    
    return users

# =============== USER STATISTICS ===============

@router.get("/me/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's statistics"""
    from app.models.skill import UserSkill, SkillRequest
    from app.models.swap import Swap, SwapStatus
    from app.models.feedback import Feedback
    
    # Count offered skills
    skills_offered = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.is_approved == True
    ).count()
    
    # Count wanted skills
    skills_wanted = db.query(SkillRequest).filter(
        SkillRequest.user_id == current_user.id,
        SkillRequest.is_active == True
    ).count()
    
    # Count swaps
    total_swaps = db.query(Swap).filter(
        (Swap.requester_id == current_user.id) | 
        (Swap.requested_user_id == current_user.id)
    ).count()
    
    completed_swaps = db.query(Swap).filter(
        ((Swap.requester_id == current_user.id) | 
         (Swap.requested_user_id == current_user.id)),
        Swap.status == SwapStatus.COMPLETED
    ).count()
    
    # Count feedback
    feedback_received = db.query(Feedback).filter(
        Feedback.receiver_id == current_user.id
    ).count()
    
    return {
        "skills_offered": skills_offered,
        "skills_wanted": skills_wanted,
        "total_swaps": total_swaps,
        "completed_swaps": completed_swaps,
        "feedback_received": feedback_received,
        "average_rating": current_user.average_rating,
        "member_since": current_user.created_at.strftime("%B %Y")
    }

# =============== ACCOUNT MANAGEMENT ===============

@router.put("/me/privacy")
async def update_privacy_settings(
    is_profile_public: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user privacy settings"""
    current_user.is_profile_public = is_profile_public
    db.commit()
    
    return {
        "message": "Privacy settings updated successfully",
        "is_profile_public": is_profile_public
    }

@router.post("/me/deactivate")
async def deactivate_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deactivate user account"""
    current_user.is_active = False
    db.commit()
    
    return {"message": "Account deactivated successfully"}

@router.post("/me/reactivate")
async def reactivate_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reactivate user account"""
    if current_user.is_banned:
        raise HTTPException(status_code=403, detail="Cannot reactivate banned account")
    
    current_user.is_active = True
    db.commit()
    
    return {"message": "Account reactivated successfully"}
