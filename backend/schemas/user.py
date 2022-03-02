from typing import List
from pydantic import BaseModel

from backend.schemas import Game

class UserBase(BaseModel):
    """Base user schema."""
    username: str


class UserCreate(UserBase):
    """Create user schema."""
    password: str


class User(BaseModel):
    """Complete user schema."""
    id: int
    username: str
    is_active: bool
    games: List[Game] = []

    class Config:
        orm_mode = True
