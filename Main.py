from tkinter import *
from tkinter import messagebox
import chess
import random
from ChessGame import ChessGame
from ChessGame import Move

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
    cg.boardToList()
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    Images()
    activeness = True
    sqSelect = ()
    usrClick = []
    while activeness:
        if cg.board.outcome():
            if cg.whiteToMove:
                Tk().wm_withdraw() #to hide the main window
                messagebox.showinfo('!','BLACK Wins')
            else:
                Tk().wm_withdraw() #to hide the main window
                messagebox.showinfo('!','WHITE Wins')
            break
        if cg.whiteToMove == whoAmI:
            lc = Chuck(cg, whoAmI)
            cg.makeMove(lc.makeMove())
        for e in pg.event.get():
            if e.type == pg.QUIT:
                activeness = False
            elif e.type == pg.MOUSEBUTTONUP:
                if cg.whiteToMove == whoAmI:
                    break
                
                loc = pg.mouse.get_pos()
                column = loc[0] // SQ_SIZE
                row = loc[1] // SQ_SIZE
                if sqSelect == (row, column):
                    sqSelect = ()
                    usrClick = []
                else:
                    sqSelect = (row, column)
                    usrClick.append(sqSelect)
                if len(usrClick) == 2:
                    move = Move(usrClick[0], usrClick[1], cg.boardToList())
                    cg.makeMove(chess.Move.from_uci(move.getChessNotation()))
                    sqSelect = ()
                    usrClick = []

                
        d_game_state(screen, cg.boardToList())
        clock.tick(MAX_FPS)
        pg.display.flip()

if __name__ == "__main__":
    main()
