
# routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.skill import Skill
from app.models.swap import Swap

router = APIRouter()

# GET /admin/users
@router.get("/admin/users", response_model=List[dict])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {"id": u.id, "name": u.name, "email": u.email, "is_public": u.is_public}
        for u in users
    ]

# DELETE /admin/users/{id}
@router.delete("/admin/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

# GET /admin/skills/pending
@router.get("/admin/skills/pending", response_model=List[dict])
def list_pending_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).filter(Skill.is_approved == 0).all()
    return [
        {"id": s.id, "name": s.name, "category": s.category}
        for s in skills
    ]

# DELETE /admin/skills/{id}
@router.delete("/admin/skills/{id}")
def delete_skill(id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted"}

# GET /admin/swaps
@router.get("/admin/swaps", response_model=List[dict])
def list_swaps(db: Session = Depends(get_db)):
    swaps = db.query(Swap).all()
    return [
        {"id": s.id, "sender_id": s.sender_id, "receiver_id": s.receiver_id, "status": s.status}
        for s in swaps
    ]

# POST /admin/announcements
@router.post("/admin/announcements")
def create_announcement(message: str):
    # For hackathon, just echo the message
    return {"message": f"Announcement posted: {message}"}
