# routers/invites.py
# FastAPI routes for invites (skeleton)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.invite import Invite
from app.models.user import User
from app.models.skill import Skill
from app.schemas.invite import InviteCreate, InviteUpdate, InviteResponse
from app.utils.jwt import get_current_user_jwt

router = APIRouter(prefix="/invites", tags=["Invites"])

def get_current_user(user=Depends(get_current_user_jwt)):
    return user.id


# Helper to enrich invite with user/skill names
def enrich_invite(invite, db):
    sender = db.query(User).filter_by(id=invite.sender_id).first()
    receiver = db.query(User).filter_by(id=invite.receiver_id).first()
    skill = db.query(Skill).filter_by(id=invite.skill_id).first()
    return {
        'id': invite.id,
        'sender_id': invite.sender_id,
        'receiver_id': invite.receiver_id,
        'skill_id': invite.skill_id,
        'sender_name': sender.name if sender else str(invite.sender_id),
        'receiver_name': receiver.name if receiver else str(invite.receiver_id),
        'skill_name': skill.name if skill else str(invite.skill_id),
        'message': getattr(invite, 'message', None),
        'status': invite.status,
        'created_at': invite.created_at,
        'rating': invite.rating,
        'feedback': invite.feedback
    }
# POST /invites/{invite_id}/feedback – Submit feedback/rating for an invite
from fastapi import Body
@router.post("/{invite_id}/feedback", response_model=InviteResponse)
def submit_invite_feedback(invite_id: int, rating: int = Body(...), feedback: str = Body(""), db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    invite = db.query(Invite).filter(Invite.id == invite_id).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    # Only the sender can rate the receiver
    if invite.sender_id != current_user:
        raise HTTPException(status_code=403, detail="Only the sender can rate the receiver.")
    invite.rating = rating
    invite.feedback = feedback
    db.commit()
    db.refresh(invite)
    return enrich_invite(invite, db)

@router.post("/", response_model=InviteResponse)
def create_invite(invite: InviteCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_invite = Invite(
        sender_id=current_user,
        receiver_id=invite.receiver_id,
        skill_id=invite.skill_id,
        message=getattr(invite, "message", None),
        status="pending"
    )
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return enrich_invite(db_invite, db)

@router.get("/incoming", response_model=List[InviteResponse])
def get_incoming_invites(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    invites = db.query(Invite).filter(Invite.receiver_id == current_user).all()
    return [enrich_invite(i, db) for i in invites]

@router.get("/outgoing", response_model=List[InviteResponse])
def get_outgoing_invites(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    invites = db.query(Invite).filter(Invite.sender_id == current_user).all()
    return [enrich_invite(i, db) for i in invites]

@router.put("/{invite_id}", response_model=InviteResponse)
def update_invite_status(invite_id: int, update: InviteUpdate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    invite = db.query(Invite).filter(Invite.id == invite_id).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    invite.status = update.status
    db.commit()
    db.refresh(invite)
    return enrich_invite(invite, db)
