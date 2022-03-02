from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from backend.database import Base

class Movement(Base):
    """Movement database model."""
    __tablename__ = 'movements'
    __table_args__ = (UniqueConstraint('direction', 'piece_id'),)

    id = Column(Integer, primary_key=True, index=True)
    direction = Column(String)
    range = Column(Integer)
    piece_id = Column(Integer, ForeignKey('pieces.id', ondelete='CASCADE'))

    piece = relationship('Piece', back_populates='movements')
