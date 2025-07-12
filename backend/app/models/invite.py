
# models/invite.py
# SQLAlchemy model for Invite
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.models import Base

class Invite(Base):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    message = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    rating = Column(Integer, nullable=True)
    feedback = Column(String, nullable=True)
