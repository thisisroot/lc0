import chess
import random
from ChessGame import ChessGame

from Chuck import Chuck
from Player import Player
from Visual import screen
import pygame as pg


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // WIDTH
MAX_FPS = 30
IMAGES = {}

def Images():
    piecesB = ['b', 'k', 'n', 'p', 'q', 'r']
    piecesW =  ['B', 'K', 'N','P','Q','R']
    for piece in piecesB:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/Black/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    for piece in piecesW:
        IMAGES[piece] = pg.transform.scale(pg.image.load("pieces/White/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
def screen(board):
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock
    screen.fill(pg.Color("white"))
    Images()
    activeness = True
    while activeness:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                activeness = False
        clock.tick(MAX_FPS)
        pg.display.flip()


def main():
    print("<-------- Welcome To LC0 -------->")
    whoAmI = not bool(int(input("LC0 : Choose Your Color \n\tWhite => 1\n\tBlack => 0\nYou :  ")))
    cg = ChessGame()
    #vaziri Code

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock
    screen.fill(pg.Color("white"))
    Images()
    activeness = True
    while cg.gameIsOn and activeness:

        for e in pg.event.get():
            if e.type == pg.QUIT:
                activeness = False
        clock.tick(MAX_FPS)
        pg.display.flip()


        #showBoard(cg.board)
        if whoAmI == cg.whiteToMove:
            lc = Chuck(cg.board, whoAmI)
            cg.makeMove(lc.makeMove())
        else:
            p = Player(cg.board, not whoAmI)
            cg.makeMove(p.makeMove())
        if cg.isGameOver():
            break

if __name__ == "__main__":
    main()
