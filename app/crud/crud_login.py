from core.hashing import Hasher
from crud import crud_user

def authenticate_user(db, username: str, password: str):
    db_user = crud_user.get_user_by_email(db, email=username)
    if not db_user:
        return False
    if not Hasher.verify_password(password, db_user.password):
        return False
    return db_user