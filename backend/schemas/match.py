from typing import Optional
from pydantic import BaseModel

from backend.schemas import Game, User

class MatchBase(BaseModel):
    """Base matchup schema."""
    player1: int
    game: int


class MatchCreate(MatchBase):
    """Create matchup schema."""
    pass


class Match(BaseModel):
    """Complete matchup schema."""
    id: int
    game: Game
    player1: User
    player2: Optional[User]
    room_code: str
    winner: Optional[User]

    class Config:
        orm_mode = True
