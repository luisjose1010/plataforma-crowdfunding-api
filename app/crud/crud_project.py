from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import models
from schemas.project import ProjectUpdate


def get_projects(db: Session, skip: int = 0, limit: int = 100, category_id: int = None, is_verified: bool = None):
    query = db.query(models.Project)
    query = query.filter(or_(models.Project.category_id == category_id, category_id == None))
    query = query.filter(or_(models.Project.is_verified == is_verified, is_verified == None))
    return query.offset(skip).limit(limit).all()

def get_projects_count(db: Session):
    return db.query(models.Project).count()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id)
    db_project.update(project.model_dump(exclude_unset=True, exclude=['is_verified'])) # Esta funcion no verifica proyectos
    db.commit()
    return db_project.first()

def verify_project(db: Session, project_id: int, is_verified: bool = True):
    db_project = db.query(models.Project).filter(models.Project.id == project_id)
    db_project.update({'is_verified': is_verified})
    db.commit()
    return db_project.first()


def delete_project(db: Session, project_id: int):
    deleted = db.query(models.Project).filter(models.Project.id == project_id).delete()
    db.commit()
    return deleted;


def is_owner(db, project_id, user) -> bool:
    print(user.id == get_project(db, project_id).user_id)
    return user.id == get_project(db, project_id).user_id