from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Post Models


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class PostDelete(BaseModel):
    id: str


class PostUpdate(BaseModel):
    update: list

# User Models


class User(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserDelete(BaseModel):
    id: str


class UserUpdate(BaseModel):
    id: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None


class UserResponse(User):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
