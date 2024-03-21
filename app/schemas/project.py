from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: str | None = None
    goal: float
    category_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_verified: bool | None = None
    category_id: int | None = None

class Project(ProjectBase):
    id: int
    donated: float
    is_verified: bool
    user_id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True