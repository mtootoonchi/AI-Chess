# AI-Chess

Basic chess features that includes an AI for decision making in Python

# Install Guide

To install packages run in terminal (Python 3.9+):

        pip install AI-Chess

# Quick Tutorial

To start the board and the AI, do the following:

        >>> from AIchess import *
        >>> aic = AIChess()

If you want to take a look at the board do this:

        >>> print(aic.board)
        
If you want to get the board as a 2D list for easy use and print each row do this:

        >>> [print(sub_list) for sub_list in aic.get_boardAs2DList()]
        
If you want to get the board as a flipped 2D list for easy use with white on top and black on bottom but with chess notation like 'a1' still being on white then print each row do this (Extra functions to support this board exist in documentation like automatically flipping the row and col to support this):

        >>> [print(sub_list) for sub_list in aic.get_boardAs2DListFlipped()]
        
If you want change the AI algorithmic minimax depth to a higher number for better accuracy at the cost of computational requirement do this (Default: 3; Needs to be greater than 0):

        >>> aic.minimaxDepth = 2
        
If you want to use the minimax AI to get one of the best possible moves for whoevers turn it is and use that move on the board then print the board do this (This assumes that the game isn't over for any reason):

        >>> aic.makeChessMove(aic.chessAIMove()[0])
        >>> [print(sub_list) for sub_list in aic.get_boardAs2DList()]
        
# Documentation

        __init__()

Initialize the library by creating board: chess.Board which is the starting chess board in the chess library, it is public for you to use however be careful as you can break some functions and minimaxDepth: int which is the depth of the search algorithm. Higher the better but requires move computational power. Single process and needs to be > 0. Default 3.

        chessAIMove() -> List[str]
        
Returns a list of the best possible legal_moves for whoevers turn it is in UCI however, it is possible that one or more of the entries can be the string 'claim_draw' instead of a UCI which is to indicate the desire to claim a draw like FIFTY_MOVES or THREEFOLD_REPETITION

        get_whiteBlackPointsDifference(game: chess.Board) -> int
        
Returns the point difference between white and black where Pawn: 1, Bishop: 3, Knight: 3, Rook: 5, Queen 9

        makeChessMove(uci: chess.Move | str) -> None
        
Needs to be at least pseudo_legal

        listAllPossibleMoves() -> List[Move]
        
Lists all possible legal_moves for whoevers turn it is for each piece

        listUCIPosPossibleMoves(uciPos: str) -> List[Move]
        
Lists all possible legal_moves for whoevers turn it is for the uciPos like 'a2', or 'b1'
Returns an empty List if no possible moves

        reset() -> None 
        
Resets board in chess.Board

        willMoveNeedPawnPromotion(uci: chess.Move | str) -> bool

Return True if move will result in a pawn promotion, False otherwise

        pieceToPieceType(result: chess.Piece | str) -> int
        
Return chess.PieceType as a int

        rowColToUCI(rowColFrom: list[int], rowColTo: list[int]) -> str
        
Accepts two List[int] which is the row and col from and to locations 
Returns a str which is a uci representing the inputs

        uciToRowCol(uci: chess.Move | str) -> List[int], List[int]
        
Accepts a str which is a uci
Returns two List[int] which are the row and col from and to representing the inputs

        rowColToUCIPos(row: int col: int) -> str
        
Accepts a row and col of a 2D list that is the chess board
Returns a uciPos which is a single position like a2 or b1 representing the inputs

        uciToRowColPos(uciPos: str) -> int, int
        
Accepts a uciPos which is a single position like a2 or b1 
Returns a row and col of a 2D list that is the chess board representing the inputs

        uciToFlippedRowCol(uci: chess.Move | str) -> List[int], List[int]
        
Accepts a uci
Returns two List[int] which are the row and col from and to in a 2D list that is the chess board representing 
the inputs but flipped so that white is on top and black is bottom

        flippedRowColToUCIPos(row: int, col: int) -> str
        
Accepts a row and col position that has been flipped so that white is on top and black is on bottom
Returns a uciPos which is a single position like a2 or b1 representing the inputs

        uciToFlippedRowColPos(uciPos: str) -> int, int
        
Accepts a uciPos which is a single position like a2 or b1 
Returns a row and col position that has been flipped so that white is on top and black is on bottom representing the inputs

        flipRowCol(rowColFrom: list[int], rowColTo: list[int]) -> List[int], List[int]
        
Accepts two List[int] which is the row and col from and to locations 
Returns two List[int] which is the row and col from and to locations but flipped so that white is one top and black is on bottom

        flipRowColPos(row: int, col: int) -> int, int
        
Accepts two int which is the row and col for a location
Returns two int which is the row and col for a location but flipped so that white is one top and black is on bottom

        get_boardAs2DList() -> List[int][int]
        
Returns a 2D list that represents the chess board with white on bottom and black on top for easy use 

        get_boardAs2DListFlipped() -> List[int][int]
        
Returns a 2D list that represents the chess board but flipped so white is on top and black is on bottom for easy use 

        get_isWhiteTurn() -> bool
        
Returns a bool where True is if it is white's turn and False if it is black's turn

        get_isStartOfGame() -> bool
        
Returns a bool where True is if it is the start of the game and False if it isn't

# Extra

For more information on how to use this project visit https://python-chess.readthedocs.io/en/latest/ where some of this project uses.