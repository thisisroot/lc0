import chess
import random

class Chuck:

    def __init__(self, cg, whoAmI):
        self.cg = cg
        self.board = cg.board
        self.whoAmI = whoAmI
        self.DEPTH = 14
    def makeMove(self):
        #move = self.bestMove()
        move = self.findBestMove(self.cg, self.cg.legalMoves())
        if move == None:
            return self.randomMove() 
        return move
        #return self.randomMove()

    def randomMove(self):
        moves = self.cg.legalMoves()
        if len(moves) != 0:
            move = moves[random.randint(0, len(moves)-1)]
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
            if len(opponentMoves) == 0 or opponentMoves is None:
                if self.cg.board.is_check():
                    opponentMaxScore = -CHECKMATE
                else :
                    opponentMaxScore = STALEMATE
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

    def findBestMove(self, cgG, legalmovesG):
        CHECKMATE = 1000
        global nextMove, c
        nextMove = None
        c = 0
        #self.findMoveMinMax(cgG, legalmovesG, self.DEPTH, cgG.whiteToMove)
        #self.findMoveNegaMax(cgG, legalmovesG, self.DEPTH, 1 if cgG.whiteToMove else -1)
        self.findMoveNegaMaxAlphaBeta(cgG, legalmovesG, self.DEPTH,-CHECKMATE, CHECKMATE, 1 if cgG.whiteToMove else -1)
        print(c)
        return nextMove

    def findMoveMinMax(self, cgG, legalmovesG, depth, whiteToMove):
        CHECKMATE = 1000
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

    def findMoveNegaMax(self, cgG, legalmovesG, depth, turnMultiplier):
        global nextMove, c
        c += 1
        CHECKMATE = 1000
        STALEMATE = 0
        if depth == 0:
            return turnMultiplier * self.scoreBoard(cgG)
        maxScore = -CHECKMATE
        for move in legalmovesG :
            cgG.makeMove(move)
            nextMoves = cgG.legalMoves()
            score = - self.findMoveNegaMax(cgG, nextMoves, depth - 1, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.DEPTH:
                    nextMove = move
            cgG.undoMove()
        return maxScore

    def findMoveNegaMaxAlphaBeta(self, cgG, legalmovesG, depth, alpha, beta, turnMultiplier):
        global nextMove, c
        c+=1
        CHECKMATE = 1000
        STALEMATE = 0
        if depth == 0:
            return turnMultiplier * self.scoreBoard(cgG)
        maxScore = -CHECKMATE
        for move in legalmovesG :
            cgG.makeMove(move)
            nextMoves = cgG.removePromotion(cgG.legalMoves())
            score = - self.findMoveNegaMaxAlphaBeta(cgG, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.DEPTH:
                    nextMove = move
            cgG.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore

    def scoreBoard(self, cgG):
        CHECKMATE = 1000
        STALEMATE = 0
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
        for row in cgG.boardToList():
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
