

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.utils.jwt import get_current_user_jwt

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
    location: str = Query(None, description="Filter by location"),
    skill: str = Query(None, description="Filter by skill name (offered or wanted)"),
    category: str = Query(None, description="Filter by skill category (offered or wanted)"),
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
    if location:
        query = query.filter(User.location == location)
    if skill:
        # skills_offered and skills_wanted are arrays of strings (JSONB)
        query = query.filter(
            (User.skills_offered != None) & (User.skills_offered.contains([skill])) |
            (User.skills_wanted != None) & (User.skills_wanted.contains([skill]))
        )
    if category:
        from app.models.skill import Skill
        from sqlalchemy import or_
        # Get all skill names in this category
        skill_names = [s.name for s in db.query(Skill).filter(Skill.category == category).all()]
        if skill_names:
            # For JSONB, use .contains([name]) for each skill name, combine with or_
            query = query.filter(
                (User.skills_offered != None) & (
                    or_(*[User.skills_offered.contains([name]) for name in skill_names])
                ) |
                (User.skills_wanted != None) & (
                    or_(*[User.skills_wanted.contains([name]) for name in skill_names])
                )
            )
    profiles = query.offset((page - 1) * page_size).limit(page_size).all()

    # Calculate average rating for each user from invites and swaps where user is receiver
    from app.models.invite import Invite
    from app.models.swap import Swap
    result = []
    for user in profiles:
        # Get all ratings where user is receiver
        invite_ratings = db.query(Invite.rating).filter(Invite.receiver_id == user.id, Invite.rating != None).all()
        swap_ratings = db.query(Swap.rating).filter(Swap.receiver_id == user.id, Swap.rating != None).all()
        ratings = [r[0] for r in invite_ratings + swap_ratings if r[0] is not None]
        user.rating = round(sum(ratings) / len(ratings), 2) if ratings else None
        result.append(user)
    return result




# Real dependency for current user using JWT
get_current_user = get_current_user_jwt


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
