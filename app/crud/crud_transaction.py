from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import models
from schemas.transaction import TransactionCreate, TransactionUpdate
from schemas.project import ProjectCreate
from core.hashing import Hasher


def get_transactions(db: Session, is_verified: bool = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Transaction)
    query = query.filter(or_(models.Transaction.is_verified == is_verified, is_verified == None))
    return query.offset(skip).limit(limit).all()

def get_transactions_count(db: Session):
    return db.query(models.Transaction).count()

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_project = None
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id)
    db_transaction.update(transaction.model_dump())
    db_transaction = db_transaction.first()

    db_project = db.query(models.Project).filter(models.Project.id == db_transaction.project_id)
    db_project_item = db_project.first()
    db_project.update({ "donated": db_project_item.donated + db_transaction.amount })
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
