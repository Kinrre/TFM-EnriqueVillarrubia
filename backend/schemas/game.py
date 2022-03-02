from typing import List, Optional
from pydantic import BaseModel

from backend.schemas import Piece, PieceBase

class GameBase(BaseModel):
    """Base game schema."""
    name: str
    board_size: int
    initial_board: str
    maximum_movements: int
    pieces: List[PieceBase]


class GameCreate(GameBase):
    """Create game schema."""
    pass


class GameUpdate(BaseModel):
    """Update game schema."""
    new_name: Optional[str] = None
    is_training: Optional[bool] = None
    is_trained: Optional[bool] = None


class Game(GameBase):
    """Complete game schema."""
    id: int
    pieces: List[Piece]
    model: str
    is_training: bool = False
    is_trained: bool = False
    owner_id: int

    class Config:
        orm_mode = True
