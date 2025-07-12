
# models/badge.py
# SQLAlchemy model for Badge
from sqlalchemy import Column, Integer, String, ForeignKey

from app.models import Base

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=True)
    badge_type = Column(String, nullable=False)  # learned, mentor, rated_5star
