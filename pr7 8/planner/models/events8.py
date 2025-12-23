from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional, List
from datetime import datetime

class Event(SQLModel, table=True):
    """Модель события для SQL базы данных"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    # Связь с пользователем
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }

class EventUpdate(SQLModel):
    """Модель для обновления события"""
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Event Title",
                "location": "New Location"
            }
        }