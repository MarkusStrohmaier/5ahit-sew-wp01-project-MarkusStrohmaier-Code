from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.userRole import UserRole

class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=15)
    email: EmailStr = Field(..., min_length=7, max_length=50)
    role: UserRole = UserRole.VISITOR

class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=50)

class UserUpdate(UserBase):
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str