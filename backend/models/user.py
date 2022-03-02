from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base

class User(Base):
    """User database model."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    games = relationship('Game', back_populates='owner')
    