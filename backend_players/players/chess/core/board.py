import json
import numpy as np

from backend_players.players.chess.core.piece import Piece
from backend_players.players.chess.core.utils import PIECES, MOVEMENTS

DEFAULT_HEIGHT = 6
DEFAULT_WIDTH = 6
DEFAULT_BOARD = '1pppp1/1pppp1/6/6/1PPPP1/1PPPP1'
DEFAULT_MAX_MOVEMENTS = 50
DEFAULT_PIECES = PIECES
DEFAULT_MOVEMENTS = MOVEMENTS


class Board():
    """
    Chess general board.
    """

    def __init__(self, height=None, width=None, fen=None, max_movements=None, pieces_fen=None, movement_rules=None, np_pieces=None, current_movement=0):
        """ Set up initial board configuration. """
        self.height = height or DEFAULT_HEIGHT
        self.width = width or DEFAULT_WIDTH
        self.fen = fen or DEFAULT_BOARD
        self.pieces_fen = pieces_fen or DEFAULT_PIECES

        if np_pieces is None:
            self.create_board_from_fen()
        else:
            self.np_pieces = np_pieces

        self.board_size = self.__board_size()
        self.action_size = self.__action_size()
        self.square_index = self.height * self.width

        self.current_movement = current_movement
        self.max_movements = max_movements or DEFAULT_MAX_MOVEMENTS
        self.movement_rules = movement_rules or DEFAULT_MOVEMENTS

    @classmethod
    def from_json(cls, game_configuration):
        """ Set up inital board configuration given a json file. """
        if isinstance(game_configuration, dict):
            game_dict = game_configuration
        else:
            game_dict = json.loads(game_configuration)

        height = game_dict['board_size'] # Height of the board
        width = game_dict['board_size'] # Width of the board
        fen = game_dict['initial_board'] # Initial board
        max_movements = game_dict['maximum_movements'] # Maximum movements of the game

        pieces = game_dict['pieces']
        pieces_fen = {} # Conversion between the fen string and the numbers
        movement_rules = {} # Movement rules of the game

        # Compute the direction and range of the pieces and the conversion of the fen string
        index = 0
        for piece in pieces:
            index += 1
            
            pieces_fen[piece['fen_name'].lower()] = -index
            pieces_fen[piece['fen_name'].upper()] = index

            movement_rules[index] = {}
            for movement in piece['movements']:
                direction = movement['direction']
                movement_rules[index][direction] = movement['range']

        return cls(height, width, fen, max_movements, pieces_fen, movement_rules)

    def create_board_from_fen(self):
        """ Create the board from a string in fen notation. """
        self.np_pieces = np.zeros([self.height, self.width], dtype=np.byte)

        row = 0
        column = 0

        for piece_type in self.fen:
            if piece_type.isdigit():
                column += int(piece_type)
            elif piece_type == '/':
                row += 1
                column = 0
            else:
                self.np_pieces[row][column] = Piece.get_number(piece_type, self.pieces_fen)
                column += 1

    def copy(self, np_pieces):
        """ Return a board with a copy by value of the pieces. """
        if np_pieces is None:
            np_pieces = np.copy(self.np_pieces)
        return Board(self.height, self.width, self.fen, self.max_movements, self.pieces_fen, self.movement_rules, np.copy(np_pieces), self.current_movement)
        
    def valid_moves(self):
        """ Returns all the valid movements for the current board. """
        valid_moves = np.zeros(self.action_size, dtype=np.byte)

        for row in range(self.height):
            for column in range(self.width):
                self.__valid_moves_square(row, column, valid_moves)

        return valid_moves

    def valid_moves_index(self):
        """ Returns all the valid movements for the current board (indexes). """
        valid_moves = self.valid_moves()
        return np.nonzero(valid_moves)[0]

    def calculate_movement_1D(self, position, new_position):
        """ Calculate the movement from a position to a new position in 1D. """
        position_index = np.ravel_multi_index(position, self.board_size)
        new_position_index = np.ravel_multi_index(new_position, self.board_size)
        final_index = position_index * self.square_index + new_position_index
        return final_index

    def calculate_movement_2D(self, action):
        """ Calculate the movement from an action in original_position and new_position. """
        square = action // self.square_index
        original_position = np.unravel_index(square, self.board_size)

        new_square = action % self.square_index
        new_position = np.unravel_index(new_square, self.board_size)

        return (original_position, new_position)

    def move(self, action):
        """ 
        Execute an action for the current board.
        NOTE: It does not check if the movement is valid.
        """
        (original_position, new_position) = self.calculate_movement_2D(action)
        
        original_piece = self.np_pieces[original_position]

        self.np_pieces[new_position] = original_piece
        self.np_pieces[original_position] = 0

    def has_ended(self):
        """
        Returns the state of the game. Four values are possible, 0 if the game
        has not finished, 1 if the player1 has win, -1 if the player1
        has loss and 1e-4 if they have drawn.
        """
        state = 0

        player1_npieces = self.np_pieces[self.np_pieces < 0].shape[0]
        player2_npieces = self.np_pieces[self.np_pieces > 0].shape[0]
        end_by_movements = self.current_movement >= self.max_movements

        if np.all(self.np_pieces >= 0) or (player1_npieces > player2_npieces and end_by_movements):
            # Win has a positive reward
            state = 1
        elif np.all(self.np_pieces <= 0) or (player1_npieces < player2_npieces and end_by_movements):
            # Loss has a negative reward
            state = -1
        elif end_by_movements:
            # Draw has a very little reward
            state = 1e-4

        return state

    def __board_size(self):
        """ Returns the board size. """
        return (self.height, self.width)

    def __action_size(self):
        """
        Returns the action size of the board. It assume every piece can move to
        any square.
        """
        total_positions = self.height ** 2 * self.width ** 2
        return total_positions

    def __valid_moves_square(self, row, column, valid_moves):
        """ Returns all the possible moves from a specific position. """
        # Only the player can move him pieces
        if self.np_pieces[row][column] < 1:
            return
        
        movements = Piece.get_movement(self.np_pieces[row][column], self.movement_rules)

        for key, value in movements.items():
            if key == 'north':
                self.__valid_moves_north(row, column, valid_moves, value)
            elif key == 'south':
                self.__valid_moves_south(row, column, valid_moves, value)
            elif key == 'west':
                self.__valid_moves_west(row, column, valid_moves, value)
            elif key == 'east':
                self.__valid_moves_east(row, column, valid_moves, value)

    def __valid_moves_north(self, row, column, valid_moves, movement):
        """ Return all the possible moves going north from a specific position. """
        position = (row, column)

        column_row = self.np_pieces[:, column][::-1] # Column of the row position
        start_row = self.height - row # The row where we begin to move
        max_row = self.height - 1 # As the column is reversed, we use this to obtain the not reversed row
        movement_range = start_row + movement # Range of the movement
        
        if movement_range > self.height:
            movement_range = self.height

        for i in range(start_row, movement_range):
            piece = column_row[i]

            if piece <= 0:
                new_position = (max_row - i, column)
                self.__register_valid_move(position, new_position, valid_moves)
            
            # The piece cannot jump
            if piece < 0 or piece > 0:
                break

    def __valid_moves_south(self, row, column, valid_moves, movement):
        """ Return all the possible moves going north from a specific position. """
        position = (row, column)

        column_row = self.np_pieces[:, column] # Column of the row position
        start_row = row + 1 # The row where we begin to move
        movement_range = start_row + movement # Range of the movement
        
        if movement_range > self.height:
            movement_range = self.height

        for i in range(start_row, movement_range):
            piece = column_row[i]

            if piece <= 0:
                new_position = (i, column)
                self.__register_valid_move(position, new_position, valid_moves)
            
            # The piece cannot jump
            if piece < 0 or piece > 0:
                break

    def __valid_moves_west(self, row, column, valid_moves, movement):
        """ Return all the possible moves going west from a specific position. """
        position = (row, column)

        row_column = self.np_pieces[row, :][::-1] # Row of the column position
        start_column = self.width - column # The column where we begin to move
        max_column = self.width - 1 # As the row is reversed, we use this to obtain the not reversed row
        movement_range = start_column + movement # Range of the movement
        
        if movement_range > self.width:
            movement_range = self.width

        for i in range(start_column, movement_range):
            piece = row_column[i]

            if piece <= 0:
                new_position = (row, max_column - i)
                self.__register_valid_move(position, new_position, valid_moves)
            
            # The piece cannot jump
            if piece < 0 or piece > 0:
                break

    def __valid_moves_east(self, row, column, valid_moves, movement):
        """ Return all the possible moves going east from a specific position. """
        position = (row, column)

        row_column = self.np_pieces[row, :] # Row of the column position
        start_column = column + 1 # The column where we begin to move
        movement_range = start_column + movement # Range of the movement
        
        if movement_range > self.width:
            movement_range = self.width

        for i in range(start_column, movement_range):
            piece = row_column[i]

            if piece <= 0:
                new_position = (row, i)
                self.__register_valid_move(position, new_position, valid_moves)
            
            # The piece cannot jump
            if piece < 0 or piece > 0:
                break
    
    def __register_valid_move(self, position, new_position, valid_moves):
        """ Register a valid move. """
        final_index = self.calculate_movement_1D(position, new_position)
        valid_moves[final_index] = 1 # This is a valid move
