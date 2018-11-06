#!/usr/bin/python3
# -*- coding: utf-8 -*-
import codecs
import json
import os
import sys

from PyQt5.QtCore import QSize, QPropertyAnimation
from PyQt5.QtGui import QFont

if getattr(sys, 'frozen', False):
    # frozen
    dir_ = os.path.dirname(sys.executable)
else:
    # unfrozen
    dir_ = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget,
                             QAbstractItemView, QHeaderView, QPushButton, QLabel, QDialog)
from model import Player, DeckType
from widgets import SelectGameDialog, DealCardsDialog, ViewGenerator

ConfigFileJson = 'res/config/card.json'


class DeployCard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.statusbar = self.statusBar()

        self.playerViewList = []
        self.config = self.readConfig()
        self.initUI()

    def readConfig(self):
        try:
            with codecs.open(ConfigFileJson, 'r', 'utf-8') as f:
                return json.loads(f.read())
        except Exception as e:
            # 配置文件加载失败
            print(e)

    def initUI(self):
        self.setWindowTitle('配牌工具')
        self.resize(735, 500)

        mWidget = QWidget()
        self.setCentralWidget(mWidget)
        mLayout = QVBoxLayout()
        mLayout.setSpacing(5)
        mWidget.setLayout(mLayout)

        self.mLayout = mLayout
        self.initTopWidget()
        self.initPlayerTable()

    def initTopWidget(self):
        btnGroup = QHBoxLayout()
        gameLabel = QLabel('', self)
        gameLabel.setObjectName('gameLabel')
        gameLabel.setFont(QFont('宋体', 12, QFont.Bold))
        btnGroup.addWidget(gameLabel)

        btnGroup.addStretch()

        selectBtn = QPushButton('选择游戏', self)
        selectBtn.clicked.connect(self.onSelectGameClick)
        btnGroup.addWidget(selectBtn)

        uploadBtn = QPushButton('上传配牌', self)
        uploadBtn.setObjectName('uploadBtn')
        uploadBtn.setEnabled(False)
        uploadBtn.clicked.connect(self.onUploadClick)
        btnGroup.addWidget(uploadBtn)

        self.mLayout.addLayout(btnGroup)

    def initPlayerTable(self):
        tableWidget = QTableWidget()
        tableWidget.setColumnCount(1)
        tableWidget.setHorizontalHeaderLabels(['手牌'])
        tableWidget.setParent(self)
        tableWidget.setObjectName('playerTable')
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.verticalHeader().setStretchLastSection(True)  # 最后一行自动扩展
        tableWidget.setSelectionMode(QAbstractItemView.NoSelection)  # 不能选择
        tableWidget.clicked.connect(self.onEidtPlayer)
        self.mLayout.addWidget(tableWidget)

    def setCurrGame(self, game):
        print('CurrentGame', game)
        uploadBtn = self.findChild(QPushButton, 'uploadBtn')
        uploadBtn.setEnabled(True)

        LINE_HEIGHT = 80
        config = self.config.get(game.type.name, None)
        gameLabel = self.findChild(QLabel, 'gameLabel')
        playerTable = self.findChild(QTableWidget, 'playerTable')
        self.changeSize(QSize(self.width(), LINE_HEIGHT * (len(config["cards"]) + config['player'])))
        # 赋值
        game.config = config
        self._currentGame = game
        # 设置当选全中的游戏 信息
        gameLabel.setText('当前游戏: %s ID: %s' % (game.name, game.id))

        # 初始化玩家视图
        labels = ['玩家' + str(i) for i in range(config['player'])] + ['预发牌']
        playerTable.setRowCount(len(labels))
        playerTable.setVerticalHeaderLabels(labels)
        self.playerViewList = []
        for i in range(config['player']):
            player = Player(i)
            self._currentGame.addPlayer(player)
            playerView = ViewGenerator.createDefaultDeckView()
            playerView.setLabelText('点击编辑')
            playerView.deckType = DeckType.Hand
            self.playerViewList.append(playerView)
            playerTable.setRowHeight(i, LINE_HEIGHT)
            playerTable.setCellWidget(i, 0, playerView)

        # 初始化发牌组视图
        perDeployCardDeck = ViewGenerator.createDefaultDeckView()
        perDeployCardDeck.setObjectName('perDeployCardDeck')
        perDeployCardDeck.setLabelText('点击编辑')
        perDeployCardDeck.deckType = DeckType.PerDeploy
        playerTable.setCellWidget(len(self.playerViewList), 0, perDeployCardDeck)
        self.perDeployCardDeck = perDeployCardDeck

    def onEidtPlayer(self, itemIndex):
        # deck 的 类型不同 响应不同的逻辑
        print("SelectIndex:[col]=%s [row]=%s" % (itemIndex.column(), itemIndex.row()))
        playerTable = self.findChild(QTableWidget, 'playerTable')
        deckWidget = playerTable.cellWidget(itemIndex.row(), itemIndex.column())
        dialog = DealCardsDialog(itemIndex.row(), self._currentGame, deckWidget.deckType)
        if dialog.exec_() == QDialog.Accepted:
            if deckWidget.deckType == DeckType.Hand:
                # 更新手牌
                deckWidget.initCards(dialog.handListModel)
                # 更新预分配牌界面
                self.perDeployCardDeck.initCards(self._currentGame.deployedCardList)
            elif deckWidget.deckType == DeckType.PerDeploy:
                # 更新预分配牌界面
                deckWidget.initCards(dialog.deployedListModel)

    def onSelectGameClick(self):
        dialog = SelectGameDialog()
        # exec()函数的真正含义是开启一个新的事件循环 可以理解成一个无限循环
        if dialog.exec_() == QDialog.Accepted:
            game = dialog.selectGame
            config = self.config.get(game.type.name, None)
            if not config:
                self.statusbar.showMessage('[%s]游戏配置不存在' % game.type.name, 2000)
                return
            self.setCurrGame(game)

    def onUploadClick(self):
        pass

    # 动画效果修改窗体大小
    def changeSize(self, size):
        self.animation = QPropertyAnimation(self, b'geometry')
        currentGeometry = self.geometry()
        currentGeometry.setSize(size)

        self.animation.setDuration(200)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(currentGeometry)
        self.animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DeployCard()
    ex.show()
    sys.exit(app.exec_())
