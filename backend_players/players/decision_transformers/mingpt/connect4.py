import torch

from backend_players.players.alphazero.connect4.connect4_game import Connect4Game

class Connect4GameDT(Connect4Game):
    """
    Connect4Game class adapted to the decision transformer architecture.
    """
    
    def __init__(self, path):
        super().__init__(path)
        self.player = 1
        self.device = torch.device('cpu')
        self.training = True
        
    def step(self, action):
        self.board.move(action)
        reward = self.getGameEnded()
        done = reward != 0
        self.player *= -1
        return torch.tensor(self.board.np_pieces), reward, done

    def train(self):
        self.training = True

    def eval(self):
        self.training = False
        
    def reset(self):
        self.board.reset()
        return torch.tensor(self.board.np_pieces)
