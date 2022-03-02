from typing import List
from pydantic import BaseModel

from backend.schemas import Movement, MovementBase

class PieceBase(BaseModel):
    """Base piece schema."""
    name: str
    fen_name: str
    movements: List[MovementBase]


class PieceCreate(PieceBase):
    """Create piece schema."""
    pass


class Piece(PieceBase):
    """Complete piece schema."""
    id: int
    movements: List[Movement]
    game_id: int

    class Config:
        orm_mode = True
