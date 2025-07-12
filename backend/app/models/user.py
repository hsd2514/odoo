
# models/user.py
# SQLAlchemy model for User
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    location = Column(String, nullable=True)
    availability = Column(String, nullable=True)
    is_public = Column(Boolean, default=True)
    photo_url = Column(String, nullable=True)
