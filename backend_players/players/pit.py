import numpy as np

from backend_players.players.Arena import Arena
from backend_players.players.MCTS import MCTS
from backend_players.players.utils import dotdict

from backend_players.players.chess.chess_game import ChessGame
from backend_players.players.chess.chess_players import HumanChessPlayer
from backend_players.players.chess.keras.NNet import NNetWrapper

path = 'backend_players/players/examples/first_game.json'

with open(path, 'r') as f:
    content = f.read()

g = ChessGame(content)
hp = HumanChessPlayer(g).play

n1 = NNetWrapper(g)
n1.load_checkpoint('backend_players/players/models/ea8b0022-99a1-4a07-b6f6-2c73ce02d3fd', 'checkpoint_2.pth.tar')

args1 = dotdict({'numMCTSSims': 30, 'cpuct': 1})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

n2 = NNetWrapper(g)
n2.load_checkpoint('backend_players/players/models/ea8b0022-99a1-4a07-b6f6-2c73ce02d3fd', 'best.pth.tar')

args2 = dotdict({'numMCTSSims': 30, 'cpuct': 1})
mcts2 = MCTS(g, n2, args2)
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

arena = Arena(n1p, n2p, g, display=ChessGame.display)

print(arena.playGames(20, verbose=True))
