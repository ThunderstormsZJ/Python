# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QFont, QDrag
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout


# 单个牌视图
class CardLabel(QLabel):
    mousePressSign = pyqtSignal(object, object)

    def __init__(self, *__args):
        super().__init__(*__args)
        self._model = None
        self._deckView = None

    # 与model绑定
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    # 属于哪个牌组
    @property
    def deckView(self):
        return self._deckView

    @deckView.setter
    def deckView(self, view):
        self._deckView = view

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pixmap().scaled(self.size()))
        drag.setHotSpot(self.rect().center())  # 设置跟随的中心点
        drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        self.mousePressSign.emit(self, e)


# 牌组
class DeckWidget(QWidget):
    dropDownSign = pyqtSignal(object, object)

    def __init__(self, isDrops):
        super().__init__()
        self._model = None
        self.tipLabel = None

        self.setAcceptDrops(isDrops)
        self.cardLayout = QHBoxLayout()
        self.setLayout(self.cardLayout)
        self.cardLayout.setSpacing(0)

        self.initUI()

    # 与 model 绑定
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model
        # 初始化已有牌
        self.initCards(self._model)

    @property
    def cardViews(self):
        viewList = []
        for index in range(0, self.cardLayout.count()):
            viewList.append(self.cardLayout.itemAt(index).widget())
        return viewList

    def initUI(self):
        label = QLabel('拖到此处')
        label.setFont(QFont('Roman times', 20, QFont.Bold))
        label.setParent(self)
        label.setStyleSheet('QLabel{color:rgb(204,204,204)}')

        self.cardLayout.addWidget(label)
        self.cardLayout.setAlignment(Qt.AlignCenter)
        self.tipLabel = label

    def initCards(self, model):
        # 移除已有牌
        while self.cardLayout.itemAt(0) and isinstance(self.cardLayout.itemAt(0).widget(), CardLabel):
            self.cardLayout.removeItem(self.cardLayout.itemAt(0))

        for card in model.lists:
            cardView = card.createView()
            cardView.deckView = self
            self.cardLayout.addWidget(cardView)
            self.showTipLabel(False)

    def setLabelText(self, text):
        self.tipLabel.setText(text)

    def addCard(self, cardView):
        cardView.deckView = self
        self.cardLayout.addWidget(cardView)
        if self._model:
            self._model.addChard(cardView.model)
        if self.tipLabel.isVisible():
            self.showTipLabel(False)

    def removeCard(self, cardView):
        cardView.setParent(None)
        if self._model:
            self._model.removeCard(cardView.model)
        if self.cardLayout.count() == 1:
            self.showTipLabel(True)

    # cardView : 需要插入的牌
    # insertedView : 被插入的位置的牌
    def insertCard(self, cardView, insertedView):
        insertIndex = self.cardLayout.indexOf(insertedView)
        if insertIndex > 0:
            self.cardLayout.removeWidget(cardView)
            self.cardLayout.insertWidget(insertIndex, cardView)
            if self._model:
                self._model.insertCard(insertIndex - 1, cardView.model)

    def getCardValueList(self):
        cardValueList = []
        # if self._model:
        #     for cardView in self._model.cardList:
        #         cardValueList.append(cardView.model.hexValue)
        return cardValueList

    def showTipLabel(self, isShow):
        if isShow:
            self.cardLayout.setAlignment(Qt.AlignCenter)
        else:
            self.cardLayout.setAlignment(Qt.AlignLeft)
        self.tipLabel.setVisible(isShow)

    def dragEnterEvent(self, e):
        if isinstance(e.source(), CardLabel):
            e.accept()

    def dropEvent(self, e):
        # 将牌添加到 列表中
        self.dropDownSign.emit(self, e)
        e.setDropAction(Qt.MoveAction)
        e.accept()
