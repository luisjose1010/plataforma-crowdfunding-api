from fastapi import FastAPI, Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session
from core.config import settings
from core.security import create_access_token
from db.database import Base, engine
from schemas.token import Token
from crud.crud_login import authenticate_user
from dependencies import get_db, get_token_data
from routers import users, projects, categories, transactions


def create_tables():         
	Base.metadata.create_all(bind=engine)
     
def set_cors_headers(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    app = set_cors_headers(app=app)
    create_tables()
    return app


app = start_application()
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(categories.router)
app.include_router(transactions.router)


@app.get("/")
async def root():
    return {"message": "API root endpoint, API is working..."}


@app.get("/token")
async def get_token(token_data: Annotated[any, Depends(get_token_data)]):
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = None
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")