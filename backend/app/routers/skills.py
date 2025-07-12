# routers/skills.py
# FastAPI routes for skills



# routers/skills.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.skill import Skill, UserSkill
from app.models.user import User
from app.schemas.skill import SkillCreate, SkillResponse, UserSkillCreate, UserSkillResponse
from app.utils.auth import get_current_user

router = APIRouter()

# GET /skills/ - List all skills
@router.get("/skills/", response_model=List[SkillResponse])
async def list_skills(db: Session = Depends(get_db)):
    """Get all skills."""
    return db.query(Skill).all()

# POST /skills/ - Create a new skill
@router.post("/skills/", response_model=SkillResponse)
async def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    """Create a new skill."""
    existing = db.query(Skill).filter(Skill.name.ilike(skill.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# POST /users/me/skills - Add a skill to the current user
@router.post("/users/me/skills", response_model=UserSkillResponse)
async def add_user_skill(
    user_skill: UserSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a skill to the current user."""
    skill = db.query(Skill).filter(Skill.id == user_skill.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    existing = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == user_skill.skill_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already added")
    db_user_skill = UserSkill(user_id=current_user.id, **user_skill.dict())
    db.add(db_user_skill)
    db.commit()
    db.refresh(db_user_skill)
    return db_user_skill

# DELETE /users/me/skills/{id} - Remove a skill from the current user
@router.delete("/users/me/skills/{id}")
async def remove_user_skill(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a skill from the current user."""
    user_skill = db.query(UserSkill).filter(
        UserSkill.id == id,
        UserSkill.user_id == current_user.id
    ).first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="User skill not found")
    db.delete(user_skill)
    db.commit()
    return {"message": "Skill removed from user"}
    # ...existing code...
    
    query = db.query(UserSkill).filter(
        UserSkill.skill_id.in_(skill_ids),
        UserSkill.user_id != current_user.id,  # Exclude self
        UserSkill.is_approved == True
    )
    
    if level:
        query = query.filter(UserSkill.proficiency_level == level)
    
    if remote_only:
        query = query.filter(UserSkill.can_teach_remotely == True)
    
    matches = query.offset(skip).limit(limit).all()
    return matches
