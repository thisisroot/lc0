from tkinter.tix import IMAGE
import chess
import random
from ChessGame import ChessGame

from Chuck import Chuck
from Player import Player
import pygame as pg


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def Images():
    piecesB = ['b', 'k', 'n', 'p', 'q', 'r']
    piecesW =  ['B', 'K', 'N','P','Q','R']
    for piece in piecesB:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/Black/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    for piece in piecesW:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/White/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))



def d_game_state(screen, board):
    d_board(screen)
    d_piece(screen, board)
    
def d_board(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors [((row + column) % 2)]
            pg.draw.rect(screen, color, pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    
    
def d_piece(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '.':
                screen.blit(IMAGES[piece], pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def main():
    print("<-------- Welcome To LC0 -------->")
    whoAmI = not bool(int(input("LC0 : Choose Your Color \n\tWhite => 1\n\tBlack => 0\nYou :  ")))
    cg = ChessGame()
    #vaziri Code

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    Images()
    activeness = True
    sqSelect = ()
    usrClick = []
    while activeness:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                activeness = False
            elif e.type == pg.MOUSEBUTTONUP:
                loc = pg.mouse.get_pos()
                column = loc[0] // SQ_SIZE
                row = loc[1] // SQ_SIZE
                if sqSelect == (row, column):
                    sqSelect = ()
                    usrClick = []
                else:
                    sqSelect = (row, column)
                    usrClick.append(sqSelect)
                
        d_game_state(screen, cg.board)
        clock.tick(MAX_FPS)
        pg.display.flip()

        #showBoard(cg.board)
        # if whoAmI == cg.whiteToMove:
        #     lc = Chuck(cg.board, whoAmI)
        #     cg.makeMove(lc.makeMove())
        # else:
        #     p = Player(cg.board, not whoAmI)
        #     cg.makeMove(p.makeMove())
        # if cg.isGameOver():
        #     break

if __name__ == "__main__":
    main()
