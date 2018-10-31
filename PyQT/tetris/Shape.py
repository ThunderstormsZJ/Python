#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
import random
from enum import Enum


# 代表方块的类型
class Tetrominoe(Enum):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredShape = 7


# 方块
class Shape(object):
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1)),
    )

    def __init__(self):
        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

    def __str__(self):
        shapeDes = '{ Shape: %s } {' % self.pieceShape
        for i in range(4):
            shapeDes += ' (x=%d,y=%d) ' % (self.coords[i][0], self.coords[i][1])

        shapeDes += '}'
        return shapeDes

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):
        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])
        return m

    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])
        return m

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])
        return m

    def maxY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])
        return m

    def rotateAlpha(self, alpha, coords):
        radian = alpha * math.pi / 180
        # 处理趋近0的情况
        radCos = round(math.cos(radian), 15)
        radSin = round(math.sin(radian), 15)

        x1 = coords[0] * radCos - coords[1] * radSin
        y1 = coords[0] * radSin - coords[1] * radCos
        return [int(x1), int(y1)]

    def rotateLeft(self):
        if self.pieceShape == Tetrominoe.SquareShape.value:
            return self
        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            coord = self.rotateAlpha(90, self.coords[i])
            result.setX(i, coord[0])
            result.setY(i, coord[1])
        return result

    def rotateRight(self):
        if self.pieceShape == Tetrominoe.SquareShape.value:
            return self
        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            coord = self.rotateAlpha(-90, self.coords[i])
            result.setX(i, coord[0])
            result.setY(i, coord[1])
        return result
