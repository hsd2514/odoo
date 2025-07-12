# routers/badges.py
# FastAPI routes for badges (skeleton)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.badge import Badge
from app.schemas.badge import BadgeCreate, BadgeResponse

router = APIRouter()

# GET /badges/ - List all badges
@router.get("/badges/", response_model=List[BadgeResponse])
async def list_badges(db: Session = Depends(get_db)):
    """Get all badges."""
    return db.query(Badge).all()

# GET /badges/user/{user_id} - List all badges for a user
@router.get("/badges/user/{user_id}", response_model=List[BadgeResponse])
async def list_user_badges(user_id: int, db: Session = Depends(get_db)):
    """Get all badges for a user."""
    return db.query(Badge).filter(Badge.user_id == user_id).all()

# POST /badges/ - Award a badge to a user
@router.post("/badges/", response_model=BadgeResponse)
async def create_badge(badge: BadgeCreate, db: Session = Depends(get_db)):
    """Award a badge to a user."""
    db_badge = Badge(**badge.dict())
    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    return db_badge
