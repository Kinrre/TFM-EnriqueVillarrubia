from pydantic import BaseModel

class MovementCheckPetition(BaseModel):
    """Movement check petition schema."""
    id: int
    board: str
    color: str
    from_position_x: int
    from_position_y: int
    to_position_x: int
    to_position_y: int


class MovementCheckResponse(BaseModel):
    """Movement check response schema."""
    valid: bool
