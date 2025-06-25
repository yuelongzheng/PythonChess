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
    
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

class Move():
    ranks_to_rows = {}
    for i in range(1,9,1):
        ranks_to_rows.update({str(i) : 8 - i})
    rows_to_ranks = {j : i for i,j in ranks_to_rows.items()}
    files_to_cols = {}
    for i in range(ord('a'), ord('a') + 8, 1):
        files_to_cols.update({chr(i) : i - ord('a')})
    cols_to_files = {j : i for i,j in files_to_cols.items()}

    
    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
    
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]


# if __name__ == '__main__':
#     m = Move
#     print(m.cols_to_files)
#     print(m.files_to_cols)
#     print(m.ranks_to_rows)
#     print(m.rows_to_ranks)
