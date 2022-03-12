import numpy as np

from backend_players.players.Arena import Arena
from backend_players.players.MCTS import MCTS
from backend_players.players.utils import dotdict

from backend_players.players.connect4.connect4_game import Connect4Game
from backend_players.players.connect4.connect4_players import HumanConnect4Player, OneStepLookaheadConnect4Player, RandomPlayer
from backend_players.players.connect4.keras.NNet import NNetWrapper

path = 'backend_players/players/examples/second_game.json'

with open(path, 'r') as f:
    content = f.read()

g = Connect4Game(content)
hp = HumanConnect4Player(g).play
gp = OneStepLookaheadConnect4Player(g, verbose=False).play
rp = RandomPlayer(g).play

n1 = NNetWrapper(g, True)
n1.load_checkpoint('D:/modelos/connect4/modelo', 'checkpoint_21.pth.tar')

args1 = dotdict({'numMCTSSims': 25, 'cpuct': 1})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

#n2 = NNetWrapper(g)
#n2.load_checkpoint('backend_players/players/models/ea8b0022-99a1-4a07-b6f6-2c73ce02d3fd', 'best.pth.tar')

#args2 = dotdict({'numMCTSSims': 25, 'cpuct': 1})
#mcts2 = MCTS(g, n2, args2)
#n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

arena = Arena(n1p, gp, g, display=Connect4Game.display)

print(arena.playGames(20, verbose=True))
