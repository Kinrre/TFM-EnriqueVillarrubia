from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.schema import UniqueConstraint

from backend.database import Base

import secrets

def generate_room_code():
    """Generate a room code random secure."""
    return secrets.token_urlsafe(4)


class Match(Base):
    """Match database model."""
    __tablename__ = 'matches'
    __table_args__ = (UniqueConstraint('room_code'),)

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id', ondelete=None))
    player1_id = Column(Integer, ForeignKey('users.id', ondelete=None))
    room_code = Column(String, default=generate_room_code)

    game = relationship('Game')
    player1 = relationship('User', foreign_keys=[player1_id])
