import tkinter as tk
from tkinter import ttk
from AIchess import *

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('AI Chess')
        self.root.geometry('1200x800')
        self.root.resizable(False, False)
        self.root.iconbitmap(r'img/bp.ico')
        self.chessboard = tk.PhotoImage(file = r'img/chessboard.png')
        self.background = tk.Canvas(self.root, width=1200, height=800)
        self.background.pack(fill = 'both', expand = True)
        self.background.create_image(200, 0, anchor = 'nw', image = self.chessboard)

        self.chessPiecesPhotos = dict(
            P = tk.PhotoImage(file = r'img/wp.png'),
            B = tk.PhotoImage(file = r'img/wB.png'),
            N = tk.PhotoImage(file = r'img/wN.png'),
            R = tk.PhotoImage(file = r'img/wR.png'),
            Q = tk.PhotoImage(file = r'img/wQ.png'),
            K = tk.PhotoImage(file = r'img/wK.png'),
            p = tk.PhotoImage(file = r'img/bp.png'),
            b = tk.PhotoImage(file = r'img/bB.png'),
            n = tk.PhotoImage(file = r'img/bN.png'),
            r = tk.PhotoImage(file = r'img/bR.png'),
            q = tk.PhotoImage(file = r'img/bQ.png'),
            k = tk.PhotoImage(file = r'img/bK.png')
        )

        self.chessPiecesImageID = dict()

        self.aic = AIChess()

        self.isWhiteBottom = True

        self.isTopUser = True
        self.isBottomUser = True

        for i in range(0, 8):
            print(self.aic.get_boardAs2DList()[i])

        self.updateChessPiecesBoard()

        self.flipWhiteAndBlackButton = tk.Button(self.background, text='Flip White\nand Black', command=self.flipWhiteAndBlackButtonFunction)
        self.flipWhiteAndBlackButton.place(x=1062.5, y=362.5, width=75, height=75)

        self.topPlayer = tk.Label(self.background, text='User', font=20)
        self.topPlayer.place(x=105, y=15, width=75, height=75)
        self.topPlayerButton = tk.Button(self.background, text='AI', command=self.topPlayerButtonFunction)
        self.topPlayerButton.place(x=20, y=15, width=75, height=75)

        self.bottomPlayer = tk.Label(self.background, text='User', font=20)
        self.bottomPlayer.place(x=105, y=700, width=75, height=75)
        self.bottomPlayerButton = tk.Button(self.background, text='AI', command=self.bottomPlayerButtonFunction)
        self.bottomPlayerButton.place(x=20, y=700, width=75, height=75)
        
        self.background.bind('<Button-3>', self.rightClickFunction)

        self.startButton = tk.Button(self.background, text='Start', command=self.startButtonFunction)
        self.startButton.place(x=1015, y=700, width=75, height=75)
        self.isStarted = False

        self.pauseButton = tk.Button(self.background, text='Pause', command=self.pauseButtonFunction, state='disabled')
        self.pauseButton.place(x=1105, y=700, width=75, height=75)

        self.resetButton = tk.Button(self.background, text='Reset', command=self.resetButtonFunction)
        self.resetButton.place(x=1015, y=600, width=75, height=75)

        self.undoButton = tk.Button(self.background, text='Undo', command=self.undoButtonFunction, state='disabled')
        self.undoButton.place(x=62.5, y=362.5, width=75, height=75)

        self.chessPieceBorderPhoto = tk.PhotoImage(file = r'img/blackBorder.png')
        self.chessPieceBorderPhoto90x90 = tk.PhotoImage(file = r'img/blackBorder90x90.png')
        self.yellowSquare = tk.PhotoImage(file = r'img/yellowSquare.png')
        self.chessPieceBorderID = self.background.create_image(200, 100, anchor ='nw', image = self.chessPieceBorderPhoto)
        self.background.delete(self.chessPieceBorderID)
        self.chessPieceBorderRowCol = [0, 0]
        self.chessMoveBorderIDs = []
        self.possibleMoves = self.aic.listAllPossibleMoves()
        self.lastMove = [self.background.create_image(0, 0, anchor ='nw', image = self.yellowSquare), self.background.create_image(0, 0, anchor ='nw', image = self.yellowSquare)]
        self.background.delete(self.lastMove[0])
        self.background.delete(self.lastMove[1])

        self.promotionMessage = tk.Label(self.background, text='What do you want your\npawn to promote to?', font=20)
        self.promotionMessage.place(x=1015, y=15)
        self.promotionPieceSelected = tk.StringVar()
        self.promotionPieces = ['Queen', 'Rook', 'Bishop', 'Knight']
        self.promotionPieceChossen = ttk.Combobox(self.background, values=self.promotionPieces, font=20, width = 16, textvariable = self.promotionPieceSelected, state='readonly')
        self.promotionPieceChossen.current(0)
        self.promotionPieceChossen.place(x=1015, y=75)

        self.root.mainloop()

    def chessPiecesOnHoverFunction(self, event):
        self.chessPieceBorderRowCol = [int(event.y / 100), int(event.x / 100) - 2]
        if self.isWhiteBottom:
            chessSquare = self.aic.get_boardAs2DList()[self.chessPieceBorderRowCol[0]][self.chessPieceBorderRowCol[1]].isupper()
        else:
            chessSquare = self.aic.get_boardAs2DListFlipped()[self.chessPieceBorderRowCol[0]][self.chessPieceBorderRowCol[1]].isupper()
        if (chessSquare == self.aic.get_isWhiteTurn()) and self.isStarted:
            self.chessPieceBorderID = self.background.create_image((self.chessPieceBorderRowCol[1] + 2) * 100, self.chessPieceBorderRowCol[0] * 100, anchor ='nw', image = self.chessPieceBorderPhoto)
            self.background.tag_bind(self.chessPieceBorderID, '<Leave>', self.chessPiecesOffHoverFunction, add='+')
            self.background.tag_bind(self.chessPieceBorderID, '<Button>', self.chessPiecesOnClickFunction, add='+')

    def chessPiecesOffHoverFunction(self, event):
        self.background.delete(self.chessPieceBorderID)

    def chessPiecesOnClickFunction(self, event):
        if self.isWhiteBottom:
            self.possibleMoves = self.aic.listUCIPosPossibleMoves(self.aic.rowColToUCIPos(self.chessPieceBorderRowCol[0], self.chessPieceBorderRowCol[1]))
        else:
            self.possibleMoves = self.aic.listUCIPosPossibleMoves(self.aic.flippedRowColToUCIPos(self.chessPieceBorderRowCol[0], self.chessPieceBorderRowCol[1]))
        for ID in self.chessMoveBorderIDs:
            self.background.delete(ID)
        self.chessMoveBorderIDs = []
        for eachMove in self.possibleMoves:
            if self.isWhiteBottom:
                moveRow, moveCol = self.aic.uciToRowColPos(eachMove.uci()[2:4])
            else:
                moveRow, moveCol = self.aic.uciToFlippedRowColPos(eachMove.uci()[2:4])
            self.chessMoveBorderIDs.append(self.background.create_image(((moveCol + 2) * 100) + 5, (moveRow * 100) + 5, anchor ='nw', image = self.chessPieceBorderPhoto90x90))
            self.background.tag_bind(self.chessMoveBorderIDs[-1], '<Button>', self.chessMovesOnClickFunction, add='+')

    def chessMovesOnClickFunction(self, event):
        chessMoveBorderRowCol = [int(event.y / 100), int(event.x / 100) - 2]
        if self.isWhiteBottom:
            chessMoveBorderUCI = self.aic.rowColToUCIPos(chessMoveBorderRowCol[0], chessMoveBorderRowCol[1])
        else:
            chessMoveBorderUCI = self.aic.flippedRowColToUCIPos(chessMoveBorderRowCol[0], chessMoveBorderRowCol[1])
        for eachYellowSquare in self.lastMove:
            self.background.delete(eachYellowSquare)
        print(self.possibleMoves)
        for eachMove in self.possibleMoves:
            if eachMove.uci()[2:4] == chessMoveBorderUCI:
                print(self.aic.willMoveNeedPawnPromotion(eachMove))
                print(eachMove)
                if self.aic.willMoveNeedPawnPromotion(eachMove):
                    if self.promotionPieceSelected.get()[0].lower() != 'k':
                        promotionPiece = self.promotionPieceSelected.get()[0].lower()
                    else:
                        promotionPiece = 'n'
                    self.aic.makeChessMove(str(eachMove)[0:4] + promotionPiece)
                else:
                    self.aic.makeChessMove(eachMove)
                if self.isWhiteBottom:
                    yellowSquareRowColFrom, yellowSquareRowColTo = self.aic.uciToRowCol(eachMove)
                else:
                    yellowSquareRowColFrom, yellowSquareRowColTo = self.aic.uciToFlippedRowCol(eachMove)
                self.lastMove = [self.background.create_image((yellowSquareRowColFrom[1] * 100) + 200, yellowSquareRowColFrom[0] * 100, anchor ='nw', image = self.yellowSquare), self.background.create_image((yellowSquareRowColTo[1] * 100) + 200, yellowSquareRowColTo[0] * 100, anchor ='nw', image = self.yellowSquare)]
                break
        self.updateChessPiecesBoard()
        for ID in self.chessMoveBorderIDs:
            self.background.delete(ID)

    def flipWhiteAndBlackButtonFunction(self):
        self.isWhiteBottom = not self.isWhiteBottom
        self.updateChessPiecesBoard()

    def topPlayerButtonFunction(self):
        if self.isTopUser:
            self.topPlayer.config(text='AI')
            self.topPlayerButton.config(text='User')
            self.isTopUser = not self.isTopUser
        else:
            self.topPlayer.config(text='User')
            self.topPlayerButton.config(text='AI')
            self.isTopUser = not self.isTopUser

    def bottomPlayerButtonFunction(self):
        if self.isBottomUser:
            self.bottomPlayer.config(text='AI')
            self.bottomPlayerButton.config(text='User')
            self.isBottomUser = not self.isBottomUser
        else:
            self.bottomPlayer.config(text='User')
            self.bottomPlayerButton.config(text='AI')
            self.isBottomUser = not self.isBottomUser

    def rightClickFunction(self, event):
        for ID in self.chessMoveBorderIDs:
            self.background.delete(ID)

    def startButtonFunction(self):
        self.pauseButton.config(state='normal')

        self.undoButton.config(state='disabled')

        self.startButton.config(state='disabled')
        self.isStarted = True
        self.flipWhiteAndBlackButton.config(state='disabled')
        self.topPlayerButton.config(state='disabled')
        self.bottomPlayerButton.config(state='disabled')

    def pauseButtonFunction(self):
        self.pauseButton.config(state='disabled')
        self.startButton.config(state='normal')
        self.isStarted = False
        if self.aic.get_isStartOfGame():
            self.undoButton.config(state='disabled')
            self.flipWhiteAndBlackButton.config(state='normal')
        else:
            self.undoButton.config(state='normal')
        self.topPlayerButton.config(state='normal')
        self.bottomPlayerButton.config(state='normal')
        for ID in self.chessMoveBorderIDs:
            self.background.delete(ID)

    def resetButtonFunction(self):
        self.aic.reset()
        self.updateChessPiecesBoard()

        self.topPlayerButton.config(state='normal')
        self.topPlayer.config(text='User')
        self.topPlayerButton.config(text='AI')
        self.isTopUser = True
        self.bottomPlayerButton.config(state='normal')
        self.bottomPlayer.config(text='User')
        self.bottomPlayerButton.config(text='AI')
        self.isBottomUser = True

        self.undoButton.config(state='disabled')
        self.pauseButton.config(state='disabled')
        self.startButton.config(state='normal')
        self.isStarted = False
        self.flipWhiteAndBlackButton.config(state='normal')
        self.isWhiteBottom = True
        self.promotionPieceChossen.current(0)
        for ID in self.chessMoveBorderIDs:
            self.background.delete(ID)
        for eachYellowSquare in self.lastMove:
            self.background.delete(eachYellowSquare)

    def undoButtonFunction(self):
        for eachYellowSquare in self.lastMove:
            self.background.delete(eachYellowSquare)
        if self.isWhiteBottom:
            yellowSquareRowColFrom, yellowSquareRowColTo = self.aic.uciToRowCol(self.aic.get_board().pop())
        else:
            yellowSquareRowColFrom, yellowSquareRowColTo = self.aic.uciToFlippedRowCol(self.aic.get_board().pop())
        self.lastMove = [self.background.create_image((yellowSquareRowColFrom[1] * 100) + 200, yellowSquareRowColFrom[0] * 100, anchor ='nw', image = self.yellowSquare), self.background.create_image((yellowSquareRowColTo[1] * 100) + 200, yellowSquareRowColTo[0] * 100, anchor ='nw', image = self.yellowSquare)]
        self.updateChessPiecesBoard()
        if self.aic.get_isStartOfGame():
            self.undoButton.config(state='disabled')
            self.flipWhiteAndBlackButton.config(state='normal')

    # updates the GUI to reflect changes made through user interaction or AI
    def updateChessPiecesBoard(self):
        if self.isWhiteBottom:
            newChessPiecesBoard = self.aic.get_boardAs2DList()
        else:
            newChessPiecesBoard = self.aic.get_boardAs2DListFlipped()
        for thisDictKeys in self.chessPiecesImageID:
            self.background.delete(self.chessPiecesImageID[thisDictKeys])
        for i in range(0, 8):
            for j in range(0, 8):
                if newChessPiecesBoard[i][j] != '.':
                    self.chessPiecesImageID[newChessPiecesBoard[i][j] + str((8 * i) + j)] = self.background.create_image((j * 100) + 205, (i * 100) + 5, anchor ='nw', image = self.chessPiecesPhotos[newChessPiecesBoard[i][j]])
                    self.background.tag_bind(self.chessPiecesImageID[newChessPiecesBoard[i][j] + str((8 * i) + j)], '<Enter>', self.chessPiecesOnHoverFunction, add='+')

MyGUI()