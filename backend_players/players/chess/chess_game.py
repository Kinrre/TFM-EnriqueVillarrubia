from backend_players.players.Game import Game
from backend_players.players.chess.core import Board

class ChessGame(Game):
    """
    ChessGame class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, path):
        self.board = Board.from_json(path)

    def getInitBoard(self):
        return self.board.np_pieces

    def getBoardSize(self):
        return self.board.board_size

    def getActionSize(self):
        return self.board.action_size

    def getNextState(self, board, player, action):
        self.board.current_movement += 1
        next_board = self.board.copy(np_pieces=board)
        next_board.move(action)
        return next_board.np_pieces, -player

    def getValidMoves(self, board, player):
        next_board = self.board.copy(np_pieces=board)
        return next_board.valid_moves()

    def getGameEnded(self, board, player):
        next_board = self.board.copy(np_pieces=board)
        state = next_board.has_ended()

        if state != 0:
            self.board.current_movement = 0

        return state

    def getCanonicalForm(self, board, player):
        # Swap player 1 to player -1
        return board * player

    def getSymmetries(self, board, pi):
        # Board is left/right board symmetric
        return [(board, pi), (board[:, ::-1], pi[::-1])]

    def stringRepresentation(self, board):
        return board.tostring() + bytes([self.board.current_movement])

    @staticmethod
    def display(board):
        print(board)
