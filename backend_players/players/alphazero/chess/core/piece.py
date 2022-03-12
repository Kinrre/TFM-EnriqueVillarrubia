class Piece:
    """
    Piece of a chess.
    """

    @staticmethod
    def get_number(fen, pieces):
        """ Return the number corresponding to a piece. """
        return pieces[fen] # KeyError
    
    @staticmethod
    def get_movement(number, movement_rules):
        """ Return the movement corresponding to a piece. """
        return movement_rules[number] # KeyError

    def __repr__(self):
        return self.fen
