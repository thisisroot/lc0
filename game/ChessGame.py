import random
from turtle import position
import chess
import numpy

class ChessGame:
    
    ranksToRow = {"1":7, "2":6, "3":5, "4":4,"5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRow.items()}
    filesToCols = {"a":0, "b": 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self):
        self.board = chess.Board()
        #self.board = chess.Board("8/8/8/8/8/4K2p/4N2k/8 w KQkq - 0 4")
        self.whiteToMove = True
        self.gameIsOn = True
        self.checkmate = False
        self.stalemate = False
        self.moveLog = []

    def makeMove(self, move, log = False):
        if move in self.board.legal_moves:
            self.board.push(chess.Move.from_uci(str(move)))
            if log:
                self.moveLog.append(str(move))
                #self.moveLog.append(self.board.san(chess.Move(self.getSqNumber(str(move)[:2]), self.getSqNumber(str(move)[2:4]))))
                if(self.whiteToMove):
                    print("White : " + str(move))
                else : 
                    print("Black : " + str(move))
            self.whiteToMove = not self.whiteToMove
            return self.board

    def getMoveLog(self):
        return self.moveLog

    def getSANNotation(self, move, board):
        return str(chess.Board.parse_san(move))

    def undoMoveWithLog(self):
        self.moveLog.pop()
        self.board.pop()
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        self.board.pop()
        self.whiteToMove = not self.whiteToMove

    def isGameOver(self):
        if self.checkmate or self.stalemate:
            self.gameIsOn = False
            return True
    
    def getBoard(self):
        return self.board

    def boardToList(self):
        s = str(self.board)
        boardList = []
        x = []
        for i in range(len(s)):
            if s[i] != " " and s[i] != "\n":
                x.append(s[i])
            if s[i] == "\n":
                boardList.append(x)
                x = []
            if i == len(s) - 1:
                boardList.append(x)
        return boardList
    
    def legalMoves(self):
        s = str(self.board.legal_moves)
        for i in range(len(s)):
            if s[i] == "(":
                s = s[i+1:len(s)-2]
                break
        output = tuple(map(str, s.split(', ')))
        new_output = []
        if output != [] and output is not None:
            for o in output:
                if o != '':
                    new_output.append(chess.Move.from_uci(self.board.parse_san(o).uci()))
        random.shuffle(new_output)
        return new_output

    def removePromotion(self, moves):
        output = []
        for i in moves:
            if len(str(i)) != 5:
                output.append(i)
        return output
    
    def getMovesOfPiece(self, r, c):
        output = []
        moves = self.legalMoves()
        position = self.colsToFiles[c] + self.rowsToRanks[r]
        if moves != []:
            for i in moves:
                m=str(i)
                if m[:2] == position:
                    output.append(m[2:])
        return output
        
    def getMovesOfPieceByNotation(self, position):
        output = []
        moves = self.legalMoves()
        if moves != []:
            for i in moves:
                m=str(i)
                if m[:2] == position:
                    output.append(m)
        return output

    def getPositionOfPiece(self, p):
        board = self.boardToList()
        for i in range(8):
            for j in range(8):
                if board[i][j] == p:
                    return self.colsToFiles[j] + self.rowsToRanks[i]

    def notationToPosition(self, s):
        return (self.filesToCols[s[0]], self.ranksToRow[s[1]])

    def getKingsPosition(self, white):
        board = self.boardToList()
        for i in range(8):
            for j in range(8):
                if board[i][j] == ("K" if white else "k"):
                    return self.colsToFiles[j] + self.rowsToRanks[i]
    
    def getSqNumber(self, s):
        row = {"1":0, "2":1, "3":2, "4":3,"5":4, "6":5, "7":6, "8":7}
        col = {"a":0, "b": 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
        return (row[s[1]] * 8) + col[s[0]]
    
    def printTheBoard(self,board):
        for i in range(8):
            for j in range(8):
                print(str(board[i][j]), end=' ')
            print("\n")
    
    #https://colab.research.google.com/drive/1GSeBQdyZH_nHvl52XW0uhXV3Cslho24O#scrollTo=tAFSOFc8pJf8
    
    def square_to_index(self, square):
            
        squares_index = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7}
        letter = chess.square_name(square)
        return 8 - int(letter[1]), squares_index[letter[0]]
    def translate(self, board):
        # this is the 3d matrix
        board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

        # here we add the pieces's view on the matrix
        for piece in chess.PIECE_TYPES:
            for square in board.pieces(piece, chess.WHITE):
                idx = numpy.unravel_index(square, (8, 8))
                board3d[piece - 1][7 - idx[0]][idx[1]] = 1
            for square in board.pieces(piece, chess.BLACK):
                idx = numpy.unravel_index(square, (8, 8))
                board3d[piece + 5][7 - idx[0]][idx[1]] = 1

        # add attacks and valid moves too
        # so the network knows what is being attacked
        aux = board.turn
        board.turn = chess.WHITE
        for move in board.legal_moves:
            i, j = self.square_to_index(move.to_square)
            board3d[12][i][j] = 1
        board.turn = chess.BLACK
        for move in board.legal_moves:
            i, j = self.square_to_index(move.to_square)
            board3d[13][i][j] = 1
        board.turn = aux
        
        return board3d

    def pieceToBinary(self, p):
        output = []
        board = self.boardToList()
        for row in board:
            temp = []
            for square in row:
                if square == '.':
                    temp.append(0)
                elif square == p:
                    temp.append(1)
                else:
                    temp.append(0)
            output.append(temp)
        return output
    
    def movesToBinary(self, whoAmI):
        color = chess.WHITE if whoAmI else chess.BLACK
        temp = []
        for i in range(64):
            if(chess.Board.is_attacked_by(color, i)):
                temp.append(1)
            else:
                temp.append(0)
        pass
                

class Move():
    ranksToRow = {"1":7, "2":6, "3":5, "4":4,"5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRow.items()}
    filesToCols = {"a":0, "b": 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}
    def __init__(self, startsq, endsq, board):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]