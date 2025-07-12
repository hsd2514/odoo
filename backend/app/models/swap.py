
# models/swap.py
# SQLAlchemy model for Swap
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from app.models import Base

class Swap(Base):
    __tablename__ = "swaps"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_offered = Column(Integer, ForeignKey("skills.id"), nullable=False)
    skill_requested = Column(Integer, ForeignKey("skills.id"), nullable=False)
    status = Column(String, default="pending")
    scheduled_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    message = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    feedback = Column(String, nullable=True)
