# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QDialog, QTableWidget, QHeaderView, QAbstractItemView,
                             QVBoxLayout, QWidget, QHBoxLayout)
from model import Card, CardType
from PyQt5.QtCore import Qt

LINE_HEIGHT = 80


# 分牌弹窗
class DealCardsDialog(QDialog):
    def __init__(self, index, gameModel):
        super().__init__()

        self._playerModel = gameModel.players[index]
        print(self._playerModel)
        self._gameModel = gameModel
        self.resize(560, 700)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle('分牌  [玩家%s]' % self._playerModel.seatId)
        self.iniUI()

    def iniUI(self):
        mLayout = QVBoxLayout()
        self.setLayout(mLayout)

        self.mLayout = mLayout
        self.initDeck()
        self.initPlayerCardsDeck()
        # self.mLayout.addStretch()

    # 初始化 手牌和预分配牌 牌组
    def initPlayerCardsDeck(self):
        tableWidget = QTableWidget(2, 1, self)
        # tableWidget.setColumnCount(1)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.setObjectName('playerTable')
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.setSelectionMode(QAbstractItemView.NoSelection)  # 不能选择
        self.mLayout.addWidget(tableWidget)
        tableWidget.setVerticalHeaderLabels(['手牌', '预发牌'])
        tableWidget.setRowHeight(0, LINE_HEIGHT)
        tableWidget.setRowHeight(1, LINE_HEIGHT * 2)

        handView = self._playerModel.createHandView()
        deployedView = self._playerModel.createDeployedView()
        handView.dropDownSign.connect(self.dropInDeckView)
        deployedView.dropDownSign.connect(self.dropInDeckView)
        tableWidget.setCellWidget(0, 0, handView)
        tableWidget.setCellWidget(1, 0, deployedView)

    # 初始化牌组
    def initDeck(self):
        tableWidget = QTableWidget()
        tableWidget.setColumnCount(1)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.setParent(self)
        tableWidget.setObjectName('deckTable')
        # tableWidget.horizontalHeader().setStretchLastSection(True)  # 列头自适应宽度
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.setSelectionMode(QAbstractItemView.NoSelection)  # 不能选择
        self.mLayout.addWidget(tableWidget)

        # 初始化牌数据
        labels = []
        cards = []
        for item in self._gameModel.config['cards']:
            labels.append(item['label'])
            cards.append(item['content'])
        tableWidget.setRowCount(len(labels))
        tableWidget.setFixedHeight((LINE_HEIGHT + 1) * len(labels))
        tableWidget.setVerticalHeaderLabels(labels)
        for i, line in enumerate(cards):
            cardWidget = QWidget()
            lineLayout = QHBoxLayout()
            cardWidget.setLayout(lineLayout)
            lineLayout.setSpacing(10)
            tableWidget.setRowHeight(i, LINE_HEIGHT)
            tableWidget.setCellWidget(i, 0, cardWidget)

            for index, cardValue in enumerate(line):
                cardModel = Card(cardValue, CardType.InitCard)
                lineLayout.addWidget(cardModel.createView())
            lineLayout.addStretch()

    def dropInDeckView(self, deckView, event):
        cardView = event.source()
        cardModel = cardView.model
        cardViewListModel = deckView.model
        if cardModel.type == CardType.HandCard:
            # 调整手牌中牌的位置
            if cardView.deckView != deckView:
                return
            # 插入到拖到牌的位置
            cardSize = cardView.size()
            for cv in deckView.cardViews:
                if cv != cardView:
                    crossPos = cv.pos() - event.pos()
                    if cardSize.width() > abs(crossPos.x()) and cardSize.height() > abs(crossPos.y()):
                        deckView.insertCard(cardView, cv)
                        break
        elif cardModel.type == CardType.InitCard:
            if len(cardViewListModel.lists) >= 14:
                # self.statusbar.showMessage('已到达最大牌数')
                return
            # 从牌堆中拖出的牌
            handCardView = Card(cardModel.value, CardType.HandCard).createView()
            handCardView.mousePressSign.connect(self.cardClick)
            deckView.addCard(handCardView)

    def cardClick(self, cardView, event):
        if event.buttons() == Qt.RightButton:
            playerView = cardView.deckView
            if playerView:
                playerView.removeCard(cardView)
