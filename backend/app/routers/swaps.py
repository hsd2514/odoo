

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.swap import Swap
from app.schemas.swap import SwapCreate, SwapUpdate, SwapResponse

router = APIRouter(prefix="/swaps", tags=["Swaps"])

# Dummy dependency for current user (replace with real auth in production)
def get_current_user():
    return 1  # user id 1 for demo

# POST /swaps – Create a swap request
@router.post("/", response_model=SwapResponse)
def create_swap(
    swap: SwapCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    db_swap = Swap(
        sender_id=current_user,
        receiver_id=swap.receiver_id,
        skill_offered=swap.skill_offered,
        skill_requested=swap.skill_requested,
        scheduled_time=swap.scheduled_time,
        status="pending"
    )
    db.add(db_swap)
    db.commit()
    db.refresh(db_swap)
    return db_swap

# GET /swaps/incoming – List incoming swap requests
@router.get("/incoming", response_model=List[SwapResponse])
def get_incoming_swaps(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return db.query(Swap).filter(Swap.receiver_id == current_user).all()

# GET /swaps/outgoing – List outgoing swap requests
@router.get("/outgoing", response_model=List[SwapResponse])
def get_outgoing_swaps(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return db.query(Swap).filter(Swap.sender_id == current_user).all()

# PUT /swaps/{swap_id} – Update swap status
@router.put("/{swap_id}", response_model=SwapResponse)
def update_swap_status(swap_id: int, update: SwapUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    swap.status = update.status
    db.commit()
    db.refresh(swap)
    return swap
