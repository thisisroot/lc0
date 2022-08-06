import chess
import random

class Chuck:

    def __init__(self, cg, whoAmI):
        self.cg = cg
        self.board = cg.board
        self.whoAmI = whoAmI

    def makeMove(self):
        move = self.bestMove()
        if move == None:
            return self.randomMove() 
        return move

    def randomMove(self):
        moves = self.cg.legalMoves()
        move = moves[random.randint(0, len(moves))]
        return move
    
    def bestMove(self):
        CHECKMATE = 1000
        STALEMATE = 0
        turnMultiplier = 1 if self.cg.whiteToMove else -1
        opponentMinMaxScore = CHECKMATE
        bestPlayerMove = None
        moves = self.cg.legalMoves()
        for move in moves:
            self.cg.board.push(move)
            opponentMoves = self.cg.legalMoves()
            opponentMaxScore = -CHECKMATE
            for om in opponentMoves:
                self.cg.board.push(om)
                if self.cg.board.is_checkmate():
                    score = -turnMultiplier * CHECKMATE
                elif self.cg.board.is_stalemate():
                    score = STALEMATE
                else:
                    score = -turnMultiplier * self.scoreMaterial(self.cg.boardToList())
                if score > opponentMaxScore:
                    opponentMaxScore = score
                self.cg.board.pop()
            if opponentMaxScore < opponentMinMaxScore :
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = move
            self.cg.board.pop()
        return bestPlayerMove

    def scoreMaterial(self, board):
        pieceScore = {"K":0, "k":0, "Q":10, "q":10, "R":5, "r":5, "B":3, "b":3, "N": 3, "n":3, "P":1, "p":1}
        whiteTup = ("P", "N", "B", "Q", "R", "K")
        bkackTup = ("p", "n", "b", "q", "r", "k")
        score = 0
        for row in board:
            for square in row:
                if square in whiteTup:
                    score += pieceScore[square]
                elif square in bkackTup:
                    score -= pieceScore[square]
        return score
