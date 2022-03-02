from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from multiprocessing import Process

from backend_players.schemas import TrainResponse
from backend_players.core.config import GAME_URL, MEMORY_GPU, TIME_WAIT_GPU
from backend_players.players.main import train

import GPUtil
import requests
import time

router = APIRouter()

@router.post('/api/v1/train/{id}', response_model=TrainResponse, status_code=status.HTTP_202_ACCEPTED, tags=['train'])
async def train_game(id: int):
    time.sleep(TIME_WAIT_GPU) # Wait to create the other training processes

    gpu = GPUtil.getGPUs()[0]

    # Ensuring we have enough memory for a training process and a playing process
    if gpu.memoryFree < MEMORY_GPU * 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Not enough memory in the system, please try later')

    game_response = requests.get(GAME_URL + str(id)) # Get the game configuration

    if game_response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=game_response.json()['detail'])

    game_json = game_response.json()

    if game_json['is_trained']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Game already trained')

    if game_json['is_training']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Game already training')

    # Indicate what neural network will be used to trained
    board_size = game_json['board_size']
    small =  True if board_size < 5 else False

    model = 'backend_players/players/models/' + game_json['model'] # Obtain the model of the game

    proc = Process(target=train, args=(game_json, small, model)) # Create the process of training
    proc.start() # Start the process

    return {'id': game_json['id'], 'detail': 'Player training request sent, check the id for the status'}
