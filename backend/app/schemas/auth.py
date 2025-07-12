# schemas/auth.py
# Pydantic schemas for authentication
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserLogin(BaseModel):
    email_or_username: str = Field(..., description="Email address or username")
    password: str = Field(..., min_length=6, description="User password")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: int
    username: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

class PasswordReset(BaseModel):
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=6, description="New password")

class EmailVerification(BaseModel):
    token: str = Field(..., description="Email verification token")
