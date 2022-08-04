import chess

class ChessGame:

    def __init__(self):
        self.board = chess.Board()
        self.whiteToMove = True
        self.gameIsOn = True
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):
        if move in self.board.legal_moves:
            self.board.push(chess.Move.from_uci(str(move)))
            self.whiteToMove = not self.whiteToMove
            return self.board

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
        for i in s:
            if i != " " and i != "\n":
                x.append(i)
            if i == "\n":
                boardList.append(x)
                x = []
        return boardList