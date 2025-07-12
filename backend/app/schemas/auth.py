from pydantic import BaseModel, EmailStr

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class AuthRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
