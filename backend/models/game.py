from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from backend.database import Base

import uuid

class Game(Base):
    """Game database model."""
    __tablename__ = 'games'
    __table_args__ = (UniqueConstraint('name', 'owner_id'),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    board_size = Column(Integer)
    initial_board = Column(String)
    maximum_movements = Column(Integer)
    model = Column(String, unique=True, index=True, default=uuid.uuid4)
    is_training = Column(Boolean, default=False)
    is_trained = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    pieces = relationship('Piece', back_populates='game')
    owner = relationship('User', back_populates='games')
