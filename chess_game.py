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

        self.board = np.full((8,8,2),EMPTY)
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

       # place all black pieces
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
        dispString += "  a b c d e f g h\n"
        self.error = ""
        for rank in range(8):
            dispString += str(7-rank+1)
            dispString += ' '
            for file_ in range(8):
                whitePiece = self.board[file_, 7-rank, WHITE]
                blackPiece = self.board[file_, 7-rank, BLACK]
                blackSquare = False if ( (file_+rank) % 2 == 0 ) else True
                fColor = '1;37;40' if blackSquare else '0;30;107'
                if   whitePiece != EMPTY:
                    pieceSymbol = self.SYMBOL_DICT_FILLED[whitePiece] if blackSquare else self.SYMBOL_DICT_EMPTY[whitePiece]
                    dispString += '\x1b[%sm%s\x1b[0m' % (fColor, pieceSymbol)
                elif blackPiece != EMPTY:
                    pieceSymbol = self.SYMBOL_DICT_EMPTY[blackPiece] if blackSquare else self.SYMBOL_DICT_FILLED[blackPiece]
                    dispString += '\x1b[%sm%s\x1b[0m' % (fColor, pieceSymbol)
                else:
                    dispString += '\x1b[%sm \x1b[0m' % (fColor)
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
        piece = self.board[fileI, rankI, color]
        if (piece == EMPTY):
            if logError: self.error = f"No {self.COLOR_DICTIONARY[color]} piece in position ({self.FILE_DICTIONARY[fileI]}, {rankI+1})"
            return False
        if (fileI==fileO) and (rankI == rankO):
            if logError: self.error = f"Have to move piece to new position!"
            return False
        if self.board[fileO, rankO, color] != EMPTY:
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
        legal = True
        if fileI == fileO:
            maxRank = max(rankI,rankO)
            minRank = min(rankI,rankO)
            for rank in range(minRank+1, maxRank):
                legal = self.board[fileI, rank, WHITE]==EMPTY and self.board[fileI, rank, BLACK]==EMPTY
                if not legal:
                    return legal
        else:
            maxFile = max(fileI,fileO)
            minFile = min(fileI,fileO)
            for file_ in range(minFile+1, maxFile):
                legal = legal and self.board[file_, rankI, WHITE]==EMPTY and self.board[file_, rankI, BLACK]==EMPTY
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
            legal = self.board[fileI + fileSign*i, rankI + rankSign*i, WHITE]==EMPTY and self.board[ fileI + fileSign*i, rankI + rankSign*i, BLACK]==EMPTY
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
            legal = True if self.board[fileO, rankO, otherColor] == EMPTY else False
        elif move == ( 1, direction) or move == (-1, direction): 
            legal = True if self.board[fileO, rankO, otherColor] != EMPTY else False
        elif move == ( 0, 2*direction) and 3*direction % 7 == rankO:
            legal = True if self.board[fileO, rankO, otherColor] == EMPTY else False
        return legal

    def Move(self, fileI, rankI, fileO, rankO, color):
        piece = self.board[fileI, rankI, color]
        otherColor = BLACK if color == WHITE else WHITE
        legal = self.IsLegalMove(fileI, rankI, fileO, rankO, color)

        if legal:
            self.board[fileI, rankI, color] = EMPTY
            self.board[fileO, rankO, color] = piece
            killedPiece = self.board[fileO, rankO, otherColor]
            self.board[fileO, rankO, otherColor] = EMPTY
            if self.IsCheck(color):
                self.board[fileI, rankI, color] = piece
                self.board[fileO, rankO, color] = EMPTY
                self.board[fileO, rankO, otherColor] = killedPiece
                self.error = "Can't put yourself in check"
                return False
        return legal

    def IsCheck(self, color):
        otherColor = BLACK if color == WHITE else WHITE
        pieceCoords = np.where(self.board[:,:,otherColor] != EMPTY)
        kingCoords = np.where(self.board[:,:,color] == KING)
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
        if not self.IsCheck(color):
            return False
        pieceCoords = np.where(self.board[:,:,color] != EMPTY)
        for i in range(pieceCoords[0].size):
            fileI = pieceCoords[0][i]
            rankI = pieceCoords[1][i]
            piece = self.board[fileI,rankI,color]
            for move in self.MOVE_DICT[piece]:
                fileO = fileI + move[0]
                rankO = rankI + move[1]
                legal = self.IsLegalMove(fileI, rankI, fileO, rankO, color, logError = False)
                if legal:
                    otherColor = BLACK if color == WHITE else WHITE
                    self.board[fileI, rankI, color] = EMPTY
                    self.board[fileO, rankO, color] = piece
                    killedPiece = self.board[fileO, rankO, otherColor]
                    self.board[fileO, rankO, otherColor] = EMPTY
                    check = self.IsCheck(color)
                    self.board[fileI, rankI, color] = piece
                    self.board[fileO, rankO, color] = EMPTY
                    self.board[fileO, rankO, otherColor] = killedPiece
                    if not check:
                        return False
        return True


if __name__ == "__main__":
    chessGame = ChessGame()
    i = 0
    # In case someone has modified the starting positions,
    # we want to check if anyone has won in the start of the
    # game.

    # In this case, debugging is a likely motive, and to make
    # that process easier, the screen is not cleared
    if   chessGame.IsCheckMate(WHITE):
        chessGame.DispState()
        print("Black has won the game!")
        exit()
    elif chessGame.IsCheckMate(BLACK):
        chessGame.DispState()
        print("White has won the game!")
        exit()
    while True:
        color = i%2
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
            i += 1
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
