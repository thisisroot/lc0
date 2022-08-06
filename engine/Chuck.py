import chess
import random

class Chuck:

    def __init__(self, cg, whoAmI):
        self.cg = cg
        self.board = cg.board
        self.whoAmI = whoAmI
        self.DEPTH = 2
    def makeMove(self):
        move = self.findBestMoveMinMax(self.cg, self.cg.legalMoves())
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
        random.shuffle(moves)
        for move in moves:
            self.cg.board.push(move)
            opponentMoves = self.cg.legalMoves()
            if self.cg.board.is_checkmate():
                opponentMaxScore = -CHECKMATE
            elif self.cg.board.is_stalemate():
                opponentMaxScore = STALEMATE
            else:
                opponentMaxScore = -CHECKMATE
                for om in opponentMoves:
                    self.cg.board.push(om)
                    if self.cg.board.is_checkmate():
                        score = CHECKMATE
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

    def findBestMoveMinMax(self, cgG, legalmovesG):
        global nextMove
        nextMove = None
        self.findMoveMinMax(cgG, legalmovesG, self.DEPTH, cgG.whiteToMove)
        return nextMove

    def findMoveMinMax(self, cgG, legalmovesG, depth, whiteToMove):
        CHECKMATE = 1000
        STALEMATE = 0
        turnMultiplier = 1 if cgG.whiteToMove else -1
        global nextMove
        if depth == 0:
            return self.scoreMaterial(cgG.boardToList())
        if whiteToMove:
            maxScore = -CHECKMATE
            for move in legalmovesG:
                cgG.makeMove(move)
                nextMoves = cgG.legalMoves()
                score = self.findMoveMinMax(cgG, nextMoves, depth - 1, not whiteToMove)
                if score > maxScore:
                    maxScore = score
                    if depth == self.DEPTH:
                        nextMove = move
                cgG.undoMove()
            return maxScore
        else :
            minScore = CHECKMATE
            for move in legalmovesG:
                cgG.makeMove(move)
                nextMoves = cgG.legalMoves()
                score = self.findMoveMinMax(cgG, nextMoves, depth - 1, not whiteToMove)
                if score < minScore:
                    minScore = score
                    if depth == self.DEPTH:
                        nextMove = move
                cgG.undoMove()
            return minScore
    def scoreBoard(cgG):
        CHECKMATE = 1000
        STALEMATE = 0
        turnMultiplier = 1 if cgG.whiteToMove else -1
        if cgG.board.is_checkmate():
            if cgG.whiteToMove:
                return -CHECKMATE
            else :
                return CHECKMATE
        elif cgG.board.is_stalemate():
            return STALEMATE
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
