import logging
import numpy as np
import socketio
import sys
import re

from backend_players.players.MCTS import MCTS
from backend_players.players.utils import dotdict

from backend_players.players.chess.chess_game import ChessGame as Game
from backend_players.players.chess.keras.NNet import NNetWrapper

log = logging.getLogger(__name__)
SOCKET_IO_ENDPOINT = 'http://localhost:8001/'

class ArenaOnline:
    """
    An Arena class where a computer agent can play online through Socket.io.
    """

    sio = socketio.Client()

    def __init__(self, game_configuration, small, model, room_code):
        self.game = Game(game_configuration)
        self.board = self.game.getInitBoard()
        self.neural_network_player = self.__create_player(small, model)
        self.room_code = room_code
        self.is_active_player = False

    def __create_player(self, small, model):
        """ Create the player of the model trained. """
        neural_network = NNetWrapper(self.game, small)
        neural_network.load_checkpoint(model, 'best.pth.tar')

        args = dotdict({'numMCTSSims': 25, 'cpuct': 1})
        mcts = MCTS(self.game, neural_network, args)

        neural_network_player = lambda x: np.argmax(mcts.getActionProb(x, temp=0))

        return neural_network_player

    def call_backs(self): 
        @self.sio.event
        def connect():
            """ 
            Connection to the Socket.io server, emit a join room event and a room_completed.
            """
            self.sio.emit('join', self.room_code)
            data = {'roomCode': self.room_code, 'playerName': 'Computer'}
            self.sio.emit('room_completed', data)

        @self.sio.event
        def move(position):
            """ Move event. """
            if not self.is_active_player:
                # Handle opponent movement
                self.move_opponent_piece(position)
                self.is_active_player = True

                # Create our movement
                payload = self.move_piece()
                self.sio.emit('move', payload)

                # Check end game
                (has_end, payload) = self.get_end_game()
                if has_end:
                    self.sio.emit('end_game', payload)
            else:
                self.is_active_player = False

        @self.sio.event
        def endGame(data):
            """ End of the game. """
            self.sio.emit('leave', self.room_code)
            self.sio.disconnect()
            sys.exit(0)

        @self.sio.event
        def leave():
            """ Leave room event. """
            self.sio.emit('leave', self.room_code)
            self.sio.disconnect()
            sys.exit(0)

    def move_piece(self):
        """ Perform the best movement of the neural network. """
        current_player = -1 # The agent are the black pieces
        action = self.neural_network_player(self.game.getCanonicalForm(self.board, current_player)) # Get the best action
        valids = self.game.getValidMoves(self.game.getCanonicalForm(self.board, current_player), 1) # Get the valid actions

        # Calculate the movement in 2D
        (original_position, new_position) = self.game.board.calculate_movement_2D(action)
        original_position = [i * 100 for i in original_position]
        new_position = [i * 100 for i in new_position]

        # In CSS they are reversed
        from_position = f'translate({original_position[1]}%, {original_position[0]}%)'
        new_position = f'translate({new_position[1]}%, {new_position[0]}%)'

        payload = {'fromPosition': from_position, 'toPosition': new_position, 'roomCode': self.room_code}

        # Get the next state
        self.board, current_player = self.game.getNextState(self.board, current_player, action)

        return payload

    def move_opponent_piece(self, position):
        """ Move the piece to the new position obtain from the socket.io of an opponent """
        # In the communication, the positions are given by hunderds
        from_position_css = [int(i) // 100 for i in re.findall(r'\d+', position['fromPosition'])]
        to_position_css = [int(i) // 100 for i in re.findall(r'\d+', position['toPosition'])]

        # In CSS they are reversed
        from_position = [0, 0]
        from_position[0] = from_position_css[1]
        from_position[1] = from_position_css[0]

        to_position = [0, 0]
        to_position[0] = to_position_css[1]
        to_position[1] = to_position_css[0]

        white_action = self.game.board.calculate_movement_1D(from_position, to_position) # Calculate the action of the white pieces
        
        current_player = 1 # The opponent are the white pieces
        self.board, current_player = self.game.getNextState(self.board, current_player, white_action) # Get the next state

    def get_end_game(self):
        """ Checks if the game has ended. """
        end = self.game.getGameEnded(self.board, 0)
        color = None

        if end == 1:
            color = 'white'
        elif end == -1:
            color = 'black'

        has_end = True if color != None else False
        payload = {'roomCode': self.room_code, 'winner': color}

        return (has_end, payload)

    def run(self):
        self.call_backs()
        self.sio.connect(SOCKET_IO_ENDPOINT)
        self.sio.wait()


def play(game_configuration, small, model, room_code):
    player = ArenaOnline(game_configuration, small, model, room_code)
    player.run()
