from tkinter import *
from tkinter import messagebox
import chess
import pygame_menu
from game.ChessGame import ChessGame
from game.ChessGame import Move

from engine.Chuck import Chuck
import pygame as pg


HEIGHT = 512
WIDTH = HEIGHT * 1.5
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
WHOAMI = 0

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

def set_piece_color(value, color):
    global WHOAMI
    WHOAMI = color
    print(WHOAMI)
    return WHOAMI

def menu():
    pg.init()
    surface = pg.display.set_mode((400, 300))
    pg.display.set_caption('LC0')
    Icon = pg.image.load('images/logo.png')
    pg.display.set_icon(Icon)
    menu = pygame_menu.Menu('LC0', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)

    menu.add.text_input('Name :', default='Root')
    menu.add.selector('Difficulty :', [('White', 0), ('Black', 1)], onchange=set_piece_color)
    menu.add.button('Play', rungame)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

def rungame():
    global WHOAMI
    cg = ChessGame()
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('LC0')
    Icon = pg.image.load('images/logo.png')
    pg.display.set_icon(Icon)
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    Images()
    activeness = True
    sqSelect = ()
    usrClick = []
    while activeness:
        if cg.board.outcome():
            if cg.board.is_checkmate():
                if cg.whiteToMove:
                    Tk().wm_withdraw() #to hide the main window
                    messagebox.showinfo('!','BLACK Wins')
                else:
                    Tk().wm_withdraw() #to hide the main window
                    messagebox.showinfo('!','WHITE Wins')
            else:
                Tk().wm_withdraw() #to hide the main window
                messagebox.showinfo('!','DRAW')
            break
        if cg.whiteToMove == WHOAMI:
            lc = Chuck(cg, WHOAMI)
            cg.makeMove(lc.makeMove())
        for e in pg.event.get():
            if e.type == pg.QUIT:
                activeness = False
                pg.quit()
            elif e.type == pg.MOUSEBUTTONUP:
                if cg.whiteToMove == WHOAMI:
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
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    cg.undoMove()
                    cg.undoMove()
                elif e.key == pg.K_r:
                    cg = ChessGame()
                    sqSelect = ()
                    usrClick = [] 
        d_game_state(screen, cg.boardToList())
        clock.tick(MAX_FPS)
        pg.display.flip()
    pg.quit()