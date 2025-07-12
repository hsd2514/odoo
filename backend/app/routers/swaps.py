# routers/swaps.py
# FastAPI routes for swaps
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.swap import Swap, SwapStatus, SwapType
from app.models.skill import Skill, UserSkill
from app.models.user import User
from app.schemas.swap import (
    SwapCreate, SwapResponse, SwapUpdate, SwapStatusUpdate,
    SwapListResponse, SwapDetailResponse
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/swaps", tags=["swaps"])

# =============== SWAP REQUEST MANAGEMENT ===============

@router.post("/", response_model=SwapResponse)
async def create_swap_request(
    swap: SwapCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new swap request"""
    # Validate that requested user exists and is active
    requested_user = db.query(User).filter(
        User.id == swap.requested_user_id,
        User.is_active == True,
        User.is_banned == False
    ).first()
    
    if not requested_user:
        raise HTTPException(status_code=404, detail="Requested user not found or inactive")
    
    # Can't create swap with yourself
    if swap.requested_user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create swap with yourself")
    
    # Validate offered skill belongs to current user
    offered_skill = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == swap.offered_skill_id,
        UserSkill.is_approved == True
    ).first()
    
    if not offered_skill:
        raise HTTPException(status_code=400, detail="You don't offer this skill")
    
    # Validate requested skill belongs to the requested user
    requested_skill = db.query(UserSkill).filter(
        UserSkill.user_id == swap.requested_user_id,
        UserSkill.skill_id == swap.requested_skill_id,
        UserSkill.is_approved == True
    ).first()
    
    if not requested_skill:
        raise HTTPException(status_code=400, detail="Requested user doesn't offer this skill")
    
    # Check for existing pending swap between same users for same skills
    existing_swap = db.query(Swap).filter(
        Swap.requester_id == current_user.id,
        Swap.requested_user_id == swap.requested_user_id,
        Swap.offered_skill_id == swap.offered_skill_id,
        Swap.requested_skill_id == swap.requested_skill_id,
        Swap.status == SwapStatus.PENDING
    ).first()
    
    if existing_swap:
        raise HTTPException(status_code=400, detail="You already have a pending swap request for these skills")
    
    # Set response deadline (7 days from now)
    response_deadline = datetime.utcnow() + timedelta(days=7)
    
    db_swap = Swap(
        requester_id=current_user.id,
        response_deadline=response_deadline,
        **swap.dict()
    )
    
    db.add(db_swap)
    db.commit()
    db.refresh(db_swap)
    
    return db_swap

@router.get("/", response_model=List[SwapListResponse])
async def get_user_swaps(
    status: Optional[SwapStatus] = Query(None),
    as_requester: Optional[bool] = Query(None, description="Filter swaps where user is requester"),
    as_requested: Optional[bool] = Query(None, description="Filter swaps where user is requested"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's swaps (both as requester and requested user)"""
    query = db.query(Swap).filter(
        (Swap.requester_id == current_user.id) | 
        (Swap.requested_user_id == current_user.id)
    )
    
    if status:
        query = query.filter(Swap.status == status)
    
    if as_requester is True:
        query = query.filter(Swap.requester_id == current_user.id)
    elif as_requested is True:
        query = query.filter(Swap.requested_user_id == current_user.id)
    
    swaps = query.order_by(Swap.created_at.desc()).offset(skip).limit(limit).all()
    return swaps

@router.get("/pending", response_model=List[SwapListResponse])
async def get_pending_swaps(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all pending swap requests for the current user"""
    pending_swaps = db.query(Swap).filter(
        Swap.requested_user_id == current_user.id,
        Swap.status == SwapStatus.PENDING
    ).order_by(Swap.created_at.desc()).all()
    
    return pending_swaps

@router.get("/{swap_id}", response_model=SwapDetailResponse)
async def get_swap_details(
    swap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed information about a specific swap"""
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    
    # Check if user is involved in this swap
    if swap.requester_id != current_user.id and swap.requested_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have access to this swap")
    
    return swap

# =============== SWAP RESPONSE MANAGEMENT ===============

@router.post("/{swap_id}/accept", response_model=SwapResponse)
async def accept_swap_request(
    swap_id: int,
    proposed_start_date: Optional[datetime] = None,
    meeting_location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept a swap request"""
    swap = db.query(Swap).filter(
        Swap.id == swap_id,
        Swap.requested_user_id == current_user.id,
        Swap.status == SwapStatus.PENDING
    ).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap request not found or not pending")
    
    # Check if response deadline has passed
    if swap.response_deadline and datetime.utcnow() > swap.response_deadline:
        swap.status = SwapStatus.REJECTED
        swap.rejection_reason = "Response deadline expired"
        swap.rejected_at = datetime.utcnow()
        db.commit()
        raise HTTPException(status_code=400, detail="Response deadline has passed")
    
    swap.status = SwapStatus.ACCEPTED
    if proposed_start_date:
        swap.proposed_start_date = proposed_start_date
    if meeting_location:
        swap.meeting_location = meeting_location
    
    db.commit()
    db.refresh(swap)
    
    return swap

@router.post("/{swap_id}/reject", response_model=SwapResponse)
async def reject_swap_request(
    swap_id: int,
    rejection_reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject a swap request"""
    swap = db.query(Swap).filter(
        Swap.id == swap_id,
        Swap.requested_user_id == current_user.id,
        Swap.status == SwapStatus.PENDING
    ).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap request not found or not pending")
    
    swap.status = SwapStatus.REJECTED
    swap.rejection_reason = rejection_reason
    swap.rejected_at = datetime.utcnow()
    
    db.commit()
    db.refresh(swap)
    
    return swap

# =============== SWAP PROGRESS MANAGEMENT ===============

@router.post("/{swap_id}/start", response_model=SwapResponse)
async def start_swap(
    swap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start an accepted swap"""
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    
    # Check if user is involved in this swap
    if swap.requester_id != current_user.id and swap.requested_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have access to this swap")
    
    if swap.status != SwapStatus.ACCEPTED:
        raise HTTPException(status_code=400, detail="Swap must be accepted before starting")
    
    swap.status = SwapStatus.IN_PROGRESS
    swap.actual_start_date = datetime.utcnow()
    
    db.commit()
    db.refresh(swap)
    
    return swap

@router.put("/{swap_id}/progress", response_model=SwapResponse)
async def update_swap_progress(
    swap_id: int,
    progress: int = Query(..., ge=0, le=100, description="Progress percentage (0-100)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update progress of a swap"""
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    
    if swap.status != SwapStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Swap must be in progress to update progress")
    
    # Update progress based on who is updating
    if swap.requester_id == current_user.id:
        swap.requester_progress = progress
    elif swap.requested_user_id == current_user.id:
        swap.requested_user_progress = progress
    else:
        raise HTTPException(status_code=403, detail="You don't have access to this swap")
    
    # If both users have completed (100% progress), mark swap as completed
    if swap.requester_progress == 100 and swap.requested_user_progress == 100:
        swap.status = SwapStatus.COMPLETED
        swap.completion_date = datetime.utcnow()
    
    db.commit()
    db.refresh(swap)
    
    return swap

@router.post("/{swap_id}/complete", response_model=SwapResponse)
async def complete_swap(
    swap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a swap as completed"""
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    
    # Check if user is involved in this swap
    if swap.requester_id != current_user.id and swap.requested_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have access to this swap")
    
    if swap.status != SwapStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Swap must be in progress to complete")
    
    swap.status = SwapStatus.COMPLETED
    swap.completion_date = datetime.utcnow()
    swap.requester_progress = 100
    swap.requested_user_progress = 100
    
    db.commit()
    db.refresh(swap)
    
    return swap

# =============== SWAP CANCELLATION ===============

@router.post("/{swap_id}/cancel", response_model=SwapResponse)
async def cancel_swap(
    swap_id: int,
    cancellation_reason: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a swap (requester can cancel if pending, both can cancel if accepted/in-progress)"""
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    
    # Check if user can cancel
    can_cancel = False
    if swap.status == SwapStatus.PENDING and swap.requester_id == current_user.id:
        can_cancel = True
    elif swap.status in [SwapStatus.ACCEPTED, SwapStatus.IN_PROGRESS]:
        if swap.requester_id == current_user.id or swap.requested_user_id == current_user.id:
            can_cancel = True
    
    if not can_cancel:
        raise HTTPException(status_code=403, detail="You cannot cancel this swap")
    
    if not swap.can_be_cancelled:
        raise HTTPException(status_code=400, detail="This swap cannot be cancelled")
    
    swap.status = SwapStatus.CANCELLED
    swap.cancelled_by = current_user.id
    swap.cancellation_reason = cancellation_reason
    swap.cancelled_at = datetime.utcnow()
    
    db.commit()
    db.refresh(swap)
    
    return swap

@router.delete("/{swap_id}")
async def delete_swap_request(
    swap_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a swap request (only if pending and user is requester)"""
    swap = db.query(Swap).filter(
        Swap.id == swap_id,
        Swap.requester_id == current_user.id,
        Swap.status == SwapStatus.PENDING
    ).first()
    
    if not swap:
        raise HTTPException(
            status_code=404, 
            detail="Swap request not found or cannot be deleted"
        )
    
    db.delete(swap)
    db.commit()
    
    return {"message": "Swap request deleted successfully"}

# =============== SWAP STATISTICS ===============

@router.get("/stats/summary")
async def get_swap_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get swap statistics for current user"""
    
    # Count swaps by status
    stats = {}
    for status in SwapStatus:
        count = db.query(Swap).filter(
            ((Swap.requester_id == current_user.id) | 
             (Swap.requested_user_id == current_user.id)),
            Swap.status == status
        ).count()
        stats[status.value] = count
    
    # Additional metrics
    success_rate = 0
    if stats['completed'] > 0 and (stats['completed'] + stats['cancelled'] + stats['rejected']) > 0:
        total_concluded = stats['completed'] + stats['cancelled'] + stats['rejected']
        success_rate = round((stats['completed'] / total_concluded) * 100, 2)
    
    return {
        "swap_counts": stats,
        "success_rate_percentage": success_rate,
        "total_swaps": sum(stats.values())
    }
