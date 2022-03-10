import json
import numpy as np

DEFAULT_HEIGHT = 6
DEFAULT_WIDTH = 7
DEFAULT_WIN_LENGTH = 4
DEFAULT_PLAYER_1 = 1
DEFAULT_PLAYER_2 = -1


class Board():
    """
    Connect4 Board.
    """

    def __init__(self, height=None, width=None, win_length=None, np_pieces=None):
        """ Set up initial board configuration. """
        self.height = height or DEFAULT_HEIGHT
        self.width = width or DEFAULT_WIDTH
        self.win_length = win_length or DEFAULT_WIN_LENGTH

        if np_pieces is None:
            self.np_pieces = np.zeros([self.height, self.width], dtype=np.byte)
        else:
            self.np_pieces = np_pieces
        
        assert self.np_pieces.shape == (self.height, self.width)

        self.board_size = self.__board_size()
        self.action_size = self.__action_size()

    @classmethod
    def from_json(cls, game_configuration):
        """ Set up inital board configuration given a json file. """
        if isinstance(game_configuration, dict):
            game_dict = game_configuration
        else:
            game_dict = json.loads(game_configuration)

        height = game_dict['height']
        width = game_dict['width']
        win_length = game_dict['win_length']

        return cls(height, width, win_length)

    def copy(self, np_pieces):
        """ Return a board with a copy by value of the pieces. """
        if np_pieces is None:
            np_pieces = np.copy(self.np_pieces)
        return Board(self.height, self.width, self.win_length, np.copy(np_pieces))

    def get_valid_moves(self):
        """ The valid movements are the columns which the top row is empty. """
        return self.np_pieces[0] == 0

    def move(self, action, player):
        valid_rows = np.where(self.np_pieces[:, action] == 0)[0]

        if len(valid_rows) == 0:
            raise ValueError(f"Can't play a piece on column {action} in board \n {self.np_pieces}")

        self.np_pieces[valid_rows[-1]][action] = player

    def has_ended(self, player):
        """
        Returns the reward of the game. Four values are possible, 0 if the game
        has not finished, 1 if the player1 has win, -1 if the player1
        has loss and 1e-4 if they have drawn.
        """
        reward = 0
        winner = 0

        for _player in [DEFAULT_PLAYER_2, DEFAULT_PLAYER_1]:
            player_pieces = self.np_pieces == -_player
            # Check rows & columns for win
            if (self._is_straight_winner(player_pieces) or
                self._is_straight_winner(player_pieces.transpose()) or
                self._is_diagonal_winner(player_pieces)):
                winner = -_player

        if winner == player:
            # Win has a positive reward
            reward = 1
        elif winner == -player:
            # Loss has a negative reward
            reward = -1
        elif not self.get_valid_moves().any():
            # Draw has a very little reward
            reward = 1e-4

        return reward

    def _is_straight_winner(self, player_pieces):
        """ Checks if player_pieces contains a vertical or horizontal win. """
        run_lengths = [player_pieces[:, i:i + self.win_length].sum(axis=1)
                       for i in range(len(player_pieces) - self.win_length + 2)]
                       
        return max([x.max() for x in run_lengths]) >= self.win_length

    def _is_diagonal_winner(self, player_pieces):
        """ Checks if player_pieces contains a diagonal win. """
        win_length = self.win_length
        
        for i in range(len(player_pieces) - win_length + 1):
            for j in range(len(player_pieces[0]) - win_length + 1):
                if all(player_pieces[i + x][j + x] for x in range(win_length)):
                    return True
            for j in range(win_length - 1, len(player_pieces[0])):
                if all(player_pieces[i + x][j - x] for x in range(win_length)):
                    return True

        return False

    def reset(self):
        """ Reset the board pieces. """
        self.np_pieces = np.zeros([self.height, self.width], dtype=np.byte)

    def __board_size(self):
        """ Returns the board size. """
        return (self.height, self.width)

    def __action_size(self):
        """
        Returns the action size of the board. That's the width, as a user can put
        a piece in every column.
        """
        return self.width
