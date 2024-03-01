from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.project import Project
from dependencies import get_db
from crud import crud_project


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Project])
def read_projects(skip: int = 0, limit: int = 100, category_id: int = None, db: Session = Depends(get_db)):
    return crud_project.get_projects(db, skip=skip, limit=limit, category_id=category_id)

@router.get("/count", response_model=int)
def read_projects_count(db: Session = Depends(get_db)):
    return crud_project.get_projects_count(db)


@router.get("/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud_project.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project