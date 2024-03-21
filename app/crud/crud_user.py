from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import models
from schemas.user import UserCreate, UserUpdate
from schemas.project import ProjectCreate
from core.hashing import Hasher


def get_users(db: Session, id_card: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.User)
    query = query.filter(or_(models.User.id_card == id_card, id_card == None))
    return query.offset(skip).limit(limit).all()

def get_users_count(db: Session):
    return db.query(models.User).count()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.User(**user.model_dump(exclude={'password'}), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_project(db: Session, project: ProjectCreate, user_id: int):
    db_item = models.Project(**project.model_dump(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_user(db: Session, user_id: int, user: UserUpdate, token_user: models.User = None):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    if user.new_password:
        hashed_password = Hasher.get_password_hash(user.new_password)
        db_user.update({"password": hashed_password})
    if not user.is_superuser == None and token_user.is_superuser:
        db_user.update({"is_superuser": user.is_superuser})
    db_user.update(user.model_dump(exclude_unset=True, exclude=["password", "new_password", "is_superuser"]))
    db.commit()
    return db_user.first()