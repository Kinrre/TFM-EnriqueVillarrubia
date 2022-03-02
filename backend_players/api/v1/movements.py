from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from backend_players.schemas import MovementCheckResponse, MovementCheckPetition
from backend_players.core.config import GAME_URL
from backend_players.players.chess.core.board import Board

import requests

router = APIRouter()

@router.post('/api/v1/movements/', response_model=MovementCheckResponse, tags=['movements'])
def check_movement(movement: MovementCheckPetition):
    game_response = requests.get(GAME_URL + str(movement.id)) # Get the game configuration

    if game_response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=game_response.json()['detail'])

    game_json = game_response.json()

    # Swap fen if color is black
    if (movement.color == 'black'):
        movement.board = movement.board.swapcase()

    # Get a board with that fen board
    board = Board.from_json(game_json)
    board.fen = movement.board
    board.create_board_from_fen()

    # Get the valid movements
    valid_moves = board.valid_moves_index()

    # Calculate the movement
    from_position = [movement.from_position_x, movement.from_position_y]
    to_position = [movement.to_position_x, movement.to_position_y]
    movement_1D = board.calculate_movement_1D(from_position, to_position)
    is_valid = movement_1D in valid_moves

    return {'valid': is_valid}
