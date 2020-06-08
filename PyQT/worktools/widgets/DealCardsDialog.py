# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QDialog, QTableWidget, QHeaderView, QAbstractItemView, QSizePolicy,
                             QVBoxLayout, QWidget, QHBoxLayout, QStatusBar, QPushButton, QTableWidgetItem)
from model import Card, CardType, DeckType
from widgets import ViewGenerator
from PyQt5.QtCore import Qt, QItemSelectionModel, QPropertyAnimation
import copy

LINE_HEIGHT = 70


# 分牌弹窗
class DealCardsDialog(QDialog):
    def __init__(self, index, gameModel, deckType, parent):
        super().__init__(parent)

        # model
        self._gameModel = gameModel
        self._deckType = deckType
        # 布局不同
        if deckType == DeckType.Hand:
            self._playerModel = gameModel.players[index]
            self._handListModel = copy.deepcopy(self._playerModel.handCardList)
            self._deployedListModel = copy.deepcopy(self._playerModel.deployedCardList)

            self.resize(self._gameModel.config['cardMaxNum'] * Card.WIDTH + 86, 450)
            self.setWindowTitle('分牌-->[玩家%s]' % self._playerModel.seatId)
        elif deckType == DeckType.PerDeploy:
            self._deployedListModel = copy.deepcopy(self._gameModel.deployedCardList)

            self.resize(660, 630)
            self.setWindowTitle('分牌-->预分配牌')

        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.iniUI()

    def showEvent(self, event):
        pass

    @property
    def handListModel(self):
        return self._handListModel

    @property
    def deployedListModel(self):
        return self._deployedListModel

    def iniUI(self):
        mLayout = QVBoxLayout()
        self.setLayout(mLayout)

        self.mLayout = mLayout
        self.initDeck()
        self.initPlayerCardsDeck()

        # 确认按钮
        btnGroup = QHBoxLayout()
        self.mLayout.addLayout(btnGroup)
        btnGroup.addStretch()
        confirmBtn = QPushButton('确认', self)
        confirmBtn.clicked.connect(self.onConfirmClick)
        btnGroup.addWidget(confirmBtn)
        self.confirmBtn = confirmBtn

        self.statusbar = QStatusBar()
        self.mLayout.addWidget(self.statusbar)
        self.statusbar.setSizeGripEnabled(False)

    # 初始化 手牌和预分配牌 牌组
    def initPlayerCardsDeck(self):
        # 表格布局
        tableWidget = QTableWidget()
        tableWidget.setColumnCount(1)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.setParent(self)
        tableWidget.setObjectName('playerTable')
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.verticalHeader().setStretchLastSection(True)
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.mLayout.addWidget(tableWidget)
        self._playerTableWidget = tableWidget

        if self._deckType == DeckType.Hand:
            self.addHandDeck()
        elif self._deckType == DeckType.PerDeploy:
            self.addPerDeployDeck()

        modelIndex = self._playerTableWidget.model().index(0, 0)
        self._playerTableWidget.selectionModel().select(modelIndex, QItemSelectionModel.Select)

    def addHandDeck(self):
        curRow = self._playerTableWidget.rowCount()
        self._playerTableWidget.insertRow(curRow)
        self._playerTableWidget.setVerticalHeaderItem(curRow, QTableWidgetItem(DeckType.Hand.label))
        self._playerTableWidget.setRowHeight(curRow, LINE_HEIGHT)
        handView = ViewGenerator.createModelDeckView(self._handListModel)
        handView.deckType = DeckType.Hand
        handView.dropDownSign.connect(self.dropInDeckView)
        handView.row = curRow
        handView.initCards(self._handListModel, self.onCardClick)
        self._playerTableWidget.setCellWidget(curRow, 0, handView)
        self.updateHeaderTextCount(handView)

    def addPerDeployDeck(self):
        curRow = self._playerTableWidget.rowCount()
        self._playerTableWidget.insertRow(curRow)
        self._playerTableWidget.setVerticalHeaderItem(curRow, QTableWidgetItem(DeckType.Hand.label))
        deployedView = ViewGenerator.createModelDeckView(self._deployedListModel)
        deployedView.deckType = DeckType.PerDeploy
        deployedView.dropDownSign.connect(self.dropInDeckView)
        deployedView.row = curRow
        deployedView.initCards(self._deployedListModel, self.onCardClick, maxWidth=self.size().width() - 60)
        self._playerTableWidget.setCellWidget(curRow, 0, deployedView)
        self.updateHeaderTextCount(deployedView)

    # 初始化牌组
    def initDeck(self):
        tableWidget = QTableWidget()
        tableWidget.setColumnCount(1)
        tableWidget.horizontalHeader().setVisible(False)
        tableWidget.setParent(self)
        tableWidget.setObjectName('deckTable')
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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
                cardView = ViewGenerator.createCardView(cardModel)
                cardView.mousePressSign.connect(self.onAddCardClick)
                lineLayout.addWidget(cardView)
            lineLayout.addStretch()

    def dropInDeckView(self, deckView, event):
        cardView = event.source()
        cardModel = cardView.model
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
            # 从牌堆中拖出的height牌
            self.addCardToDeckView(cardModel, deckView)

    def addCardToDeckView(self, cardModel, deckView):
        if deckView.deckType == DeckType.Hand:
            cardViewListModel = deckView.model
            if len(cardViewListModel.lists) >= self._gameModel.config['cardMaxNum']:
                self.statusbar.showMessage('已到达最大牌数[%d张]' % self._gameModel.config['cardMaxNum'], 2000)
                return
            handCardView = ViewGenerator.createCardView(Card(cardModel.value, CardType.HandCard))
        elif deckView.deckType == DeckType.PerDeploy:
            handCardView = ViewGenerator.createCardView(Card(cardModel.value, CardType.DealCard))
        handCardView.mousePressSign.connect(self.onCardClick)
        deckView.addCard(handCardView)
        self.updateHeaderTextCount(deckView)

    def updateHeaderTextCount(self, deckView):
        # 更新牌数提示
        count = len(deckView.model.lists)
        text = '%s\n[%d]' % (deckView.deckType.label, count)
        if count == 0:
            text = deckView.deckType.label
        self._playerTableWidget.verticalHeaderItem(deckView.row).setText(text)

    # 动画效果修改窗体大小
    def changeSize(self, size):
        self.animation = QPropertyAnimation(self, b'geometry')
        currentGeometry = self.geometry()
        currentGeometry.setSize(size)

        self.animation.setDuration(200)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(currentGeometry)
        self.animation.start()

    def onCardClick(self, cardView, event):
        if event.buttons() == Qt.RightButton:
            # remove card
            deckView = cardView.deckView
            if deckView:
                deckView.removeCard(cardView)
                self.updateHeaderTextCount(deckView)

    def onAddCardClick(self, cardView, event):
        if event.buttons() == Qt.RightButton:
            # add card
            # 只能单选
            if len(self._playerTableWidget.selectedIndexes()) > 0:
                modelIndex = self._playerTableWidget.selectedIndexes()[0]
                deckView = self._playerTableWidget.cellWidget(modelIndex.row(), modelIndex.column())
                self.addCardToDeckView(cardView.model, deckView)

    def onConfirmClick(self):
        # 改变赋值
        if self._deckType == DeckType.Hand:
            if self._playerModel.handCardList == self._handListModel and \
                    self._playerModel.deployedCardList == self._deployedListModel:
                self.reject()
            else:
                self._playerModel.handCardList = self._handListModel
                self._playerModel.deployedCardList = self._deployedListModel
                # self._gameModel.updateDeployedCardListByPlayer()
                self.accept()
        elif self._deckType == DeckType.PerDeploy:
            if self._gameModel.deployedCardList == self._deployedListModel:
                self.reject()
            else:
                self._gameModel.deployedCardList = self._deployedListModel
                # self._gameModel.updatePlayerDeployedCardListByList()
                self.accept()
