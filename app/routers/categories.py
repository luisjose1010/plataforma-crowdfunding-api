from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.category import Category
from dependencies import get_db
from crud import crud_category


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Category])
def read_categories(skip: int = 0, limit: int = 100, url: str = None, db: Session = Depends(get_db)):
    categories = crud_category.get_categories(db, skip=skip, limit=limit, url=url)
    return categories

@router.get("/count", response_model=int)
def read_categories_count(db: Session = Depends(get_db)):
    return crud_category.get_categories_count(db)


@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_project = crud_category.get_category(db, category_id=category_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_project