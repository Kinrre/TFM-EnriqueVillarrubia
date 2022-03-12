"""
Utils file to save all constants values.
"""

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

PIECES = {'p': -PAWN, 'k': -KNIGHT, 'b': -BISHOP, 'r': -ROOK, 'q': -QUEEN, 'k': -KING,
          'P': PAWN, 'K': KNIGHT, 'B': BISHOP, 'R': ROOK, 'Q': QUEEN, 'K': KING}

MOVEMENTS = {PAWN: {'north': 2, 'south': 2, 'west': 2, 'east': 2}}
