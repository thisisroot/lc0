import chess
import random

def showBoard(board):
    print("<------------->")
    print(board)
    print("<------------->")

def makeMove(board, whoAmI, chuckToMove):
    if chuckToMove:
        #its Chuck move
        board.push(chess.Move.from_uci(str(chuckMove(board, whoAmI))))
    else:
        #its Player move
        board.push(chess.Move.from_uci(playerMove(board, whoAmI)))

def chuckMove(board, whoAmI):
    for move in board.legal_moves:
        isTheMove = random.randint(0, 2)
        if isTheMove:
            return move

def playerMove(board, whoAmI):
    move = ""
    isValidMove = False
    print("Choose Your Move Wisely : ")
    while not isValidMove:
        move = input()
        if chess.Move.from_uci(move) in board.legal_moves:
            isValidMove = True
            print("Finally")
            return move
        else:
            print("I Said Choose Your Move Wisely : ")
            
    return move

def main():
    print("<-------- Welcome To LC0 -------->")
    whoAmI = not bool(int(input("LC0 : Choose Your Color \n\tWhite => 1\n\tBlack => 0\nYou :  ")))
    board = chess.Board()
    chuckToMove = whoAmI
    gameIsOn = True
    checkmate = False
    stalemate = False
    while gameIsOn:
        showBoard(board)
        makeMove(board, whoAmI, chuckToMove)
        if checkmate or stalemate:
            gameIsOn = False
            break
        chuckToMove = not chuckToMove

if __name__ == "__main__":
    main()
