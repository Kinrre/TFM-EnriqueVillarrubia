from sqlalchemy.orm import Session

from backend import crud, schemas

import bcrypt

def auth_user(db: Session, user: schemas.UserCreate):
    """Authenticate a user from the system."""
    db_user = crud.get_user_by_username(db, user.username)
    valid_password = False

    if db_user:
        valid_password = bcrypt.checkpw(user.password.encode(), db_user.password.encode())

    if not valid_password:
        db_user = None

    return db_user
