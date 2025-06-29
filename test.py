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

    
if __name__ == '__main__':
    unittest.main()

    