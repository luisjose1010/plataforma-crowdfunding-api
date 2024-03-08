from pydantic import BaseModel
from datetime import datetime
from .project import Project

class UserBase(BaseModel):
    id_card: str
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    id_card: str | None = None
    email: str | None = None
    name: str | None = None
    password: str | None = None
    new_password: str | None = None
    avatar: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None

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