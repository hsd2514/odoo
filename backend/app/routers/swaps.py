

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.swap import Swap
from app.models.user import User
from app.models.skill import Skill
from app.schemas.swap import SwapCreate, SwapUpdate, SwapResponse, SwapDetailResponse
from fastapi import Body
from app.utils.jwt import get_current_user_jwt

router = APIRouter(prefix="/swaps", tags=["Swaps"])


# Real dependency for current user using JWT
def get_current_user(user=Depends(get_current_user_jwt)):
    return user.id

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
        status="pending",
        message=getattr(swap, "message", None)
    )
    db.add(db_swap)
    db.commit()
    db.refresh(db_swap)
    return db_swap


# Helper to enrich swap with user/skill names
def enrich_swap(swap, db):
    sender = db.query(User).filter_by(id=swap.sender_id).first()
    receiver = db.query(User).filter_by(id=swap.receiver_id).first()
    skill_offered = db.query(Skill).filter_by(id=swap.skill_offered).first()
    skill_requested = db.query(Skill).filter_by(id=swap.skill_requested).first()
    return {
        'id': swap.id,
        'sender_id': swap.sender_id,
        'receiver_id': swap.receiver_id,
        'sender_name': sender.name if sender else str(swap.sender_id),
        'receiver_name': receiver.name if receiver else str(swap.receiver_id),
        'skill_offered': swap.skill_offered,
        'skill_offered_name': skill_offered.name if skill_offered else str(swap.skill_offered),
        'skill_requested': swap.skill_requested,
        'skill_requested_name': skill_requested.name if skill_requested else str(swap.skill_requested),
        'status': swap.status,
        'scheduled_time': swap.scheduled_time,
        'created_at': swap.created_at,
        'message': getattr(swap, 'message', None),
        'rating': swap.rating,
        'feedback': swap.feedback
    }
# POST /swaps/{swap_id}/feedback – Submit feedback/rating for a swap
@router.post("/{swap_id}/feedback", response_model=SwapResponse)
def submit_swap_feedback(swap_id: int, rating: int = Body(...), feedback: str = Body(""), db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    swap.rating = rating
    swap.feedback = feedback
    db.commit()
    db.refresh(swap)
    return enrich_swap(swap, db)

# GET /swaps/incoming – List incoming swap requests
@router.get("/incoming", response_model=List[SwapDetailResponse])
def get_incoming_swaps(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    swaps = db.query(Swap).filter(Swap.receiver_id == current_user).all()
    return [enrich_swap(s, db) for s in swaps]

# GET /swaps/outgoing – List outgoing swap requests
@router.get("/outgoing", response_model=List[SwapDetailResponse])
def get_outgoing_swaps(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    swaps = db.query(Swap).filter(Swap.sender_id == current_user).all()
    return [enrich_swap(s, db) for s in swaps]

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
