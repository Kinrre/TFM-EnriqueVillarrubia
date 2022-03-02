from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.api.dependencies import get_db
from backend.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@router.post('/api/v1/auth/token', response_model=schemas.Token, tags=['auth'])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    user = schemas.UserCreate(username=form_data.username, password=form_data.password)
    db_user = crud.auth_user(db, user)

    if db_user is None:
        raise credentials_exception

    access_token = create_access_token(
        data={'sub': str(db_user.id), 'name': db_user.username}
    )

    return {'access_token': access_token, 'token_type': 'bearer'}
