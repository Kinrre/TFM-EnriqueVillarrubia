import numpy as np

class HumanChessPlayer():
    """
    A human chess player.
    """

    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        board_size = self.game.getBoardSize()
        square_index = self.game.board.square_index

        #print('\nMoves:', [(np.unravel_index(i // square_index, board_size), np.unravel_index(i % square_index, board_size), i) for (i, valid) in enumerate(valid_moves) if valid])

        while True:
            try:
                original_row = int(input('From row: '))
                original_column = int(input('From column: '))
                position = (original_row, original_column)

                new_row = int(input('To row: '))
                new_column = int(input('To column: '))
                new_position = (new_row, new_column)

                move = self.__to_move(position, new_position)
            except ValueError:
                print("That's not a number")

            try:
                if valid_moves[move]:
                    break
                else: 
                    print('Invalid move')
            except UnboundLocalError:
                pass

        return move

    def __to_move(self, position, new_position):
        position_index = np.ravel_multi_index(position, self.game.getBoardSize())
        new_position_index = np.ravel_multi_index(new_position, self.game.getBoardSize())
        return position_index * self.game.board.square_index + new_position_index
