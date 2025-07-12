# routers/feedback.py
# FastAPI routes for feedback and ratings
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.feedback import Feedback, FeedbackType
from app.models.swap import Swap, SwapStatus
from app.models.user import User
from app.schemas.feedback import (
    FeedbackCreate, FeedbackResponse, FeedbackUpdate,
    FeedbackListResponse, FeedbackSummary
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/feedback", tags=["feedback"])

# =============== FEEDBACK CREATION ===============

@router.post("/", response_model=FeedbackResponse)
async def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create feedback/rating for another user"""
    # Validate receiver exists
    receiver = db.query(User).filter(
        User.id == feedback.receiver_id,
        User.is_active == True
    ).first()
    
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    # Cannot give feedback to yourself
    if feedback.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot give feedback to yourself")
    
    # If swap_id is provided, validate the swap
    if feedback.swap_id:
        swap = db.query(Swap).filter(Swap.id == feedback.swap_id).first()
        if not swap:
            raise HTTPException(status_code=404, detail="Swap not found")
        
        # Check if user was involved in the swap
        if swap.requester_id != current_user.id and swap.requested_user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You were not involved in this swap")
        
        # Check if swap is completed
        if swap.status != SwapStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Can only give feedback for completed swaps")
        
        # Check if feedback already exists for this swap from this user
        existing_feedback = db.query(Feedback).filter(
            Feedback.swap_id == feedback.swap_id,
            Feedback.giver_id == current_user.id
        ).first()
        
        if existing_feedback:
            raise HTTPException(status_code=400, detail="You have already given feedback for this swap")
    
    # Create feedback
    db_feedback = Feedback(
        giver_id=current_user.id,
        **feedback.dict()
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    # Update receiver's rating
    _update_user_rating(db, feedback.receiver_id)
    
    return db_feedback

# =============== FEEDBACK RETRIEVAL ===============

@router.get("/user/{user_id}", response_model=List[FeedbackListResponse])
async def get_user_feedback(
    user_id: int,
    feedback_type: Optional[FeedbackType] = None,
    public_only: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get feedback received by a user"""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(Feedback).filter(
        Feedback.receiver_id == user_id,
        Feedback.is_hidden == False
    )
    
    if public_only:
        query = query.filter(Feedback.is_public == True)
    
    if feedback_type:
        query = query.filter(Feedback.feedback_type == feedback_type)
    
    feedback_list = query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    return feedback_list

@router.get("/user/{user_id}/summary", response_model=FeedbackSummary)
async def get_user_feedback_summary(user_id: int, db: Session = Depends(get_db)):
    """Get feedback summary for a user"""
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all public feedback for the user
    feedback_query = db.query(Feedback).filter(
        Feedback.receiver_id == user_id,
        Feedback.is_public == True,
        Feedback.is_hidden == False
    )
    
    all_feedback = feedback_query.all()
    
    if not all_feedback:
        return FeedbackSummary(
            user_id=user_id,
            total_feedback=0,
            average_rating=0.0,
            rating_distribution={},
            recent_feedback=[]
        )
    
    # Calculate statistics
    ratings = [f.rating for f in all_feedback]
    total_feedback = len(ratings)
    average_rating = round(sum(ratings) / total_feedback, 2)
    
    # Rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[str(i)] = ratings.count(i)
    
    # Recent feedback (last 5)
    recent_feedback = feedback_query.order_by(Feedback.created_at.desc()).limit(5).all()
    
    return FeedbackSummary(
        user_id=user_id,
        total_feedback=total_feedback,
        average_rating=average_rating,
        rating_distribution=rating_distribution,
        recent_feedback=recent_feedback
    )

@router.get("/my-given", response_model=List[FeedbackListResponse])
async def get_my_given_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get feedback given by current user"""
    feedback_list = db.query(Feedback).filter(
        Feedback.giver_id == current_user.id
    ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    return feedback_list

@router.get("/my-received", response_model=List[FeedbackListResponse])
async def get_my_received_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get feedback received by current user"""
    feedback_list = db.query(Feedback).filter(
        Feedback.receiver_id == current_user.id,
        Feedback.is_hidden == False
    ).order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    return feedback_list

# =============== FEEDBACK MANAGEMENT ===============

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific feedback details"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Check access permissions
    can_access = (
        feedback.giver_id == current_user.id or
        feedback.receiver_id == current_user.id or
        (feedback.is_public and not feedback.is_hidden)
    )
    
    if not can_access:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update feedback (only by the feedback giver)"""
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id,
        Feedback.giver_id == current_user.id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found or not owned by you")
    
    # Update only provided fields
    update_data = feedback_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(feedback, field, value)
    
    db.commit()
    db.refresh(feedback)
    
    # Update receiver's rating if rating was changed
    if 'rating' in update_data:
        _update_user_rating(db, feedback.receiver_id)
    
    return feedback

@router.post("/{feedback_id}/respond")
async def respond_to_feedback(
    feedback_id: int,
    response: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Respond to feedback (only by the feedback receiver)"""
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id,
        Feedback.receiver_id == current_user.id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found or not for you")
    
    feedback.response = response
    feedback.response_date = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Response added successfully"}

@router.post("/{feedback_id}/helpful")
async def mark_feedback_helpful(
    feedback_id: int,
    is_helpful: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark feedback as helpful or not helpful"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if feedback.giver_id == current_user.id or feedback.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot vote on your own feedback")
    
    # In a real application, you'd track individual votes to prevent duplicate voting
    # For now, we'll just increment the counters
    if is_helpful:
        feedback.helpful_votes += 1
    else:
        feedback.not_helpful_votes += 1
    
    db.commit()
    
    return {"message": "Vote recorded successfully"}

@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete feedback (only by the feedback giver)"""
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id,
        Feedback.giver_id == current_user.id
    ).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found or not owned by you")
    
    receiver_id = feedback.receiver_id
    
    db.delete(feedback)
    db.commit()
    
    # Update receiver's rating after deletion
    _update_user_rating(db, receiver_id)
    
    return {"message": "Feedback deleted successfully"}

# =============== HELPER FUNCTIONS ===============

def _update_user_rating(db: Session, user_id: int):
    """Update user's overall rating based on all feedback received"""
    from datetime import datetime
    
    feedback_list = db.query(Feedback).filter(
        Feedback.receiver_id == user_id,
        Feedback.is_hidden == False
    ).all()
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    if feedback_list:
        total_rating = sum(f.rating for f in feedback_list)
        rating_count = len(feedback_list)
        user.total_rating = total_rating
        user.rating_count = rating_count
    else:
        user.total_rating = 0
        user.rating_count = 0
    
    db.commit()
