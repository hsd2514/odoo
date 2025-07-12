
# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from passlib.context import CryptContext
from jose import jwt
from app.config import SECRET_KEY

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Explicit OPTIONS handler for CORS preflight
@router.options("/auth/register")
def options_register():
    return {}

# POST /auth/register – Register
@router.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        location=user.location,
        availability=user.availability,
        is_public=user.is_public,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Explicit OPTIONS handler for CORS preflight
@router.options("/auth/login")
def options_login():
    return {}



# POST /auth/login – Login (returns real JWT token)
@router.post("/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Return a real JWT token
    from datetime import datetime, timedelta
    payload = {
        "sub": str(db_user.id),
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
