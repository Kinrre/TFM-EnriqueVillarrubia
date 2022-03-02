from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.database import Base

class Piece(Base):
    """Piece database model."""
    __tablename__= 'pieces'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    fen_name = Column(String)
    game_id = Column(Integer, ForeignKey('games.id', ondelete='CASCADE'))

    movements = relationship('Movement', back_populates='piece')
    game = relationship('Game', back_populates='pieces')
