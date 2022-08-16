from cgitb import text
import os
import sys
from tkinter import *
from tkinter import messagebox
import chess
import pygame_menu
from game.ChessGame import ChessGame
from game.ChessGame import Move

from engine.Chuck import Chuck
import pygame as pg


WIDTH = HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 300
MOVE_LOG_PANEL_HEIGHT = 512
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



def d_game_state(cg, screen, board, sqSelected, moveLogFont):
    d_board(screen)
    highlightSquares(screen, cg, sqSelected)
    highlightCheck(screen, cg)
    d_piece(screen, board)
    d_moveLog(screen, cg, moveLogFont)
    
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

def d_moveLog(screen, cg, font):
    board = chess.Board()
    moveLogRect = pg.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pg.draw.rect(screen, pg.Color("black"), moveLogRect)
    moveLog = cg.getMoveLog()
    textY = 5
    lineSpacing = 2
    movesPerRow = 3
    moves = movesToList(board.variation_san([chess.Move.from_uci(m) for m in moveLog]))
    for i in range(0, len(moves), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moves):
                text += moves[i+j] + " "
        textObj = font.render(text ,True , pg.Color("gray"))
        textLocation = moveLogRect.move(5, textY)
        screen.blit(textObj, textLocation)
        textY += textObj.get_height() + lineSpacing

def movesToList(moves):
    p = 0
    c = 2
    output = []
    for i in range(len(moves)):
        if i+1 >= len(moves) and c == 2:
            output.append(moves)
            return output
        if i+1 < len(moves):
            if moves[i] == str(c) and moves[i+1] == ".":
                output.append(moves[p:i])
                p = i
                c += 1
        else:
            output.append(moves[p:])
    return output

def set_piece_color(value, color):
    global WHOAMI
    WHOAMI = color
    print(WHOAMI)
    return WHOAMI

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def menu():
    pg.init()
    surface = pg.display.set_mode((400, 300))
    pg.display.set_caption('LC0')
    Icon = pg.image.load('images/logo.png')
    pg.display.set_icon(Icon)
    menu = pygame_menu.Menu('LC0', 400, 300,
                       theme=pygame_menu.themes.THEME_DARK)

    menu.add.text_input('Name :', default='Root')
    menu.add.selector('Color :', [('White', 0), ('Black', 1)], onchange=set_piece_color)
    menu.add.button('Play', rungame)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)

def highlightSquares(screen, cgG, sqSelected):
    piecesB = ['b', 'k', 'n', 'p', 'q', 'r']
    piecesW =  ['B', 'K', 'N','P','Q','R']
    if sqSelected != ():
        r, c = sqSelected
        board = cgG.boardToList()
        if board[r][c] in (piecesW if cgG.whiteToMove else piecesB):
            s = pg.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(pg.Color('blue'))
            screen.blit(s, ((c*SQ_SIZE, r*SQ_SIZE)))
            s.fill(pg.Color('yellow'))
            moves = cgG.getMovesOfPiece(r, c)
            if moves != None and moves != []:
                for move in moves:
                    x, y = cgG.notationToPosition(move)
                    screen.blit(s, (SQ_SIZE*x, SQ_SIZE*y))
def highlightCheck(screen, cgG):
    s = pg.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)
    s.fill(pg.Color('red'))
    if cgG.board.is_attacked_by(chess.BLACK, cgG.getSqNumber(cgG.getKingsPosition(True))):
        x, y = cgG.notationToPosition(cgG.getKingsPosition(True))
        screen.blit(s, (SQ_SIZE*x, SQ_SIZE*y))
    elif cgG.board.is_attacked_by(chess.WHITE, cgG.getSqNumber(cgG.getKingsPosition(False))):
        x, y = cgG.notationToPosition(cgG.getKingsPosition(False))
        screen.blit(s, (SQ_SIZE*x, SQ_SIZE*y))


def rungame():
    global WHOAMI
    cg = ChessGame()
    #print(cg.translate(cg.board))
    pg.init()
    screen = pg.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    pg.display.set_caption('LC0')
    Icon = pg.image.load('images/logo.png')
    pg.display.set_icon(Icon)
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    moveLogFont = pg.font.SysFont("Arial", 16, False, False)
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
            cg.makeMove(lc.makeMove(), log=True)
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
                if sqSelect == (row, column) or column >= 8:
                    sqSelect = ()
                    usrClick = []
                elif len(usrClick) == 0 and cg.boardToList()[row][column] == ".":
                    sqSelect = ()
                    usrClick = []
                else:
                    sqSelect = (row, column)
                    usrClick.append(sqSelect)
                if len(usrClick) == 2:
                    move = Move(usrClick[0], usrClick[1], cg.boardToList())
                    #making promotion legal
                    m = move.getChessNotation()
                    movesofP = cg.getMovesOfPieceByNotation(m[:2])
                    for i in movesofP:
                        if i == m+'q':
                            m = i
                    cg.makeMove(chess.Move.from_uci(m), log=True)
                    sqSelect = ()
                    usrClick = []
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    cg.undoMoveWithLog()
                    cg.undoMoveWithLog()
                elif e.key == pg.K_r:
                    cg = ChessGame()
                    sqSelect = ()
                    usrClick = [] 
        d_game_state(cg, screen, cg.boardToList(), sqSelect, moveLogFont)
        clock.tick(MAX_FPS)
        pg.display.flip()
    pg.quit()