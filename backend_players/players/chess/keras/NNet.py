import numpy as np
import time
import os

from tensorflow.keras.callbacks import TensorBoard

from backend_players.players.utils import *
from backend_players.players.NeuralNet import NeuralNet
from backend_players.players.chess.keras.ChessNNet import ChessNNet, ChessNNetSmall

DEFAULT_LOG_DIR = 'D:/modelos/chess/modelo2'

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': True,
    'num_channels': 512,
    'log_dir': DEFAULT_LOG_DIR,
})

class NNetWrapper(NeuralNet):

    def __init__(self, game, small, log_dir=DEFAULT_LOG_DIR):
        # The board size is less than 5x5
        if small:
            self.nnet = ChessNNetSmall(game, args)
        else:
            self.nnet = ChessNNet(game, args)

        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        args.log_dir = log_dir

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        tensorboard = TensorBoard(log_dir=args.log_dir)
        self.nnet.model.fit(x=input_boards, y=[target_pis, target_vs], batch_size=args.batch_size,
                            epochs=args.epochs, callbacks=[tensorboard])

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict(board)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        #if not os.path.exists(filepath):
        #    raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)
