from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: str | None = None
    donated: float
    goal: float
    category_id: int

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True