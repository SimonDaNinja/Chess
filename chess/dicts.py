from chess.constants import *

COLOR_DICTIONARY = { WHITE:"white",
                     BLACK:"black" }
PIECE_DICTIONARY = { EMPTY: "empty",
                     BISHOP:"bishop",
                     KING:  "king",
                     KNIGHT:"knight",
                     PAWN:  "pawn",
                     QUEEN: "queen",
                     ROOK:  "rook"}
RANK_DICTIONARY = { 
                    A:"a",
                    B:"b",
                    C:"c",
                    D:"d",
                    E:"e",
                    F:"f",
                    G:"g",
                    H:"h",
                    "a":A,
                    "b":B,
                    "c":C,
                    "d":D,
                    "e":E,
                    "f":F,
                    "g":G,
                    "h":H
                    }

SYMBOL_DICT_FILLED = {   BISHOP: chr(9821),
                        KING:   chr(9818),
                        KNIGHT: chr(9822),
                        PAWN:   chr(9823),
                        QUEEN:  chr(9819),
                        ROOK:   chr(9820)}

SYMBOL_DICT_EMPTY = {   BISHOP: chr(9815),
                        KING:   chr(9812),
                        KNIGHT: chr(9816),
                        PAWN:   chr(9817),
                        QUEEN:  chr(9813),
                        ROOK:   chr(9814)}

MOVE_DICT = {   ROOK:       {( 0, 1),
                            ( 0, 2),
                            ( 0, 3),
                            ( 0, 4),
                            ( 0, 5),
                            ( 0, 6),
                            ( 0, 7),
                            ( 0, 8),
                            ( 0,-1),
                            ( 0,-2),
                            ( 0,-3),
                            ( 0,-4),
                            ( 0,-5),
                            ( 0,-6),
                            ( 0,-7),
                            ( 0,-8),
                            ( 1, 0),
                            ( 2, 0),
                            ( 3, 0),
                            ( 4, 0),
                            ( 5, 0),
                            ( 6, 0),
                            ( 7, 0),
                            ( 8, 0),
                            (-1, 0),
                            (-2, 0),
                            (-3, 0),
                            (-4, 0),
                            (-5, 0),
                            (-6, 0),
                            (-7, 0),
                            (-8, 0)},
                    KNIGHT:{( 2, 1),
                            ( 2,-1),
                            (-2, 1),
                            (-2,-1),
                            ( 1, 2),
                            ( 1,-2),
                            (-1, 2),
                            (-1,-2)},
                    BISHOP:{( 1, 1),
                            ( 2, 2),
                            ( 3, 3),
                            ( 4, 4),
                            ( 5, 5),
                            ( 6, 6),
                            ( 7, 7),
                            ( 8, 8),
                            (-1,-1),
                            (-2,-2),
                            (-3,-3),
                            (-4,-4),
                            (-5,-5),
                            (-6,-6),
                            (-7,-7),
                            (-8,-8),
                            (-1, 1),
                            (-2, 2),
                            (-3, 3),
                            (-4, 4),
                            (-5, 5),
                            (-6, 6),
                            (-7, 7),
                            (-8, 8),
                            ( 1,-1),
                            ( 2,-2),
                            ( 3,-3),
                            ( 4,-4),
                            ( 5,-5),
                            ( 6,-6),
                            ( 7,-7),
                            ( 8,-8)},
                    KING:{  ( 1, 0),
                            ( 1, 1),
                            ( 0, 1),
                            (-1, 0),
                            (-1,-1),
                            ( 0,-1),
                            ( 1,-1),
                            (-1, 1)},
                    PAWN:{}}
MOVE_DICT[QUEEN] = MOVE_DICT[ROOK]|MOVE_DICT[BISHOP]
