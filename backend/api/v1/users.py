from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.api.dependencies import get_db, get_current_user

import re

router = APIRouter()

@router.post('/api/v1/users/', response_model=schemas.User, tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.username = user.username.capitalize()
    db_user = crud.get_user_by_username(db, user.username)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Username already registered')

    if not re.match(r'\w+\Z', user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Username must only contains: letters, digits and underscore')

    return crud.create_user(db, user)


@router.get('/api/v1/users/me', response_model=schemas.User, tags=['users'])
def read_current_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.put('/api/v1/users/me', response_model=schemas.User, tags=['users'])
def update_password(new_password: str = Body(..., embed=True), current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_password(db, new_password, current_user)


@router.delete('/api/v1/users/me', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    crud.delete_user(db, current_user)


@router.get('/api/v1/users/{username}', response_model=schemas.User, tags=['users'])
def read_user_username(username: str, db: Session = Depends(get_db)):
    username = username.capitalize()
    db_user = crud.get_user_by_username(db, username)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    return db_user


@router.get('/api/v1/users/id/{id}', response_model=schemas.User, tags=['users'])
def read_user_id(id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')

    return db_user
