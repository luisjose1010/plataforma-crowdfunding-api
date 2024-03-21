from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from typing import Annotated
from schemas.user import User, UserCreate, UserUpdate, UserProjects
from schemas.project import Project, ProjectCreate
from dependencies import get_db, get_token_subject
from crud import crud_user, crud_login

import re


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, id_card: str = None, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, id_card=id_card, skip=skip, limit=limit)
    return users

@router.get("/count/", response_model=int)
def read_users_count(db: Session = Depends(get_db)):
    return crud_user.get_users_count(db)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud_user.create_user(db=db, user=user)
    except IntegrityError as Error:
        orig_error = UniqueViolation(Error.orig).args[0].diag
        fields = re.search(r'\((.*)\)=\((.*)\)', orig_error.message_detail)
        raise HTTPException(status_code=422, detail={
            "msg": orig_error.message_detail,
            "key": fields.group(1),
            "value": fields.group(2)
        })
    return db_user


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    token_user = crud_user.get_user(db, token_subject)

    if user.new_password:
        if not crud_login.authenticate_user_id(db, user_id=user_id, password=user.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
    if not str(token_subject) == str(user_id) and not token_user.is_superuser:
        raise HTTPException(status_code=403, detail="User not authorized")

    try:
        db_user = crud_user.update_user(db, user_id=user_id, user=user, token_user=token_user)
    except IntegrityError as Error:
        db.rollback()
        orig_error = UniqueViolation(Error.orig).args[0].diag
        fields = re.search(r'\((.*)\)=\((.*)\)', orig_error.message_detail)
        raise HTTPException(status_code=422, detail={
            "msg": orig_error.message_detail,
            "key": fields.group(1),
            "value": fields.group(2)
        })
    return db_user

@router.get("/{user_id}/projects/", response_model=UserProjects)
def read_project_of_user(
    user_id: int,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    db_project = crud_user.get_user(db, user_id=user_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_project

@router.post("/{user_id}/projects/", response_model=Project)
def create_project_for_user(
    user_id: int, project: ProjectCreate,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    if not str(token_subject) == str(user_id):
        raise HTTPException(status_code=403, detail="User not authorized")
    return crud_user.create_user_project(db=db, project=project, user_id=user_id)