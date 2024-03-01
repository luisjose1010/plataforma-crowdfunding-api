from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import models


def get_categories(db: Session, skip: int = 0, limit: int = 100, url: str = None):
    return db.query(models.Category).filter(or_(models.Category.url == url, url == None)).offset(skip).limit(limit).all()

def get_categories_count(db: Session):
    return db.query(models.Category).count()

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()