from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from multiprocessing import Process

from backend_players.schemas import PlayGamePetition, PlayGameResponse
from backend_players.core.config import GAME_URL, MEMORY_GPU, TIME_WAIT_GPU
from backend_players.players.ArenaOnline import play

import GPUtil
import requests
import time

router = APIRouter()

@router.post('/api/v1/players/', response_model=PlayGameResponse, status_code=status.HTTP_202_ACCEPTED, tags=['players'])
async def play_game(petition: PlayGamePetition):
    time.sleep(TIME_WAIT_GPU) # Wait to create the other training processes

    gpu = GPUtil.getGPUs()[0]

    # Ensuring we have enough memory for a playing process
    if gpu.memoryFree < MEMORY_GPU:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not enough memory in the system, please try later')

    game_response = requests.get(GAME_URL + str(petition.id)) # Get the game configuration

    if game_response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=game_response.json()['detail'])

    game_json = game_response.json()

    # Indicate what neural network will be used to trained
    board_size = game_json['board_size']
    small =  True if board_size < 5 else False

    model = 'backend_players/players/models/' + game_json['model'] # Obtain the model of the game

    proc = Process(target=play, args=(game_json, small, model, petition.room_code)) # Create the process of training
    proc.start() # Start the process

    return {'detail': 'Player creation request sent'}
