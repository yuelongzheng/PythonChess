"""
Responsible for storing all information about the current state of a chess game. 
            for determining valid moves at the current state.
"""
class GameState():
    def __init__(self):
        # Board is 8 x 8 2d list, each element has 2 characters
        # first character is the colour of the piece and the second has the type of piece
        # R - Rook, N - Knight, B - Bishop, Q - Queen, K - King, p - Pawn
        # -- represents empty space with no piece
        # In the future could make it a numpy array
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        