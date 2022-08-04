import chess
import random

class Chuck:

    def __init__(self, cg, whoAmI):
        self.cg = cg
        self.board = cg.board
        self.whoAmI = whoAmI

    def makeMove(self):
        move = self.randomMove()
        return move

    def randomMove(self):
        moves = self.cg.legalMoves()
        move = moves[random.randint(0, len(moves)- 1)]
        return chess.Move.from_uci(self.board.parse_san(move).uci())