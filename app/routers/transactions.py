import re
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from schemas.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionProjectUser
from schemas.project import Project
from dependencies import get_db, get_token_data, get_token_subject
from crud import crud_transaction, crud_user, crud_project


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Transaction])
def read_transactions(skip: int = 0, limit: int = 100, is_verified: bool = None,  db: Session = Depends(get_db)):
    transaction = crud_transaction.get_transactions(db, is_verified=is_verified, skip=skip, limit=limit)
    return transaction

@router.get("/projects/users/", response_model=list[TransactionProjectUser])
def read_transactions_user(skip: int = 0, limit: int = 100, is_verified: bool = None,  db: Session = Depends(get_db)):
    db_transaction = crud_transaction.get_transactions(db, is_verified=is_verified, skip=skip, limit=limit)
    return db_transaction

@router.get("/count/", response_model=int)
def read_transactions_count(db: Session = Depends(get_db)):
    return crud_transaction.get_transactions_count(db)

@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    db_transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


@router.post("/", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    db_transaction = crud_transaction.create_transaction(db=db, transaction=transaction)
    return db_transaction

@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    token_subject: Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    token_user = crud_user.get_user(db, user_id=token_subject)
    if not token_user.is_superuser:
        raise HTTPException(status_code=403, detail="User not authorized, need superuser")

    try:
        db_transaction = crud_transaction.update_transaction(db, transaction_id=transaction_id, transaction=transaction)
    except RequestValidationError as Error:
        raise HTTPException(status_code=422, detail=str(Error))
    return db_transaction