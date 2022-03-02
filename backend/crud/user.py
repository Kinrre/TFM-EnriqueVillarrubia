from sqlalchemy.orm import Session

from backend import models, schemas

import bcrypt

def generate_password(password: str):
    """Generate the hashed password for a user."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

    return hashed_password


def create_user(db: Session, user: schemas.UserCreate):
    """Create a user to the database given a UserCreate schema."""
    hashed_password = generate_password(user.password)
    
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user: schemas.UserCreate):
    """Delete a user from the database given a UserCreate schema."""
    db_user = get_user_by_username(db, user.username)

    db.delete(db_user)
    db.commit()


def get_user_by_id(db: Session, id: int):
    """Get a user from the database by his id."""
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_username(db: Session, username: str):
    """Get a user from the database by his username."""
    return db.query(models.User).filter(models.User.username == username).first()


def update_password(db: Session, new_password: str, user: schemas.UserCreate):
    """Update the password of a user to the database."""
    hashed_password = generate_password(new_password)
    
    db_user = get_user_by_username(db, user.username)
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)

    return db_user
