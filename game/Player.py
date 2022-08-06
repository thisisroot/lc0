import chess
from pygame import init

class Player:
    def __init__(self, board, whoAmI):
        self.board = board
        self.whoAmI = whoAmI
    
    def makeMove(self):
        move = ""
        isValidMove = False
        print("Choose Your Move Wisely : ")
        while not isValidMove:
            move = input()
            if chess.Move.from_uci(move) in self.board.legal_moves:
                isValidMove = True
                print("Finally")
                return chess.Move.from_uci(move)
            else:
                print("I Said Choose Your Move Wisely : ")
        return chess.Move.from_uci(move)