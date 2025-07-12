
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter()

# Dummy dependency for current user (replace with real auth in production)
def get_current_user(db: Session = Depends(get_db)):
    # For hackathon, just return the first user
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# GET /users/me – My profile
@router.get("/users/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# PUT /users/me – Update profile
@router.put("/users/me", response_model=UserResponse)
def update_my_profile(
    update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    for field, value in update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

# GET /users/{id} – View public profile
@router.get("/users/{id}", response_model=UserResponse)
def get_user_profile(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id, User.is_public == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not public")
    return user
