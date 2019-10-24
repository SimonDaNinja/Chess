import numpy as np
from constants.constants import *
import os
BISHOP

# vertical rows are called FILES
# horizontal rows are called RANKS

def ClearScreen():
    if os.name == 'posix':
        os.system('clear')
    if os.name == 'nt':
        os.system('cls')

class ChessGame:

    from constants.dicts import COLOR_DICTIONARY
    from constants.dicts import PIECE_DICTIONARY
    from constants.dicts import RANK_DICTIONARY
    from constants.dicts import SYMBOL_DICT_FILLED
    from constants.dicts import SYMBOL_DICT_EMPTY
    from constants.dicts import MOVE_DICT

    def __init__(self):
        self.board = np.full((8,8,2),EMPTY)
        self.error = ""

        # place all white pieces
        self.board[ A, 0, WHITE ] = ROOK
        self.board[ B, 0, WHITE ] = KNIGHT
        self.board[ C, 0, WHITE ] = BISHOP
        self.board[ D, 0, WHITE ] = QUEEN
        self.board[ E, 0, WHITE ] = KING
        self.board[ F, 0, WHITE ] = BISHOP
        self.board[ G, 0, WHITE ] = KNIGHT
        self.board[ H, 0, WHITE ] = ROOK
        self.board[ A, 1, WHITE ] = PAWN
        self.board[ B, 1, WHITE ] = PAWN
        self.board[ C, 1, WHITE ] = PAWN
        self.board[ D, 1, WHITE ] = PAWN
        self.board[ E, 1, WHITE ] = PAWN
        self.board[ F, 1, WHITE ] = PAWN
        self.board[ G, 1, WHITE ] = PAWN
        self.board[ H, 1, WHITE ] = PAWN

        # place all white pieces
        self.board[ A, 7, BLACK ] = ROOK
        self.board[ B, 7, BLACK ] = KNIGHT
        self.board[ C, 7, BLACK ] = BISHOP
        self.board[ D, 7, BLACK ] = QUEEN
        self.board[ E, 7, BLACK ] = KING
        self.board[ F, 7, BLACK ] = BISHOP
        self.board[ G, 7, BLACK ] = KNIGHT
        self.board[ H, 7, BLACK ] = ROOK
        self.board[ A, 6, BLACK ] = PAWN
        self.board[ B, 6, BLACK ] = PAWN
        self.board[ C, 6, BLACK ] = PAWN
        self.board[ D, 6, BLACK ] = PAWN
        self.board[ E, 6, BLACK ] = PAWN
        self.board[ F, 6, BLACK ] = PAWN
        self.board[ G, 6, BLACK ] = PAWN
        self.board[ H, 6, BLACK ] = PAWN

    def DispState(self):
        dispString = self.error + "\n"
        self.error = ""
        dispString += "  a b c d e f g h\n"
        for file_ in range(8):
            dispString += str(file_+1)
            dispString += ' '
            for rank in range(8):
                whitePiece = self.board[rank, file_, WHITE]
                blackPiece = self.board[rank, file_, BLACK]
                blackSquare = True if ( (rank+file_) % 2 == 0 ) else False
                fColor = '1;37;40' if blackSquare else '0;30;47'
                if   whitePiece != EMPTY:
                    pieceSymbol = self.SYMBOL_DICT_FILLED[whitePiece] if blackSquare else self.SYMBOL_DICT_EMPTY[whitePiece]
                    dispString += '\x1b[%sm%s\x1b[0m' % (fColor, pieceSymbol)
                elif blackPiece != EMPTY:
                    pieceSymbol = self.SYMBOL_DICT_EMPTY[blackPiece] if blackSquare else self.SYMBOL_DICT_FILLED[blackPiece]
                    dispString += '\x1b[%sm%s\x1b[0m' % (fColor, pieceSymbol)
                else:
                    dispString += '\x1b[%sm \x1b[0m' % (fColor)
                dispString += '\x1b[%sm \x1b[0m' % (fColor)
            dispString += '\n'
        print(dispString)

    def MoveIsLegal(self, rankI, fileI, rankO, fileO, color, logError = True):
        otherColor = int(not(color))
        piece = self.board[rankI, fileI, color]

        if (rankI not in range(8)) or (fileI not in range(8)):
            print()
            if logError: self.error = f"({self.RANK_DICTIONARY[rankI]}, {fileI}) is out of bounds"
            return False
        elif (rankO not in range(8)) or (fileO not in range(8)):
            if logError: self.error = f"({self.RANK_DICTIONARY[rankO]}, {fileO}) is out of bounds"
            return False
        elif (piece == EMPTY):
            if logError: self.error = f"No {self.COLOR_DICTIONARY[color]} piece in position ({self.RANK_DICTIONARY[rankI]}, {fileI+1})"
            return False
        elif (rankI==rankO) and (fileI == fileO):
            if logError: self.error = f"Have to move piece to new position!"
            return False
        elif self.board[rankO, fileO, color] != EMPTY:
            if logError: self.error = f"Friendly fire is not allowed!"
            return False
        else:
            move = (rankO-rankI,fileO-fileI)
            legal = False
            if move in self.MOVE_DICT[piece]:
                legal = True
                if piece == ROOK:
                    legal = self.IsLegalRook(rankI, fileI, rankO, fileO)
                elif piece == BISHOP:
                    legal = self.IsLegalBishop(rankI, fileI, rankO, fileO)
                elif piece == QUEEN:
                    if move[0] == 0 or move[1] == 0:
                        legal = self.IsLegalRook(rankI, fileI, rankO, fileO)
                    else:
                        legal = self.IsLegalBishop(rankI, fileI, rankO, fileO)
            elif piece == PAWN:
                legal = self.IsLegalPawn(rankI, fileI, rankO, fileO, color)
        if logError: self.error = "" if legal else "Illegal move!"
        return legal

    def IsLegalRook(self, rankI, fileI, rankO, fileO):
        legal = True
        if rankI == rankO:
            maxFile = max(fileI,fileO)
            minFile = min(fileI,fileO)
            for file_ in range(minFile+1, maxFile):
                legal = self.board[rankI, file_, WHITE]==EMPTY and self.board[rankI, file_, BLACK]==EMPTY
                if not legal:
                    return legal
        else:
            maxRank = max(rankI,rankO)
            minRank = min(rankI,rankO)
            for rank in range(minRank+1, maxRank):
                legal = legal and self.board[rank, fileI, WHITE]==EMPTY and self.board[rank, fileI, BLACK]==EMPTY
                if not legal:
                    return legal
        return legal

    def IsLegalBishop(self, rankI, fileI, rankO, fileO):
        legal = True
        rankSign = np.sign(rankO-rankI)
        fileSign = np.sign(fileO-fileI)
        distance = abs(rankO-rankI)
        for i in range(1,distance):
            legal = self.board[rankI + rankSign*i, fileI + fileSign*i, WHITE]==EMPTY and self.board[ rankI + rankSign*i, fileI + fileSign*i, BLACK]==EMPTY
            if not legal:
                return legal
        return legal

    def IsLegalPawn(self, rankI, fileI, rankO, fileO, color):
        move = (rankO-rankI,fileO-fileI)
        legal = False
        direction = -1 if color == BLACK else 1
        otherColor = WHITE if color == BLACK else BLACK
        if   move == ( 0, direction):
            legal = True if self.board[rankO, fileO, otherColor] == EMPTY else False
        elif move == ( 1, direction) or move == (-1, direction): 
            legal = True if self.board[rankO, fileO, otherColor] != EMPTY else False
        elif move == ( 0, 2*direction) and 3*direction % 7 == fileO:
            legal = True if self.board[rankO, fileO, otherColor] == EMPTY else False
        return legal

    def Move(self, rankI, fileI, rankO, fileO, color):
        piece = self.board[rankI, fileI, color]
        otherColor = int(not(color))
        legal = self.MoveIsLegal(rankI, fileI, rankO, fileO, color)

        if legal:
            self.board[rankI, fileI, color] = EMPTY
            self.board[rankO, fileO, color] = piece
            killedPiece = self.board[rankO, fileO, otherColor]
            self.board[rankO, fileO, otherColor] = EMPTY
            if self.IsCheck(color):
                self.board[rankI, fileI, color] = piece
                self.board[rankO, fileO, color] = EMPTY
                self.board[rankO, fileO, otherColor] = killedPiece
                self.error = "Can't put yourself in check"
                return False
        return legal

    def IsCheck(self, color):
        check = False
        otherColor = BLACK if color == WHITE else WHITE
        pieceCoords = np.where(self.board[:,:,otherColor] != EMPTY)
        kingCoords = np.where(self.board[:,:,color] == KING)
        rankO = kingCoords[0][0]
        fileO = kingCoords[1][0]
        for i in range(pieceCoords[0].size):
            rankI = pieceCoords[0][i]
            fileI = pieceCoords[1][i]
            check = self.MoveIsLegal(rankI, fileI, rankO, fileO, otherColor, logError = False)
            if check:
                break
        return check

    def IsCheckMate(self, color):
        if not self.IsCheck(color):
            return False
        pieceCoords = np.where(self.board[:,:,color] != EMPTY)
        for i in range(pieceCoords[0].size):
            rankI = pieceCoords[0][i]
            fileI = pieceCoords[1][i]
            piece = self.board[rankI,fileI,color]
            for move in self.MOVE_DICT[piece]:
                rankO = move[0]
                fileO = move[1]
                legal = self.MoveIsLegal(rankI, fileI, rankO, fileO, color, logError = False)
                if legal:
                    otherColor = BLACK if color == WHITE else WHITE
                    self.board[rankI, fileI, color] = EMPTY
                    self.board[rankO, fileO, color] = piece
                    killedPiece = self.board[rankO, fileO, otherColor]
                    self.board[rankO, fileO, otherColor] = EMPTY
                    check = self.IsCheck(color)
                    self.board[rankI, fileI, color] = piece
                    self.board[rankO, fileO, color] = EMPTY
                    self.board[rankO, fileO, otherColor] = killedPiece
                    if not check:
                        return False


if __name__ == "__main__":
    chessGame = ChessGame()
    i = 0
    while True:
        color = i%2
        # TODO: error handling
        legalInput = False
        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect piece to move!")
            rankIStr = input("choose rank! [a-h]: ").lower()
            if rankIStr in "abcdefgh":
                rankI = chessGame.RANK_DICTIONARY[rankIStr]
                break
            else:
                chessGame.error = "rank must be in [a-h]!"

        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect piece to move!")
            fileIStr = input("choose file! [1-8]: ").lower()
            if fileIStr in "12345678":
                fileI = int(fileIStr)-1
                break
            else:
                chessGame.error = "file must be in [1-8]!"

        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect where to move!")
            rankOStr = input("choose rank! [a-h]: ").lower()
            if rankIStr in "abcdefgh":
                rankO = chessGame.RANK_DICTIONARY[rankOStr]
                break
            else:
                chessGame.error = "rank must be in [a-h]!"

        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect where to move!")
            fileOStr = input("choose file! [1-8]: ").lower()
            if fileOStr in "12345678":
                fileO = int(fileOStr)-1
                break
            else:
                chessGame.error = "file must be in [1-8]!"

        legalMove = chessGame.Move(rankI, fileI, rankO, fileO, color)
        if legalMove:
            i += 1
        if   chessGame.IsCheckMate(WHITE):
            ClearScreen()
            chessGame.DispState()
            print("Black has won the game!")
            exit()
        elif chessGame.IsCheckMate(BLACK):
            print("White has won the game!")
            exit()
