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
    load_images()
    running = True
    
    while running: 
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Draws all graphics in game state
'''
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''
Draw the square on the board
'''
def drawBoard(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[(r+c)%2]
            p.draw.rect(screen, colour, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

'''
Draw the pieces onto the board using GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


if __name__ == '__main__':
    main()