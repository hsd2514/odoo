
# models/feedback.py
# SQLAlchemy model for Feedback
from sqlalchemy import Column, Integer, String, ForeignKey

from app.models import Base

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    swap_id = Column(Integer, ForeignKey("swaps.id"), nullable=False)
    from_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
