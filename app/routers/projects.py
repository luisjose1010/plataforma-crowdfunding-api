from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from schemas.project import Project, ProjectUpdate
from dependencies import get_db, get_token_subject
from crud import crud_project, crud_user


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    is_verified: bool = None,
    db: Session = Depends(get_db)
):
    return crud_project.get_projects(db, skip=skip, limit=limit, category_id=category_id, is_verified=is_verified)

@router.get("/count/", response_model=int)
def read_projects_count(db: Session = Depends(get_db)):
    return crud_project.get_projects_count(db)


@router.get("/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud_project.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    token_user = crud_user.get_user(db, user_id=token_subject)
    if not token_user.is_superuser and not crud_project.is_owner(db, project_id, token_user):
        raise HTTPException(status_code=403, detail="User not authorized, need owner or superuser")
    db_project = crud_project.update_project(db, project_id=project_id, project=project)
    
    if token_user.is_superuser and not project.is_verified == None:
        db_project = crud_project.verify_project(db, project_id, project.is_verified)
    return db_project

@router.delete("/{project_id}")
def update_project(
    project_id: int,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
)-> int:
    token_user = crud_user.get_user(db, user_id=token_subject)
    if not token_user.is_superuser and not crud_project.is_owner(db, project_id, token_user):
        raise HTTPException(status_code=403, detail="User not authorized, need owner or superuser")
    db_project = crud_project.delete_project(db, project_id=project_id)
    return db_project