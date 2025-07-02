import unittest
from ChessEngine import GameState
from ChessEngine import Move

# Test functions must start with test
class test_starting_pawn_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]

    def test_white_starting_posiiton(self):
        valid_moves = self.gs.get_valid_moves()
        compare = []
        for i in range(0,8,1):
            compare.append(Move((6,i), (5,i), self.gs.board))
            compare.append(Move((6,i), (4,i), self.gs.board))
        self.assertEqual(valid_moves, compare, "Starting white pawn moves do not match")
    
    def test_black_starting_position(self):
        self.gs.white_to_move = False
        valid_moves = self.gs.get_valid_moves()
        compare = []
        for i in range(0,8,1):
            compare.append(Move((1,i), (2,i), self.gs.board))
            compare.append(Move((1,i), (3,i), self.gs.board))
        self.assertEqual(valid_moves, compare, "Starting black pawn moves do not match")

class test_taking_pawn_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ]

    def test_white_pawn_takes(self):
        valid_moves = self.gs.get_valid_moves()
        compare = []
        for i in range(0,len(self.gs.board[0]),1):
            cols = [-1,1]
            for col in cols:
                end_col = col + i
                if 0 <= end_col < len(self.gs.board[0]):
                    compare.append(Move((1,i), (0, end_col), self.gs.board))
        self.assertEqual(valid_moves, compare)
    
    def test_black_pawn_takes(self):
        self.gs.white_to_move = False
        valid_moves = self.gs.get_valid_moves()
        compare = []
        for i in range(0, len(self.gs.board[0]), 1):
            cols = [-1, 1]
            for col in cols:
                end_col = col + i
                if 0 <= end_col < len(self.gs.board[0]):
                    compare.append(Move((0,i), (1,end_col), self.gs.board))
        self.assertEqual(valid_moves, compare)

class test_pawn_reached_other_side_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            # ["--", "--", "--", "--", "--", "--", "--", "--"], 
            # ["--", "--", "--", "--", "--", "--", "--", "--"], 
            # ["--", "--", "--", "--", "--", "--", "--", "--"], 
            # ["--", "--", "--", "--", "--", "--", "--", "--"], 
            # ["--", "--", "--", "--", "--", "--", "--", "--"], 
            # ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"]
        ]
    
    # Ignoring promotions for now
    def test_white_pawn_eigth_rank_moves(self):
        valid_moves = self.gs.get_valid_moves()
        compare = []
        self.assertEqual(valid_moves, compare)

    def test_black_pawn_first_rank_moves(self):
        self.gs.white_to_move = False
        valid_moves = self.gs.get_valid_moves()
        compare = []
        self.assertEqual(valid_moves, compare)

class put_piece_at_position():
    '''
        Places a piece on the board at board[row][col]
        Initally the piece is placed at board[0][0] with prev_row == -1 and prev_col == -1
        Otherwise it takes the piece from board[prev_row][prev_col] and places it at board[row][col]
    '''
    def put_piece_at_position(self, row, col, prev_row, prev_col, piece, board):
        if prev_row == -1 and prev_col == -1:
            board[row][col] = piece
        else:
            board[row][col] = board[prev_row][prev_col]
            board[prev_row][prev_col] = "--"
        return board
    
    def surround_piece_template(self, row, col, piece, board, locations):
        for location in locations:
            end_row = row + location[0]
            end_col = col + location[1]
            if 0 <= end_row < len(board) and 0 <= end_col < len(board[0]):
                board[end_row][end_col] = piece
    '''
    Place piece in all available squares such that board[row][col] is surrounded
    '''
    def surround_piece(self, row, col, piece, board):
        locations = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (1, 1), (-1, 1)]
        self.surround_piece_template(row, col, piece, board, locations)

    def suround_knight(self, row, col, piece, board):
        locations = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        self.surround_piece_template(row, col, piece, board, locations)

class back_rank_movement():
    def __init__(self, row, col, prev_row, prev_col, piece, movements, limit, gs):
        self.row = row
        self.col = col
        self.prev_row = prev_row
        self.prev_col = prev_col
        self.piece = piece
        self.movements = movements
        self.limit = limit
        self.gs = gs
        self.rows = len(self.gs.board)
        self.cols = len(self.gs.board[0])
        self.position = put_piece_at_position()
    
    def movement(self, white):
        if white : 
            self.position.put_piece_at_position(self.row, self.col, self.prev_row, self.prev_col, "w" + self.piece, self.gs.board)
        else:
            self.gs.white_to_move = False
            self.position.put_piece_at_position(self.row, self.col, self.prev_row, self.prev_col, "b" + self.piece, self.gs.board)
        valid_moves = self.gs.get_valid_moves()
        compare = []
        for movement in self.movements:
            for j in range(1,self.limit):
                end_row = self.row + j * movement[0]
                end_col = self.col + j * movement[1]
                if 0 <= end_row < self.rows and 0 <= end_col < self.cols:
                    compare.append(Move((self.row, self.col), (end_row, end_col), self.gs.board))
        return valid_moves, compare
    
    def takes(self, white):
        if white : 
            self.position.put_piece_at_position(self.row, self.col, self.prev_row, self.prev_col, "w" + self.piece, self.gs.board)
            self.position.surround_piece(self.row, self.col, "bp", self.gs.board)
        else:
            self.gs.white_to_move = False
            self.position.put_piece_at_position(self.row, self.col, self.prev_row, self.prev_col, "b" + self.piece, self.gs.board)
            self.position.surround_piece(self.row, self.col, "wp", self.gs.board)
        valid_moves = self.gs.get_valid_moves()
        compare = []
        for movement in self.movements:
            end_row = self.row + movement[0]
            end_col = self.col +  movement[1]
            if 0 <= end_row < self.rows and 0 <= end_col < self.cols:
                    compare.append(Move((self.row, self.col), (end_row, end_col), self.gs.board))
        return valid_moves, compare

    def blocked(self, white):
        if white : 
            self.position.put_piece_at_position(self.row, self.col, self.prev_row, self.prev_col, "w" + self.piece, self.gs.board)
            self.position.surround_piece(self.row, self.col, "wD", self.gs.board)
        else:
            self.gs.white_to_move = False
            self.position.put_piece_at_position(self.row, self.col, self.prev_row, self.prev_col, "b" + self.piece, self.gs.board)
            self.position.surround_piece(self.row, self.col, "bD", self.gs.board)
        valid_moves = self.gs.get_valid_moves()
        compare = []
        return valid_moves, compare
    
class test_rook_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.position = put_piece_at_position()
        self.prev_row = -1
        self.prev_col = -1
        self.rows = len(self.gs.board)
        self.cols = len(self.gs.board[0])
        self.length = len(self.gs.board)
        self.no_of_squares = self.length * self.length
        self.movements = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def rook_movement(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            rook_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'R', self.movements, self.length, self.gs)
            valid_moves, compare = rook_movement.movement(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col

    def test_white_rook_movement(self):
        self.rook_movement(True)

    def test_black_rook_movement(self):
        self.rook_movement(False)

    def rook_takes(self, white):
        for i in range(0, self.no_of_squares):
            row = i // 8
            col = i % 8
            rook_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'R', self.movements, self.length, self.gs)
            valid_moves, compare = rook_movement.takes(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_rook_takes(self):
        self.rook_takes(True)
    
    def test_black_rook_takes(self):
        self.rook_takes(False)
    
    def rook_blocked(self, white):
        for i in range(0, self.no_of_squares):
            row = i // 8
            col = i % 8
            rook_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'R', self.movements, self.length, self.gs)
            valid_moves, compare = rook_movement.blocked(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_rook_blocked(self):
        self.rook_blocked(True)
    
    def test_black_rook_blocked(self):
        self.rook_blocked(False)

class test_knight_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.position = put_piece_at_position()
        self.prev_row = -1
        self.prev_col = -1
        self.rows = len(self.gs.board)
        self.cols = len(self.gs.board[0])
        self.length = len(self.gs.board)
        self.no_of_squares = self.length * self.length

    def knight_movement(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            if white:
                self.position.put_piece_at_position(row, col, self.prev_row, self.prev_col, "wN", self.gs.board)
            else:
                self.gs.white_to_move = False
                self.position.put_piece_at_position(row, col, self.prev_row, self.prev_col, "bN", self.gs.board)
            valid_moves = self.gs.get_valid_moves()
            compare = []
            directions = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
            for direction in directions:
                end_row = row + direction[0]
                end_col = col + direction[1]
                if 0 <= end_row < self.rows and 0 <= end_col < self.cols:
                    compare.append(Move((row,col), (end_row, end_col), self.gs.board))
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_knight_movement(self):
        self.knight_movement(True)
    
    def test_black_knight_movement(self):
        self.knight_movement(False)
    
    def knight_takes(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            if white:
                self.position.put_piece_at_position(row, col, self.prev_row, self.prev_col, "wN", self.gs.board)
                self.position.suround_knight(row, col, "bp", self.gs.board)
            else:
                self.gs.white_to_move = False
                self.position.put_piece_at_position(row, col, self.prev_row, self.prev_col, "bN", self.gs.board)
                self.position.suround_knight(row, col, "wp", self.gs.board)
            valid_moves = self.gs.get_valid_moves()
            compare = []
            directions = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
            for direction in directions:
                end_row = row + direction[0]
                end_col = col + direction[1]
                if 0 <= end_row < self.rows and 0 <= end_col < self.cols:
                    compare.append(Move((row,col), (end_row, end_col), self.gs.board))
            print(self.gs.board)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_knight_takes(self):
        self.knight_takes(True)
    
    def test_black_knight_takes(self):
        self.knight_takes(False)

    def knight_blocked(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            if white:
                self.position.put_piece_at_position(row, col, self.prev_row, self.prev_col, "wN", self.gs.board)
                self.position.suround_knight(row, col, "wD", self.gs.board)
            else:
                self.gs.white_to_move = False
                self.position.put_piece_at_position(row, col, self.prev_row, self.prev_col, "bN", self.gs.board)
                self.position.suround_knight(row, col, "bD", self.gs.board)
            valid_moves = self.gs.get_valid_moves()
            compare = []
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_knight_block(self):
        self.knight_blocked(True)
    
    def test_black_knight_block(self):
        self.knight_blocked(True)

class test_bishop_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.position = put_piece_at_position()
        self.prev_row = -1
        self.prev_col = -1
        self.rows = len(self.gs.board)
        self.cols = len(self.gs.board[0])
        self.length = len(self.gs.board)
        self.no_of_squares = self.length * self.length
        self.movements = ((-1, -1), (1, -1), (1, 1), (-1, 1))

    def bishop_movement(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            bishop_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'B', self.movements, self.length, self.gs)
            valid_moves, compare = bishop_movement.movement(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_bishop_movement(self):
        self.bishop_movement(True)
    
    def test_black_bishop_movement(self):
        self.bishop_movement(False)

    def bishop_takes(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            bishop_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'B', self.movements, self.length, self.gs)
            valid_moves, compare = bishop_movement.takes(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col

    def test_white_bishop_takes(self):
        self.bishop_takes(True)
    
    def test_black_bishop_takes(self):
        self.bishop_takes(False)
    
    def bishop_blocked(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            bishop_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'B', self.movements, self.length, self.gs)
            valid_moves, compare = bishop_movement.blocked(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col

    def test_white_bishop_blocked(self):
        self.bishop_blocked(True)
    
    def test_black_bishop_blocked(self):
        self.bishop_blocked(False)

class test_king_movement(unittest.TestCase):
    def setUp(self):
        self.gs = GameState()
        self.gs.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.position = put_piece_at_position()
        self.prev_row = -1
        self.prev_col = -1
        self.rows = len(self.gs.board)
        self.cols = len(self.gs.board[0])
        self.length = len(self.gs.board)
        self.no_of_squares = self.length * self.length
        self.movements = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (1, 1), (-1, 1))
        self.limit = 2
    
    def king_movement(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            king_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'K', self.movements, self.limit, self.gs)
            valid_moves, compare = king_movement.movement(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_king_movement(self):
        self.king_movement(True)
    
    def test_black_king_movement(self):
        self.king_movement(False)

    def king_takes(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            king_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'K', self.movements, self.limit, self.gs)
            valid_moves, compare = king_movement.takes(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col

    def test_white_king_takes(self):
        self.king_takes(True)
    
    def test_black_king_takes(self):
        self.king_takes(False)

    def king_blocked(self, white):
        for i in range(0, self.no_of_squares, 1):
            row = i // 8
            col = i % 8
            king_movement = back_rank_movement(row, col, self.prev_row, self.prev_col, 'K', self.movements, self.limit, self.gs)
            valid_moves, compare = king_movement.blocked(white)
            self.assertEqual(valid_moves, compare)
            self.prev_row = row
            self.prev_col = col
    
    def test_white_king_blocked(self):
        self.king_blocked(True)
    
    def test_black_king_blocked(self):
        self.king_blocked(False)
        
if __name__ == '__main__':
    unittest.main()

    