import chess
import pygame as pg
from pyparsing import Diagnostics
import chess


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

    
screen(1)

def showBoard(board):
    print("<------------->")
    print(board)
    print("<------------->")