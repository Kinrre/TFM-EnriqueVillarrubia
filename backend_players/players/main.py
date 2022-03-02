import argparse
import coloredlogs
import logging
import requests

from backend_players.players.Coach import Coach
from backend_players.players.chess.chess_game import ChessGame as Game
from backend_players.players.chess.keras.NNet import NNetWrapper as nn
from backend_players.players.utils import *

from pathlib import Path

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

GAME_URL = 'http://localhost:8000/api/v1/games/' # Game endpoint
DEFAULT_CHECKPOINT = 'D:/modelos/chess/modelo2'

args = dotdict({
    'numIters': 50,
    'numEps': 40,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 10,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 30,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 20,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': DEFAULT_CHECKPOINT,
    'load_model': False,
    'load_folder_file': ('temp/', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})


def train_offline(game_configuration, small, model=DEFAULT_CHECKPOINT):
    args.checkpoint = model
    Path(args.checkpoint).mkdir(parents=True, exist_ok=True) # Create directory for checkpoints if not exists

    log.info('Loading %s...', Game.__name__)
    g = Game(game_configuration)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g, small, args.checkpoint)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file[0], args.load_folder_file[1])
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


def train(game_configuration, small, model=DEFAULT_CHECKPOINT):
    requests.put(GAME_URL + str(game_configuration['id']), json={'is_training': True}) # Notify train begining
    train_offline(game_configuration, small, model)
    requests.put(GAME_URL + str(game_configuration['id']), json={'is_training': False, 'is_trained': True}) # Notify train finished


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to a JSON game configuration. See examples folder.')
    
    parser_args = parser.parse_args()

    with open(parser_args.path, 'r') as f:
        content = f.read()

    small = True
    train_offline(content, small)
