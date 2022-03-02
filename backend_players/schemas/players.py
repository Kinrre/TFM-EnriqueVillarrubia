from pydantic import BaseModel

class PlayGamePetition(BaseModel):
    """Play game petition schema."""
    id: int
    room_code: str


class PlayGameResponse(BaseModel):
    """Play game response schema."""
    detail: str
