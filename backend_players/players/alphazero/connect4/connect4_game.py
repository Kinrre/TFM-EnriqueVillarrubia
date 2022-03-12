from backend_players.players.alphazero.Game import Game
from backend_players.players.alphazero.connect4.core.board import Board

class Connect4Game(Game):
    """
    Connect4Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, path):
        self.board = Board.from_json(path)
        #self.board = Board(height, width)

    def getInitBoard(self):
        return self.board.np_pieces

    def getBoardSize(self):
        return self.board.board_size

    def getActionSize(self):
        return self.board.action_size

    def getNextState(self, board, player, action):
        next_board = self.board.copy(np_pieces=board)
        next_board.move(action, player)
        return next_board.np_pieces, -player

    def getValidMoves(self, board, player):
        next_board = self.board.copy(np_pieces=board)
        return next_board.get_valid_moves()

    def getGameEnded(self, board, player):
        next_board = self.board.copy(np_pieces=board)
        state = next_board.has_ended()
        return state

    def getCanonicalForm(self, board, player):
        # Swap player 1 to player -1
        return board * player

    def getSymmetries(self, board, pi):
        # Board is left/right board symmetric
        return [(board, pi), (board[:, ::-1], pi[::-1])]

    def stringRepresentation(self, board):
        return board.tobytes()

    @staticmethod
    def display(board):
        print(board)
