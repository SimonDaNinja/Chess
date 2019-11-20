#!/usr/bin/python3
import numpy as np
from chess.constants import *
import os

def ClearScreen():
    if os.name == 'posix':
        os.system('clear')
    if os.name == 'nt':
        os.system('cls')

class ChessGame:

    from chess.dicts import COLOR_DICTIONARY
    from chess.dicts import PIECE_DICTIONARY
    from chess.dicts import FILE_DICTIONARY
    from chess.dicts import SYMBOL_DICT_FILLED
    from chess.dicts import SYMBOL_DICT_EMPTY
    from chess.dicts import MOVE_DICT

    def __init__(self):

        self.board = np.zeros((8,8,2*6))
        self.error = ""

        # Emulating switch-case using a dict mapping pieces to functions
        # The switch is used in IsLegalMove()
        self.IS_LEGAL_SWITCH = {
                                    ROOK:   self.IsLegalRook,
                                    BISHOP: self.IsLegalBishop,
                                    PAWN:   self.IsLegalPawn,
                                    KNIGHT: self.IsLegalKnight,
                                    KING:   self.IsLegalKing,
                                    QUEEN:  self.IsLegalQueen,
                                }

        # place all white pieces
        self.board[ A, 0, WHITE*6 + ROOK ] = 1.0
        self.board[ B, 0, WHITE*6 + KNIGHT ] = 1.0
        self.board[ C, 0, WHITE*6 + BISHOP ] = 1.0
        self.board[ D, 0, WHITE*6 + QUEEN ] = 1.0
        self.board[ E, 0, WHITE*6 + KING ] = 1.0
        self.board[ F, 0, WHITE*6 + BISHOP ] = 1.0
        self.board[ G, 0, WHITE*6 + KNIGHT ] = 1.0
        self.board[ H, 0, WHITE*6 + ROOK ] = 1.0
        self.board[ A, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ B, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ C, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ D, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ E, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ F, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ G, 1, WHITE*6 + PAWN ] = 1.0
        self.board[ H, 1, WHITE*6 + PAWN ] = 1.0

       # place all black pieces
        self.board[ A, 7, BLACK*6 + ROOK ] = 1.0
        self.board[ B, 7, BLACK*6 + KNIGHT ] = 1.0
        self.board[ C, 7, BLACK*6 + BISHOP ] = 1.0
        self.board[ D, 7, BLACK*6 + QUEEN ] = 1.0
        self.board[ E, 7, BLACK*6 + KING ] = 1.0
        self.board[ F, 7, BLACK*6 + BISHOP ] = 1.0
        self.board[ G, 7, BLACK*6 + KNIGHT ] = 1.0
        self.board[ H, 7, BLACK*6 + ROOK ] = 1.0
        self.board[ A, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ B, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ C, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ D, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ E, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ F, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ G, 6, BLACK*6 + PAWN ] = 1.0
        self.board[ H, 6, BLACK*6 + PAWN ] = 1.0

    def DispState(self):
        dispString = self.error + "\n"
        dispString += "  a b c d e f g h\n"
        self.error = ""
        for rank in range(8):
            dispString += str(7-rank+1)
            dispString += ' '
            for file_ in range(8):
                where = np.where(self.board[file_, 7-rank, :] != 0)[0]
                if where.size == 0:
                    pieceColor = None
                else:
                    piece = (where[0] % 6) # There are 6 kinds of pieces in chess; each contributes a channel per color
                    pieceColor = WHITE if where[0] in range(WHITE*6, WHITE*6+6) else BLACK

                blackSquare = False if ( (file_+rank) % 2 == 0 ) else True
                fColor = '1;37;40' if blackSquare else '0;30;107'

                if pieceColor is None:
                    pieceSymbol = ' '
                elif pieceColor == WHITE:
                    pieceSymbol = self.SYMBOL_DICT_FILLED[piece] if blackSquare else self.SYMBOL_DICT_EMPTY[piece]
                else:
                    pieceSymbol = self.SYMBOL_DICT_EMPTY[piece] if blackSquare else self.SYMBOL_DICT_FILLED[piece]
                dispString += '\x1b[%sm%s\x1b[0m' % (fColor, pieceSymbol)
                dispString += '\x1b[%sm \x1b[0m' % (fColor)
            dispString += str(7-rank+1)
            dispString += ' '
            dispString += '\n'
        dispString += "  a b c d e f g h\n"
        print(dispString)

    def IsLegalMove(self, fileI, rankI, fileO, rankO, color, logError = True):

        # Pre-checks
        if (fileI not in range(8)) or (rankI not in range(8)):
            if logError: self.error = f"({self.FILE_DICTIONARY[fileI]}, {rankI}) is out of bounds"
            return False
        if (fileO not in range(8)) or (rankO not in range(8)):
            if logError: self.error = f"({self.FILE_DICTIONARY[fileO]}, {rankO}) is out of bounds"
            return False
        where = np.where(self.board[ fileI, rankI, color*6:(color*6+6) ] != 0)[0]
        if (where.size == 0):
            if logError: self.error = f"No {self.COLOR_DICTIONARY[color]} piece in position ({self.FILE_DICTIONARY[fileI]}, {rankI+1})"
            return False
        piece = where[0]
        if (fileI==fileO) and (rankI == rankO):
            if logError: self.error = f"Have to move piece to new position!"
            return False
        where = np.where(self.board[ fileO, rankO, color*6:(color*6+6) ] != 0)[0]
        if (where.size != 0):
            if logError: self.error = f"Friendly fire is not allowed!"
            return False

        # Emulating switch-case using a dict mapping pieces to functions
        if piece in self.IS_LEGAL_SWITCH:
            legal = self.IS_LEGAL_SWITCH[piece](fileI, rankI, fileO, rankO, color)
        else:
            # Corresponds to default case
            print("critical: unknown piece!\nShutting down game...")
            exit()
        if logError: self.error = "" if legal else "Illegal move!"
        return legal

    def IsLegalKing(self, fileI, rankI, fileO, rankO, color):
        move = (fileO-fileI,rankO-rankI)
        if move in self.MOVE_DICT[KING]:
            return True
        else:
            return False

    def IsLegalQueen(self, fileI, rankI, fileO, rankO, color):
        if self.IsLegalRook(fileI, rankI, fileO, rankO, color):
            return True
        elif self.IsLegalBishop(fileI, rankI, fileO, rankO, color):
            return True
        else:
            return False

    def IsLegalRook(self, fileI, rankI, fileO, rankO, color):
        move = (fileO-fileI,rankO-rankI)
        if not move in self.MOVE_DICT[ROOK]:
            return False
        if fileI == fileO:
            maxRank = max(rankI, rankO)
            minRank = min(rankI, rankO)
            for rank in range(minRank+1, maxRank):
                legal = (self.board[fileI, rank, :] == 0).all()
                if not legal:
                    return legal
        else:
            maxFile = max(fileI,fileO)
            minFile = min(fileI,fileO)
            for file_ in range(minFile+1, maxFile):
                legal = (self.board[fileI, rank, :] == 0).all()
                if not legal:
                    return legal
        return legal

    def IsLegalBishop(self, fileI, rankI, fileO, rankO, color):
        move = (fileO-fileI,rankO-rankI)
        if not move in self.MOVE_DICT[BISHOP]:
            return False
        legal = True
        fileSign = np.sign(fileO-fileI)
        rankSign = np.sign(rankO-rankI)
        distance = abs(fileO-fileI)
        for i in range(1,distance):
            legal = (self.board[fileI + fileSign*i, rankI + rankSign*i, :] == 0).all()
            if not legal:
                return legal
        return legal

    def IsLegalKnight(self, fileI, rankI, fileO, rankO, color):
        move = (fileO-fileI,rankO-rankI)
        return move in self.MOVE_DICT[KNIGHT]

    def IsLegalPawn(self, fileI, rankI, fileO, rankO, color):
        move = (fileO-fileI,rankO-rankI)
        legal = False
        direction = -1 if color == BLACK else 1
        otherColor = WHITE if color == BLACK else BLACK
        if   move == ( 0, direction):
            legal = True if (self.board[fileO, rankO, otherColor*6:(otherColor*6+1)] == 0).all() else False
        elif move == ( 1, direction) or move == (-1, direction): 
            legal = True if (self.board[fileO, rankO, otherColor*6:(otherColor*6+1)] != 0).any() else False
        elif move == ( 0, 2*direction) and 3*direction % 7 == rankO:
            legal = True if (self.board[fileO, rankO, otherColor*6:(otherColor*6+1)] == 0).all() else False
        return legal

    def Move(self, fileI, rankI, fileO, rankO, color):
        otherColor = BLACK if color == WHITE else WHITE
        legal = self.IsLegalMove(fileI, rankI, fileO, rankO, color)

        if legal:
            where =  np.where(self.board[ fileI, rankI, color*6:(color*6+6) ] != 0)[0]
            if (where.size == 0):
                print("critical: move of empty piece passed legality check! (in Move())")
                exit()
            else:
                piece = where[0]
            self.board[fileI, rankI, color*6 + piece] = 0
            self.board[fileO, rankO, color*6 + piece] = 1

            where = np.where(self.board[ fileO, rankO, otherColor*6:(otherColor*6 + 6) ] != 0)[0]
            if (where.size == 0):
                killedPiece = None
            else:
                killedPiece = where[0]

            if killedPiece is not None:
                self.board[fileO, rankO, otherColor*6+killedPiece] = 0

            if self.IsCheck(color):
                self.board[fileI, rankI, color*6 + piece] = piece
                self.board[fileO, rankO, color*6 + piece] = 0
                if killedPiece is not None:
                    self.board[fileO, rankO, otherColor*6+killedPiece] = killedPiece
                self.error = "Can't put yourself in check"
                return False
        return legal

    def IsCheck(self, color):
        otherColor = BLACK if color == WHITE else WHITE
        pieceCoords = np.where(self.board[:,:,otherColor*6:(otherColor*6 + 6)] != 0)
        kingCoords = np.where(self.board[:,:,color*6 + KING] == 1)
        fileO = kingCoords[0][0]
        rankO = kingCoords[1][0]
        for i in range(pieceCoords[0].size):
            fileI = pieceCoords[0][i]
            rankI = pieceCoords[1][i]
            check = self.IsLegalMove(fileI, rankI, fileO, rankO, otherColor, logError = False)
            if check:
                return True
        return False

    def IsCheckMate(self, color):
        # If not in check, it is impossible to be check mate
        if not self.IsCheck(color):
            return False
        pieceCoords = np.where(self.board[:,:,color*6:(color*6+6) != 0])
        for i in range(pieceCoords[0].size):
            fileI = pieceCoords[0][i]
            rankI = pieceCoords[1][i]
            piece = pieceCoords[2][i]
            for move in self.MOVE_DICT[piece]:
                fileO = fileI + move[0]
                rankO = rankI + move[1]
                legal = self.IsLegalMove(fileI, rankI, fileO, rankO, color, logError = False)
                if legal:
                    otherColor = BLACK if color == WHITE else WHITE
                    self.board[fileI, rankI, color*6 + piece] = 0
                    self.board[fileO, rankO, color*6 + piece] = 1
                    where = np.where(self.board[fileO, rankO, otherColor] != 0)
                    if where[0].size != 0:
                        killedPiece = where[0]
                    else:
                        killedPiece = None
                    if killedPiece is not None:
                        self.board[fileO, rankO, otherColor*6+killedPiece] = 0
                    check = self.IsCheck(color)
                    self.board[fileI, rankI, color*6 + piece] = 1
                    self.board[fileO, rankO, color*6 + piece] = 0
                    if killedPiece is not None:
                        self.board[fileO, rankO, otherColor*6 + piece] = killedPiece
                    if not check:
                        return False
        return True


if __name__ == "__main__":
    chessGame = ChessGame()
    color = 0
    # In case someone has modified the starting positions,
    # we want to check if anyone has won in the start of the
    # game.

    # In this case, debugging is a likely motive, and to make
    # that process easier, the screen is not cleared
    chessGame.DispState()
    if   chessGame.IsCheckMate(WHITE):
        chessGame.DispState()
        print("Black has won the game!")
        exit()
    elif chessGame.IsCheckMate(BLACK):
        chessGame.DispState()
        print("White has won the game!")
        exit()
    while True:
        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect piece to move")
            fileIStr = input("choose file [a-h]: ").lower()
            if fileIStr in "abcdefgh" and not fileIStr=="":
                fileI = chessGame.FILE_DICTIONARY[fileIStr]
                break
            else:
                chessGame.error = "file must be in [a-h]!"

        while True:
            ClearScreen()
            chessGame.DispState()
            chessGame.IsCheckMate(WHITE)
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect piece to move")
            rankIStr = input("choose rank [1-8]: ").lower()
            if rankIStr in "12345678" and not rankIStr=="":
                rankI = int(rankIStr)-1
                break
            else:
                chessGame.error = "rank must be in [1-8]!"

        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect where to move")
            fileOStr = input("choose file [a-h]: ").lower()
            if fileOStr in "abcdefgh" and not fileOStr=="":
                fileO = chessGame.FILE_DICTIONARY[fileOStr]
                break
            else:
                chessGame.error = "file must be in [a-h]!"

        while True:
            ClearScreen()
            chessGame.DispState()
            print(f"It is {chessGame.COLOR_DICTIONARY[color]}'s turn\nSelect where to move")
            rankOStr = input("choose rank [1-8]: ").lower()
            if rankOStr in "12345678" and not rankOStr=="":
                rankO = int(rankOStr)-1
                break
            else:
                chessGame.error = "rank must be in [1-8]!"

        legalMove = chessGame.Move(fileI, rankI, fileO, rankO, color)
        if legalMove:
            color ^= 1
            if   chessGame.IsCheckMate(WHITE):
                ClearScreen()
                chessGame.DispState()
                print("Black has won the game!")
                exit()
            elif chessGame.IsCheckMate(BLACK):
                ClearScreen()
                chessGame.DispState()
                print("White has won the game!")
                exit()
