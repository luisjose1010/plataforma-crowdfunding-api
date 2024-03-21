from pydantic import BaseModel
from datetime import datetime
from .user import ProjectUser

class TransactionBase(BaseModel):
    reference_number: str
    payment_system: str
    amount: float
    user_id: int
    project_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    is_verified: bool

class Transaction(TransactionBase):
    id: int
    is_verified: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TransactionProjectUser(Transaction):
    project: ProjectUser