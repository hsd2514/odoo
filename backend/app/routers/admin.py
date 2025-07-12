# routers/admin.py
# FastAPI routes for admin functionality
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User, UserRole
from app.models.skill import Skill, UserSkill, SkillRequest
from app.models.swap import Swap, SwapStatus
from app.models.feedback import Feedback
from app.models.invite import Invite
from app.schemas.user import UserResponse
from app.schemas.skill import SkillResponse
from app.schemas.swap import SwapResponse
from app.schemas.feedback import FeedbackResponse
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

# =============== USER MANAGEMENT ===============

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    is_active: Optional[bool] = None,
    is_banned: Optional[bool] = None,
    role: Optional[UserRole] = None,
    search: Optional[str] = Query(None, min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all users with filtering (Admin only)"""
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if is_banned is not None:
        query = query.filter(User.is_banned == is_banned)
    
    if role:
        query = query.filter(User.role == role)
    
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%")) |
            (User.full_name.ilike(f"%{search}%"))
        )
    
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users

@router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    ban_reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Ban a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Cannot ban admin users")
    
    user.is_banned = True
    user.is_active = False
    user.ban_reason = ban_reason
    user.banned_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": f"User {user.username} has been banned", "reason": ban_reason}

@router.post("/users/{user_id}/unban")
async def unban_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Unban a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_banned = False
    user.is_active = True
    user.ban_reason = None
    user.banned_at = None
    
    db.commit()
    
    return {"message": f"User {user.username} has been unbanned"}

@router.post("/users/{user_id}/make-admin")
async def make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Make a user an admin (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_banned:
        raise HTTPException(status_code=400, detail="Cannot make banned user an admin")
    
    user.role = UserRole.ADMIN
    db.commit()
    
    return {"message": f"User {user.username} is now an admin"}

# =============== SKILL MODERATION ===============

@router.get("/skills/flagged", response_model=List[SkillResponse])
async def get_flagged_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all flagged skills (Admin only)"""
    flagged_skills = db.query(Skill).filter(Skill.is_flagged == True).all()
    return flagged_skills

@router.post("/skills/{skill_id}/approve")
async def approve_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Approve a skill (Admin only)"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    skill.is_approved = True
    skill.is_flagged = False
    skill.flag_reason = None
    
    db.commit()
    
    return {"message": f"Skill '{skill.name}' has been approved"}

@router.post("/skills/{skill_id}/reject")
async def reject_skill(
    skill_id: int,
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Reject a skill (Admin only)"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    skill.is_approved = False
    skill.is_flagged = True
    skill.flag_reason = reason
    
    db.commit()
    
    return {"message": f"Skill '{skill.name}' has been rejected", "reason": reason}

@router.get("/user-skills/flagged")
async def get_flagged_user_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all flagged user skills (Admin only)"""
    flagged_user_skills = db.query(UserSkill).filter(UserSkill.is_flagged == True).all()
    return flagged_user_skills

@router.post("/user-skills/{user_skill_id}/approve")
async def approve_user_skill(
    user_skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Approve a user skill (Admin only)"""
    user_skill = db.query(UserSkill).filter(UserSkill.id == user_skill_id).first()
    
    if not user_skill:
        raise HTTPException(status_code=404, detail="User skill not found")
    
    user_skill.is_approved = True
    user_skill.is_flagged = False
    user_skill.flag_reason = None
    
    db.commit()
    
    return {"message": "User skill has been approved"}

@router.post("/user-skills/{user_skill_id}/reject")
async def reject_user_skill(
    user_skill_id: int,
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Reject a user skill (Admin only)"""
    user_skill = db.query(UserSkill).filter(UserSkill.id == user_skill_id).first()
    
    if not user_skill:
        raise HTTPException(status_code=404, detail="User skill not found")
    
    user_skill.is_approved = False
    user_skill.is_flagged = True
    user_skill.flag_reason = reason
    
    db.commit()
    
    return {"message": "User skill has been rejected", "reason": reason}

# =============== SWAP MONITORING ===============

@router.get("/swaps", response_model=List[SwapResponse])
async def get_all_swaps(
    status: Optional[SwapStatus] = None,
    flagged_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all swaps with filtering (Admin only)"""
    query = db.query(Swap)
    
    if status:
        query = query.filter(Swap.status == status)
    
    if flagged_only:
        query = query.filter(Swap.is_flagged == True)
    
    swaps = query.order_by(Swap.created_at.desc()).offset(skip).limit(limit).all()
    return swaps

@router.post("/swaps/{swap_id}/flag")
async def flag_swap(
    swap_id: int,
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Flag a swap (Admin only)"""
    swap = db.query(Swap).filter(Swap.id == swap_id).first()
    
    if not swap:
        raise HTTPException(status_code=404, detail="Swap not found")
    
    swap.is_flagged = True
    swap.flag_reason = reason
    swap.admin_notes = f"Flagged by admin {current_user.username} on {datetime.utcnow()}"
    
    db.commit()
    
    return {"message": "Swap has been flagged", "reason": reason}

# =============== FEEDBACK MODERATION ===============

@router.get("/feedback/flagged", response_model=List[FeedbackResponse])
async def get_flagged_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all flagged feedback (Admin only)"""
    flagged_feedback = db.query(Feedback).filter(Feedback.is_flagged == True).all()
    return flagged_feedback

@router.post("/feedback/{feedback_id}/hide")
async def hide_feedback(
    feedback_id: int,
    reason: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Hide feedback (Admin only)"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.is_hidden = True
    feedback.is_flagged = True
    feedback.flag_reason = reason
    feedback.admin_notes = f"Hidden by admin {current_user.username} on {datetime.utcnow()}"
    
    db.commit()
    
    return {"message": "Feedback has been hidden", "reason": reason}

@router.post("/feedback/{feedback_id}/unhide")
async def unhide_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Unhide feedback (Admin only)"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.is_hidden = False
    feedback.is_flagged = False
    feedback.flag_reason = None
    
    db.commit()
    
    return {"message": "Feedback has been unhidden"}

# =============== PLATFORM MESSAGING ===============

@router.post("/broadcast")
async def send_platform_message(
    title: str = Body(...),
    message: str = Body(...),
    target_all: bool = Body(True),
    target_user_ids: Optional[List[int]] = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Send platform-wide message (Admin only)"""
    # In a real application, you would implement a notification system
    # For now, we'll just log the message and return success
    
    if target_all:
        target_count = db.query(User).filter(User.is_active == True).count()
        message_log = f"Broadcast message sent to all {target_count} active users"
    else:
        target_count = len(target_user_ids) if target_user_ids else 0
        message_log = f"Message sent to {target_count} specific users"
    
    # In a real app, you would store this in a messages/notifications table
    # and implement WebSocket or push notifications
    
    return {
        "message": "Platform message sent successfully",
        "title": title,
        "content": message,
        "target_count": target_count,
        "sent_by": current_user.username,
        "sent_at": datetime.utcnow()
    }

# =============== REPORTS AND ANALYTICS ===============

@router.get("/reports/user-activity")
async def get_user_activity_report(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get user activity report (Admin only)"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # New user registrations
    new_users = db.query(User).filter(
        User.created_at >= start_date,
        User.created_at <= end_date
    ).count()
    
    # Active users (users who have logged in or performed actions)
    total_active_users = db.query(User).filter(User.is_active == True).count()
    
    # Banned users
    banned_users = db.query(User).filter(User.is_banned == True).count()
    
    return {
        "period_days": days,
        "start_date": start_date,
        "end_date": end_date,
        "new_users_registered": new_users,
        "total_active_users": total_active_users,
        "banned_users": banned_users,
        "total_users": db.query(User).count()
    }

@router.get("/reports/swap-stats")
async def get_swap_statistics_report(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get swap statistics report (Admin only)"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Swap counts by status
    swap_stats = {}
    for status in SwapStatus:
        count = db.query(Swap).filter(
            Swap.status == status,
            Swap.created_at >= start_date,
            Swap.created_at <= end_date
        ).count()
        swap_stats[status.value] = count
    
    # Success rate
    total_concluded = (swap_stats.get('completed', 0) + 
                      swap_stats.get('cancelled', 0) + 
                      swap_stats.get('rejected', 0))
    
    success_rate = 0
    if total_concluded > 0:
        success_rate = round((swap_stats.get('completed', 0) / total_concluded) * 100, 2)
    
    return {
        "period_days": days,
        "swap_counts": swap_stats,
        "success_rate_percentage": success_rate,
        "total_swaps": sum(swap_stats.values())
    }

@router.get("/reports/feedback-logs")
async def get_feedback_report(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get feedback and rating report (Admin only)"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Feedback statistics
    total_feedback = db.query(Feedback).filter(
        Feedback.created_at >= start_date,
        Feedback.created_at <= end_date
    ).count()
    
    # Average ratings
    avg_rating = db.query(func.avg(Feedback.rating)).filter(
        Feedback.created_at >= start_date,
        Feedback.created_at <= end_date
    ).scalar()
    
    # Rating distribution
    rating_distribution = {}
    for rating in range(1, 6):
        count = db.query(Feedback).filter(
            Feedback.rating == rating,
            Feedback.created_at >= start_date,
            Feedback.created_at <= end_date
        ).count()
        rating_distribution[str(rating)] = count
    
    # Flagged feedback
    flagged_feedback = db.query(Feedback).filter(
        Feedback.is_flagged == True,
        Feedback.created_at >= start_date,
        Feedback.created_at <= end_date
    ).count()
    
    return {
        "period_days": days,
        "total_feedback": total_feedback,
        "average_rating": round(avg_rating, 2) if avg_rating else 0,
        "rating_distribution": rating_distribution,
        "flagged_feedback": flagged_feedback
    }

@router.get("/reports/export/csv")
async def export_reports_csv(
    report_type: str = Query(..., regex="^(users|swaps|feedback)$"),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Export reports as CSV (Admin only)"""
    # In a real application, you would generate actual CSV files
    # For now, we'll return a message indicating the export type
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    return {
        "message": f"CSV export prepared for {report_type} data",
        "report_type": report_type,
        "period": f"{start_date.date()} to {end_date.date()}",
        "note": "In production, this would return a downloadable CSV file"
    }
