import chess
import random

class Chuck:

    def __init__(self, board, whoAmI):
        self.board = board
        self.whoAmI = whoAmI

    def makeMove(self):
        move = self.randomMove()
        return move

    def randomMove(self):
        for move in self.board.legal_moves:
            isTheMove = random.randint(0, 2)
            if isTheMove:
                return move