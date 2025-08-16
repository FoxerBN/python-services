from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
class LoginBody(BaseModel):
    username: str
    password: str    

    class ConfigDict:
        form_attributes = True
