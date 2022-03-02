from sqlalchemy.orm import Session

from backend import models, schemas

def create_match(db: Session, match: schemas.MatchCreate):
    """Create a match to the database given a MatchCreate schema."""
    db_match = models.Match(player1_id=match.player1, game_id=match.game)

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return db_match


def get_match_by_id(db: Session, match_id: int):
    """Get a match from the database by his id."""
    db_match = db.query(models.Match).filter(
        models.Match.id == match_id
    ).first()
    return db_match


def get_match_by_room_code(db: Session, room_code: str):
    """Get a match from the database by his room code."""
    db_match = db.query(models.Match).filter(
        models.Match.room_code == room_code
    ).first()
    return db_match
