
# models/skill.py
# SQLAlchemy models for skills and related entities
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enum for skill level
class SkillLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

# Skill Category model (simple string for now)
class SkillCategory(Base):
    __tablename__ = "skill_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# Skill model
class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    is_approved = Column(Integer, default=1)  # 1=True, 0=False
    is_flagged = Column(Integer, default=0)
    offer_count = Column(Integer, default=0)
    request_count = Column(Integer, default=0)

# Association table for user skills (offered/wanted)
class UserSkill(Base):
    __tablename__ = "user_skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    type = Column(String, nullable=False)  # "offered" or "wanted"
    level = Column(Enum(SkillLevel), default=SkillLevel.beginner)
    is_approved = Column(Integer, default=1)  # 1=True, 0=False
    can_teach_remotely = Column(Integer, default=0)
    proficiency_level = Column(Enum(SkillLevel), default=SkillLevel.beginner)

# Skill request model (for requesting a skill swap or mentorship)
class SkillRequest(Base):
    __tablename__ = "skill_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    message = Column(String, nullable=True)
    is_active = Column(Integer, default=1)  # 1=True, 0=False
