from typing import List
from sqlalchemy.orm import Session

from backend import models, schemas

def create_piece(db: Session, piece: schemas.PieceCreate, game_id: int):
    """Create a piece to the database given a PieceCreate schema and the game."""
    db_piece = models.Piece(
        name=piece.name,
        fen_name=piece.fen_name,
        game_id=game_id
    )

    db.add(db_piece)
    db.commit()
    db.refresh(db_piece)

    return db_piece


def create_pieces(db: Session, pieces: List[schemas.PieceCreate], game_id: int):
    """Create pieces to the database given a List of PieceCreate schema and the game."""
    db_pieces = []

    for piece in pieces:
        db_piece = create_piece(db, piece, game_id)
        db_pieces.append(db_piece)

    return db_pieces
