from turtle import position
import chess

class ChessGame:

    ranksToRow = {"1":7, "2":6, "3":5, "4":4,"5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRow.items()}
    filesToCols = {"a":0, "b": 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self):
        self.board = chess.Board()
        self.whiteToMove = True
        self.gameIsOn = True
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):
        if move in self.board.legal_moves:
            self.board.push(chess.Move.from_uci(str(move)))
            if(self.whiteToMove):
                print("White : " + str(move))
            else : 
                print("Black : " + str(move))
            self.whiteToMove = not self.whiteToMove
            return self.board

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
                new_output.append(chess.Move.from_uci(self.board.parse_san(o).uci()))
        return new_output
    
    def getMovesOfPiece(self, p, r, c):
        output = []
        moves = self.legalMoves()
        position = self.colsToFiles[c] + self.rowsToRanks[r]
        if moves != []:
            for i in moves:
                m=str(i)
                if m[:2] == position:
                    output.append(m[2:])
        return output
        
    def getPositionOfPiece(self, p):
        board = self.boardToList()
        for i in range(8):
            for j in range(8):
                if board[i][j] == p:
                    print(i, j)
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