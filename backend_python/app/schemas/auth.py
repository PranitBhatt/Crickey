"""
Authentication schemas.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str
    name: str
    role: UserRole
    phone: Optional[str] = None


class UserResponse(BaseModel):
    """User response model"""
    id: int
    email: str
    name: str
    role: UserRole
    phone: Optional[str]
    team_id: Optional[int]
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token data"""
    user_id: Optional[int] = None
    email: Optional[str] = None

