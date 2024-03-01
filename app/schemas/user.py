from pydantic import BaseModel
from datetime import datetime
from .project import Project

class UserBase(BaseModel):
    id_card: str
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    avatar: str | None = None
    is_active: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserProjects(User):
    id: int
    projects: list[Project] = []

    class Config:
        orm_mode = True