from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.core.config import SECRET_KEY, ALGORITHM

from backend.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials. Reason: ',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        sub: str = payload.get('sub')
        name: str = payload.get('name')
        exp: int = payload.get('exp')
        
        if sub is None or name is None or exp is None:
            raise credentials_exception

        token_data = schemas.TokenData(sub=sub, name=name, exp=exp)
    except JWTError as e:
        credentials_exception.detail += str(e)
        raise credentials_exception
    
    user = crud.get_user_by_username(db, token_data.name)
    
    if user is None:
        credentials_exception.detail += 'Invalid user'
        raise credentials_exception

    return user
