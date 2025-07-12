# database.py: DB engine and session for PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.models.user import Base as UserBase
from app.models.skill import Base as SkillBase
from app.models.swap import Base as SwapBase
from app.models.feedback import Base as FeedbackBase
from app.models.badge import Base as BadgeBase
from app.models.invite import Base as InviteBase

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables at startup
UserBase.metadata.create_all(bind=engine)
SkillBase.metadata.create_all(bind=engine)
SwapBase.metadata.create_all(bind=engine)
FeedbackBase.metadata.create_all(bind=engine)
BadgeBase.metadata.create_all(bind=engine)
InviteBase.metadata.create_all(bind=engine)

# Dependency for FastAPI to get a DB session
from typing import Generator

def get_db() -> Generator:
    """
    Yields a SQLAlchemy database session and ensures it is closed after use.
    Example usage in FastAPI:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
