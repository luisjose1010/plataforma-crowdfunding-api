from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.exceptions import HTTPException
from crud import crud_user, crud_project
from schemas.user import UserUpdate
from dependencies import get_db, get_token_subject
import glob


router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Not found"}},
)

@router.get("/users/{user_id}")
async def getAvatar(
    user_id: int,
)->FileResponse:
    image_path = Path(f"./src/avatars/{user_id}.png")
    if not image_path.is_file():
        return HTTPException(status_code=404, detail="File not found")
    return FileResponse(image_path)

@router.get("/projects/{project_id}")
async def getImage(
    project_id: int,
)->FileResponse:
    image_path = Path(f"./src/projects/{project_id}.png")
    if not image_path.is_file():
        return HTTPException(status_code=404, detail="File not found")
    return FileResponse(image_path)


@router.post("/users/{user_id}")
async def uploadAvatar(
    file: UploadFile,
    user_id: int,
    token_subject:Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    try:
        file_extension = file.filename.split(".")[1]
        file_path = f"./src/avatars/{user_id}.{file_extension}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        crud_user.update_user(db, user_id=user_id, user=UserUpdate(avatar=file_path))
        return {"message": "File saved"}
    except Exception as e:
        return HTTPException(status_code=500, detail=e.args)

@router.post("/projects/{project_id}")
async def uploadAvatar(
    file: UploadFile,
    project_id: int,
    token_subject:Annotated[str, Depends(get_token_subject)],
    db: Annotated[Session, Depends(get_db)]
):
    try:
        file_extension = file.filename.split(".")[1]
        file_path = f"./src/projects/{project_id}.png"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return {"message": "File saved"}
    except Exception as e:
        return HTTPException(status_code=500, detail=e.args)
