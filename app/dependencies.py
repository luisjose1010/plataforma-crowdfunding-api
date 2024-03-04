from fastapi import Depends, HTTPException, status
from typing import Annotated
from db.database import SessionLocal
from jose import JWTError, jwt
from core.security import oauth2_scheme
from core.config import settings


# Dependency database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencies token security
def get_token_subject(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_subject: str = payload.get("sub")
        if token_subject is None:
            raise credentials_exception
    except JWTError as Error:
        credentials_exception.detail = str(Error)
        raise credentials_exception
    return token_subject

def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload is None:
            raise credentials_exception
    except JWTError as Error:
        credentials_exception.detail(Error)
        raise credentials_exception
    return payload