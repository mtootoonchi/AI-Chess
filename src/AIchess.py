import chess

class AIChess:
    def __init__(self):
        self.board = chess.Board()

    def makeChessMove(self, uci):
        self.board.push_uci(str(uci))

    def listAllPossibleMoves(self):
            return list(self.board.legal_moves)

    def listUCIPosPossibleMoves(self, uciPos):
        allPossibleMoves = self.listAllPossibleMoves()
        uciPossibleMoves = []
        for Move in allPossibleMoves:
            if Move.uci()[0:2] == uciPos:
                uciPossibleMoves.append(Move)
        return uciPossibleMoves

    def reset(self):
        self.board.reset()

    def willMoveNeedPawnPromotion(self, uci):
        if (str(uci)[1] == '2' and str(uci)[3] == '1' and self.board.piece_at(chess.parse_square(str(uci)[0:2])).symbol().upper() == 'P') or (str(uci)[1] == '7' and str(uci)[3] == '8' and self.board.piece_at(chess.parse_square(str(uci)[0:2])).symbol().upper() == 'P'):
            return True
        else:
            return False

    def pieceToPieceType(self, result):
        if str(result).lower() == 'p':
            return 1
        elif str(result).lower() == 'n':
            return 2
        elif str(result).lower() == 'b':
            return 3
        elif str(result).lower() == 'r':
            return 4
        elif str(result).lower() == 'q':
            return 5
        elif str(result).lower() == 'k':
            return 6
        else:
            return 0

    def rowColToUCI(self, rowColFrom, rowColTo):
        uciCol = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return uciCol[rowColFrom[1]] + str(8 - rowColFrom[0]), uciCol[rowColTo[1]] + str(8 - rowColTo[0])

    def uciToRowCol(self, uci):
        colUCI = dict(a = 0, b = 1, c = 2, d = 3, e = 4, f = 5, g = 6, h = 7)
        return [8 - int(str(uci)[1]), colUCI[str(uci)[0]]], [8 - int(str(uci)[3]), colUCI[str(uci)[2]]]

    def rowColToUCIPos(self, row, col):
        uciCol = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return uciCol[col] + str(8 - row)

    def uciToRowColPos(self, uciPos):
        colUCI = dict(a = 0, b = 1, c = 2, d = 3, e = 4, f = 5, g = 6, h = 7)
        row = 8 - int(uciPos[1])
        col = colUCI[uciPos[0]]
        return row, col

    def uciToFlippedRowCol(self, uci):
        flippedRowColFrom, flippedRowColTo = self.uciToRowCol(uci)
        return self.flipRowCol(flippedRowColFrom, flippedRowColTo)

    def flippedRowColToUCIPos(self, row, col):
        flippedRow, flippedCol = self.flipRowColPos(row, col)
        return self.rowColToUCIPos(flippedRow, flippedCol)

    def uciToFlippedRowColPos(self, uciPos):
        row, col = self.uciToRowColPos(uciPos)
        return self.flipRowColPos(row, col)

    def flipRowCol(self, rowColFrom, rowColTo):
        rowColFrom[0] = 7 - rowColFrom[0]
        rowColFrom[1] = 7 - rowColFrom[1]
        rowColTo[0] = 7 - rowColTo[0]
        rowColTo[1] = 7 - rowColTo[1]
        return rowColFrom, rowColTo

    def flipRowColPos(self, row, col):
        return 7 - row, 7 - col

    def get_board(self):
        return self.board

    def get_boardAs2DList(self):
        boardAs2DList = [['.' for i in range(8)] for j in range(8)]
        for square in chess.SQUARES:
            if self.board.piece_at(square) != None:
                boardAs2DList[int((63 - square) / 8)][square % 8] = self.board.piece_at(square).symbol()
        return boardAs2DList

    def get_boardAs2DListFlipped(self):
        boardAs2DList = [['.' for i in range(8)] for j in range(8)]
        for square in chess.SQUARES:
            if self.board.piece_at(square) != None:
                boardAs2DList[int((square) / 8)][(63 - square) % 8] = self.board.piece_at(square).symbol()
        return boardAs2DList

    def get_isWhiteTurn(self):
        return self.board.turn

    def get_isStartOfGame(self):
        try:
            self.board.peek()
        except IndexError:
            return True
        return False
