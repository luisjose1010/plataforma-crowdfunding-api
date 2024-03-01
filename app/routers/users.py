from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import User, UserCreate, UserProjects
from schemas.project import Project, ProjectCreate
from dependencies import get_db
from crud import crud_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/count", response_model=int)
def read_users_count(db: Session = Depends(get_db)):
    return crud_user.get_users_count(db)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/projects/", response_model=UserProjects)
def read_project_of_user(user_id: int, db: Session = Depends(get_db)):
    db_project = crud_user.get_user(db, user_id=user_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_project

@router.post("/{user_id}/projects/", response_model=Project)
def create_project_for_user(
    user_id: int, project: ProjectCreate, db: Session = Depends(get_db)
):
    return crud_user.create_user_project(db=db, project=project, user_id=user_id)