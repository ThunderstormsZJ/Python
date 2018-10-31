#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication

from tetris.Board import Board


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.tBoard = Board(self)
        self.setCentralWidget(self.tBoard)
        self.tBoard.start()

        self.statusbar = self.statusBar()

        self.resize(200, 380)
        self.center()
        self.setWindowTitle('Tetris')

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tetris()
    ex.show()
    sys.exit(app.exec_())
