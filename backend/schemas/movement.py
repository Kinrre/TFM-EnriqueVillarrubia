from pydantic import BaseModel

class MovementBase(BaseModel):
    """Base movement schema."""
    direction: str
    range: int


class MovementCreate(MovementBase):
    """Create movement schema."""
    pass


class Movement(MovementBase):
    """Completa movement schema."""
    id: int
    piece_id: int

    class Config:
        orm_mode = True
