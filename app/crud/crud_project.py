from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import models


def get_projects(db: Session, skip: int = 0, limit: int = 100, category_id: int = None):
    return db.query(models.Project).filter(or_(models.Project.category_id == category_id, category_id == None)).offset(skip).limit(limit).all()

def get_projects_count(db: Session):
    return db.query(models.Project).count()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()
