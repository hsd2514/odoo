# database.py: DB engine and session for PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
