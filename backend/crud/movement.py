from typing import List
from sqlalchemy.orm import Session

from backend import models, schemas

def create_movement(db: Session, movement: schemas.MovementCreate, piece_id: int):
    """Create a movement to the database given a MovementCreate schema and the piece."""
    db_movement = models.Movement(
        direction=movement.direction,
        range=movement.range,
        piece_id=piece_id
    )

    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)

    return db_movement


def create_movements(db: Session, movements: List[schemas.MovementCreate], piece_id: int):
    """Create movements to the database given a List of MovementCreate schema and the piece."""
    db_movements = []

    for movement in movements:
        db_movement = create_movement(db, movement, piece_id)
        db_movements.append(db_movement)

    return db_movements
