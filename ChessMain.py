"""
Responsible for handling user input and displaying the current game-state object
"""

import pygame as p 
import ChessEngine

WIDTH = HEIGHT = 512 # 400 is another option
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations later on
IMAGES = {}

'''
Initialise a global dictionary of images. Called only once in the main.
'''
def load_images():
    pieces = ["wp", "bp", "wR", "bR", "wB", "bB", "wN", "bN", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
    

'''
Main driver for the code. Handle user input and update graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()
    running = True
    square_selected = () # No square is selected, keep track of the last click of the user (tuple : (row, col))
    player_clicks = [] # Keep track of player clicks
    while running: 
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                print(row,col,gs.board[row][col])
                if square_selected == (row, col):
                    square_selected = () # deselect
                    player_clicks = [] # clear player clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    # print(move.get_chess_notation())
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    # print(gs.board)
                        square_selected = ()
                        player_clicks = []
                    else:
                        player_clicks = [square_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when the key 'z' is pressed
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
            
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Draws all graphics in game state
'''
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

'''
Draw the square on the board
'''
def draw_board(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[(r+c)%2]
            p.draw.rect(screen, colour, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

'''
Draw the pieces onto the board using GameState.board
'''
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == '__main__':
    main()