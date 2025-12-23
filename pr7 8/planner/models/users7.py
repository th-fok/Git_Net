from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from models.events8 import Event

class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = []
    
    model_config = ConfigDict(  # Новый стиль конфигурации Pydantic v2
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
                "events": []
            }
        }
    )

class NewUser(User):
    pass

class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!"
            }
        }
    )