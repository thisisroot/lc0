import chess
import random
from ChessGame import ChessGame

from Chuck import Chuck
from Player import Player
from Visual import showBoard

def main():
    print("<-------- Welcome To LC0 -------->")
    whoAmI = not bool(int(input("LC0 : Choose Your Color \n\tWhite => 1\n\tBlack => 0\nYou :  ")))
    cg = ChessGame()
    while cg.gameIsOn:
        showBoard(cg.board)
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
