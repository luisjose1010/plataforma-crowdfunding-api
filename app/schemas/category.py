from datetime import datetime
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str
    url: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    projects_count: int

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True