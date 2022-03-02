from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.api.dependencies import get_db, get_current_user

router = APIRouter()

@router.post('/api/v1/matches/', response_model=schemas.Match, tags=['matches'])
def create_match(game_id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_game = crud.get_game_by_id(db, game_id)
    
    if not db_game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Game not found')
    
    match = schemas.MatchCreate(player1=current_user.id, game=game_id)

    return crud.create_match(db, match)


@router.get('/api/v1/matches/', response_model=schemas.Match, tags=['matches'])
def get_match(room_code: str, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_match = crud.get_match_by_room_code(db, room_code)

    if db_match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Match not found')

    return db_match
