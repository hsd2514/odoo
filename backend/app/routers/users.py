

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse

# Set a prefix for all user-related endpoints
router = APIRouter(prefix="/users", tags=["users"])


from sqlalchemy import distinct

# GET /users/locations – List all unique user locations
@router.get("/locations", response_model=List[str])
def list_user_locations(db: Session = Depends(get_db)):
    """Get all unique user locations."""
    locations = db.query(distinct(User.location)).all()
    return [l[0] for l in locations if l[0]]

# GET /users/public – List public profiles with search, filter, pagination
@router.get("/public", response_model=List[UserResponse])
def list_public_profiles(
    db: Session = Depends(get_db),
    search: str = Query(None, description="Search by name/email"),
    availability: str = Query(None, description="Filter by availability"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Page size"),
):
    """
    List public user profiles with optional search, filter, and pagination.
    Example: /users/public?search=alice&page=2&page_size=5
    """
    query = db.query(User).filter(User.is_public == True)
    if search:
        query = query.filter((User.name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%")))
    if availability:
        query = query.filter(User.availability == availability)
    profiles = query.offset((page - 1) * page_size).limit(page_size).all()
    return profiles



# Dummy dependency for current user (replace with real auth in production)
def get_current_user(db: Session = Depends(get_db)):
    # For hackathon, just return the first user
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


# GET /users/me – My profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get the current user's profile."""
    return current_user


# PUT /users/me – Update profile
@router.put("/me", response_model=UserResponse)
def update_my_profile(
    update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update the current user's profile."""
    for field, value in update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


# GET /users/{id} – View public profile
@router.get("/{id}", response_model=UserResponse)
def get_user_profile(id: int, db: Session = Depends(get_db)):
    """Get a public user profile by user ID."""
    user = db.query(User).filter(User.id == id, User.is_public == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not public")
    return user
