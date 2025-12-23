from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime

class User(SQLModel, table=True):
    """Модель пользователя для SQL базы данных"""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    username: Optional[str] = None
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Связь с событиями (опционально, если нужна)
    # events: List["Event"] = Relationship(back_populates="user")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "fastapiuser",
                "password": "strong!!!"
            }
        }

class UserSignIn(SQLModel):
    """Модель для входа пользователя"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }

class UserCreate(SQLModel):
    """Модель для создания пользователя"""
    email: EmailStr
    username: Optional[str] = None
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "fastapiuser",
                "password": "strong!!!"
            }
        }