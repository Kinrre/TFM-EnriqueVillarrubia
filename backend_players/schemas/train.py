from pydantic import BaseModel

class TrainResponse(BaseModel):
    """Train response schema."""
    id: int
    detail: str
