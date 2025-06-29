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
        self.move_functions = {'p' : self.get_pawn_moves, 'R' : self.get_rook_moves,
                               'N' : self.get_knight_moves, 'B' : self.get_bishop_moves,
                               'Q' : self.get_queen_moves, 'K' : self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
    
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) >= 1 :
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    '''
    All moves considering checkmates
    '''
    def get_valid_moves(self):
        return self.get_all_possible_moves()

    '''
    All moves regardless of checkmates
    '''
    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if(turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    self.move_functions[piece](r, c, moves)
        return moves
    
    def get_pawn_moves(self, r, c, moves):
        start_index = 0
        end_index = len(self.board) - 1
        if self.white_to_move:
            if r - 1 >= start_index:
                if self.board[r - 1][c] == "--": # make sure square above is clear
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == end_index - 1 and self.board[r - 2][c] == "--": # initial pawn 2 square move
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c - 1 >= start_index:
                    if self.board[r - 1][c - 1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if c + 1 <= end_index:
                    if self.board[r - 1][c + 1][0] == 'b':
                        moves.append(Move((r,c), (r - 1, c + 1), self.board))
        else:
            if r + 1 <= end_index:
                if self.board[r + 1][c] == "--": # make sure square below is clear
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == start_index + 1 and self.board[r + 2][c] == "--": # initial pawn 2 square move
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= start_index:
                    if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if c + 1 <= end_index:
                    if self.board[r+1][c+1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
    
    def get_rook_moves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemy_colour = 'b' if self.white_to_move else 'w'
        length = len(self.board)
        for d in directions:
            for i in range(1,length):
                end_row = r + i*d[0]
                end_col = c + i*d[1]
                if 0 <= end_row < length and 0 <= end_col < length:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--": # empty square
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_colour: # opposing chess piece 
                        moves.append(Move((r,c), (end_row, end_col), self.board))
                        break
                    else : # friendly chess piece
                        break
                else:
                    break

    
    def get_knight_moves(self, r, c, moves):
        pass
    
    def get_bishop_moves(self, r, c, moves):
        pass
    
    def get_queen_moves(self, r, c, moves):
        pass

    def get_king_moves(self, r, c, moves):
        pass

                


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
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
    
    '''
    Override equal method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return ' '.join([str(self.start_row), str(self.start_col), str(self.end_row), str(self.end_col)])

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
