#!/usr/bin/python3
# -*- coding: utf-8 -*-
import copy
import random

from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame

from tetris.Shape import Shape, Tetrominoe


class Board(QFrame):
    BoardWidth = 10  # 水平方向容纳方块的个数
    BoardHeight = 22  # 垂直方向容纳方块的个数
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.setFocusPolicy(Qt.StrongFocus)
        self.isWaitingAfterLine = False
        self.timer = QBasicTimer()
        self.board = [[Tetrominoe.NoShape.value for j in range(Board.BoardWidth)] for i in range(Board.BoardHeight)]

    def start(self):
        self.newPiece()
        self.timer.start(Board.Speed, self)

    # 设置已经落下完成的图块
    def setShapeAt(self, x, y, shape):
        self.board[y][x] = shape

    def shapeAt(self, x, y):
        return self.board[y][x]

    def squareWidth(self):
        # 每个方块的宽度
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        # 每块方块的长度
        return self.contentsRect().height() // Board.BoardHeight

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        topMargin = rect.bottom() - self.squareHeight() * Board.BoardHeight

        # 渲染已经存在的图块
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.board[i][j]
                if shape != Tetrominoe.NoShape.value:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    topMargin + i * self.squareHeight(),
                                    shape)

        if self.curPiece.shape() != Tetrominoe.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY + self.curPiece.y(i)
                self.drawSquare(painter,
                                rect.left() + x * self.squareWidth(),
                                topMargin + y * self.squareHeight(),
                                self.curPiece.shape())

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                # self.newPiece()
            elif self.curPiece.shape() != Tetrominoe.NoShape.value:
                self.oneLineDown()
        else:
            super(Board, self).timerEvent(event)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
        elif key == Qt.Key_Space:
            self.dropDown()
        elif key == Qt.Key_D:
            self.oneLineDown()

    def dropDown(self):
        newY = self.curY
        while newY <= Board.BoardHeight:
            if not self.tryMove(self.curPiece, self.curX, newY):
                break
            newY += 1

        self.pieceDropped()

    # 移除已经满的行
    def removeFullLines(self):
        removeLines = []
        print('removeFullLines')
        for i in range(Board.BoardHeight):
            count = 0
            for j in range(Board.BoardWidth):
                if self.board[i][j] != Tetrominoe.NoShape.value:
                    count += 1
            if count == Board.BoardWidth:
                removeLines.append(i)

        # 移除已满行数 (将上一行的数据覆盖到下一行)
        if len(removeLines) > 0:
            print('removeFullLines:', removeLines)
            for num in removeLines:
                # 删除已经满的一行
                if num < Board.BoardHeight:
                    del self.board[num]
                # 在矩阵起始位置添加空白的一行
                self.board.insert(0, [Tetrominoe.NoShape.value for i in range(Board.BoardWidth)])

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape.value)
            self.update()

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY + 1):
            self.pieceDropped()

    # 图块 已经落下完成
    def pieceDropped(self):
        print('pieceDropped')
        # 记录每个图块的位置
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY + self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()
        if not self.isWaitingAfterLine:
            print('newPiece')
            self.newPiece()

    # 移动整个图形
    def tryMove(self, newPiece, newX, newY):
        # 一次移动一个方块的位置
        for i in range(4):
            # 判断每个方块是否可以继续移动
            x = newX + newPiece.x(i)
            y = newY + newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            # 判断是和已有图块重合
            if self.board[y][x] != Tetrominoe.NoShape.value:
                return False

        self.curX = newX
        self.curY = newY
        self.curPiece = newPiece
        self.update()
        return True

    def newPiece(self):
        self.curPiece = Shape()
        # self.curPiece.setShape(Tetrominoe.SquareShape.value)
        self.curPiece.setRandomShape()
        # 代表 图形零点的坐标
        # 加上坐标超出屏幕的大小
        self.curX = random.randint(1, Board.BoardWidth - 2) + abs(self.curPiece.minX())  # 算出随机水平出现的格数
        self.curY = abs(self.curPiece.minY())  # 距离上方的格数

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        # 画出一个矩形
        color = QColor(colorTable[shape])
        # 矩形中间的颜色填充 （需要减去线的宽度）
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        # 高亮的线
        painter.setPen(color.lighter())
        painter.drawLine(x, y, x, y + self.squareHeight() - 1)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        # 暗色的线 形成方块之间的空隙
        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, y + 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
