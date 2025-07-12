# routers/skills.py
# FastAPI routes for skills
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.skill import Skill, UserSkill, SkillRequest, SkillCategory, SkillLevel
from app.models.user import User
from app.schemas.skill import (
    SkillCreate, SkillResponse, UserSkillCreate, UserSkillUpdate, 
    UserSkillResponse, SkillRequestCreate, SkillRequestUpdate, SkillRequestResponse
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/skills", tags=["skills"])

# =============== SKILL MANAGEMENT ===============

@router.get("/", response_model=List[SkillResponse])
async def get_all_skills(
    category: Optional[SkillCategory] = None,
    search: Optional[str] = Query(None, min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all approved skills with optional filtering"""
    query = db.query(Skill).filter(Skill.is_approved == True, Skill.is_flagged == False)
    
    if category:
        query = query.filter(Skill.category == category)
    
    if search:
        query = query.filter(Skill.name.ilike(f"%{search}%"))
    
    skills = query.offset(skip).limit(limit).all()
    return skills

@router.post("/", response_model=SkillResponse)
async def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new skill"""
    # Check if skill already exists
    existing_skill = db.query(Skill).filter(Skill.name.ilike(skill.name)).first()
    if existing_skill:
        raise HTTPException(status_code=400, detail="Skill already exists")
    
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get a specific skill by ID"""
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.is_approved == True).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.get("/search/by-name")
async def search_skills_by_name(
    name: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search skills by name (for autocomplete)"""
    skills = db.query(Skill).filter(
        Skill.name.ilike(f"%{name}%"),
        Skill.is_approved == True,
        Skill.is_flagged == False
    ).limit(limit).all()
    
    return [{"id": skill.id, "name": skill.name, "category": skill.category} for skill in skills]

# =============== USER SKILLS (OFFERED) ===============

@router.get("/user/{user_id}/offered", response_model=List[UserSkillResponse])
async def get_user_offered_skills(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all skills offered by a specific user"""
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if profile is public or if it's the current user
    if not user.is_profile_public:
        # Add logic here to check if current user is the owner
        pass
    
    user_skills = db.query(UserSkill).filter(
        UserSkill.user_id == user_id,
        UserSkill.is_approved == True
    ).all()
    
    return user_skills

@router.post("/user/offered", response_model=UserSkillResponse)
async def add_user_skill(
    user_skill: UserSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a skill that the current user can offer"""
    # Check if skill exists
    skill = db.query(Skill).filter(Skill.id == user_skill.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Check if user already offers this skill
    existing = db.query(UserSkill).filter(
        UserSkill.user_id == current_user.id,
        UserSkill.skill_id == user_skill.skill_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="You already offer this skill")
    
    db_user_skill = UserSkill(
        user_id=current_user.id,
        **user_skill.dict()
    )
    
    db.add(db_user_skill)
    db.commit()
    db.refresh(db_user_skill)
    
    # Update skill offer count
    skill.offer_count += 1
    db.commit()
    
    return db_user_skill

@router.put("/user/offered/{user_skill_id}", response_model=UserSkillResponse)
async def update_user_skill(
    user_skill_id: int,
    skill_update: UserSkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a skill offered by the current user"""
    user_skill = db.query(UserSkill).filter(
        UserSkill.id == user_skill_id,
        UserSkill.user_id == current_user.id
    ).first()
    
    if not user_skill:
        raise HTTPException(status_code=404, detail="User skill not found")
    
    # Update only provided fields
    update_data = skill_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_skill, field, value)
    
    db.commit()
    db.refresh(user_skill)
    return user_skill

@router.delete("/user/offered/{user_skill_id}")
async def remove_user_skill(
    user_skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a skill offered by the current user"""
    user_skill = db.query(UserSkill).filter(
        UserSkill.id == user_skill_id,
        UserSkill.user_id == current_user.id
    ).first()
    
    if not user_skill:
        raise HTTPException(status_code=404, detail="User skill not found")
    
    # Update skill offer count
    skill = db.query(Skill).filter(Skill.id == user_skill.skill_id).first()
    if skill and skill.offer_count > 0:
        skill.offer_count -= 1
    
    db.delete(user_skill)
    db.commit()
    
    return {"message": "Skill removed successfully"}

# =============== SKILL REQUESTS (WANTED) ===============

@router.get("/user/{user_id}/wanted", response_model=List[SkillRequestResponse])
async def get_user_wanted_skills(
    user_id: int,
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all skills wanted by a specific user"""
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(SkillRequest).filter(SkillRequest.user_id == user_id)
    
    if active_only:
        query = query.filter(SkillRequest.is_active == True)
    
    skill_requests = query.all()
    return skill_requests

@router.post("/user/wanted", response_model=SkillRequestResponse)
async def add_skill_request(
    skill_request: SkillRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a skill that the current user wants to learn"""
    # Check if skill exists
    skill = db.query(Skill).filter(Skill.id == skill_request.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Check if user already has an active request for this skill
    existing = db.query(SkillRequest).filter(
        SkillRequest.user_id == current_user.id,
        SkillRequest.skill_id == skill_request.skill_id,
        SkillRequest.is_active == True
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="You already have an active request for this skill")
    
    db_skill_request = SkillRequest(
        user_id=current_user.id,
        **skill_request.dict()
    )
    
    db.add(db_skill_request)
    db.commit()
    db.refresh(db_skill_request)
    
    # Update skill request count
    skill.request_count += 1
    db.commit()
    
    return db_skill_request

@router.put("/user/wanted/{skill_request_id}", response_model=SkillRequestResponse)
async def update_skill_request(
    skill_request_id: int,
    request_update: SkillRequestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a skill request by the current user"""
    skill_request = db.query(SkillRequest).filter(
        SkillRequest.id == skill_request_id,
        SkillRequest.user_id == current_user.id
    ).first()
    
    if not skill_request:
        raise HTTPException(status_code=404, detail="Skill request not found")
    
    # Update only provided fields
    update_data = request_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(skill_request, field, value)
    
    db.commit()
    db.refresh(skill_request)
    return skill_request

@router.delete("/user/wanted/{skill_request_id}")
async def remove_skill_request(
    skill_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a skill request by the current user"""
    skill_request = db.query(SkillRequest).filter(
        SkillRequest.id == skill_request_id,
        SkillRequest.user_id == current_user.id
    ).first()
    
    if not skill_request:
        raise HTTPException(status_code=404, detail="Skill request not found")
    
    # Update skill request count
    skill = db.query(Skill).filter(Skill.id == skill_request.skill_id).first()
    if skill and skill.request_count > 0:
        skill.request_count -= 1
    
    db.delete(skill_request)
    db.commit()
    
    return {"message": "Skill request removed successfully"}

# =============== SKILL MATCHING ===============

@router.get("/matches/for-user", response_model=List[UserSkillResponse])
async def find_skill_matches(
    skill_id: Optional[int] = Query(None),
    level: Optional[SkillLevel] = None,
    remote_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Find users who offer skills that the current user wants to learn"""
    # Get current user's skill requests
    user_requests = db.query(SkillRequest).filter(
        SkillRequest.user_id == current_user.id,
        SkillRequest.is_active == True
    ).all()
    
    if not user_requests and not skill_id:
        raise HTTPException(status_code=400, detail="No active skill requests found")
    
    # Build query for matching user skills
    if skill_id:
        skill_ids = [skill_id]
    else:
        skill_ids = [req.skill_id for req in user_requests]
    
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
