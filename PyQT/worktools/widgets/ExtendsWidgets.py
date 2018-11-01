# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QFont, QDrag
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QHBoxLayout, QStackedWidget
from model import Card
import math


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
class DeckWidget(QStackedWidget):
    dropDownSign = pyqtSignal(object, object)

    def __init__(self, isDrops):
        super().__init__()
        self._model = None
        self.tipLabel = None
        self._isDefaultLayout = None

        self.setAcceptDrops(isDrops)
        # 构造两个widget
        cardWidget = QWidget()
        defaultWidget = QWidget()

        self.cardLayout = QGridLayout()
        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.defaultLayout = QHBoxLayout()
        self.defaultLayout.setAlignment(Qt.AlignCenter)

        defaultWidget.setLayout(self.defaultLayout)
        cardWidget.setLayout(self.cardLayout)
        self.addWidget(defaultWidget)
        self.addWidget(cardWidget)

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

    @property
    def cardCount(self):
        return self.cardLayout.count()

    def initUI(self):
        label = QLabel('拖到此处')
        label.setFont(QFont('Roman times', 20, QFont.Bold))
        label.setParent(self)
        label.setStyleSheet('QLabel{color:rgb(204,204,204)}')
        self.tipLabel = label
        self.defaultLayout.addWidget(label)
        self.showDefaultLayout(True)

    def initCards(self, model):
        # 移除已有牌
        while self.cardLayout.itemAt(0) and isinstance(self.cardLayout.itemAt(0).widget(), CardLabel):
            self.cardLayout.removeItem(self.cardLayout.itemAt(0))

        for card in model.lists:
            cardView = card.createView()
            cardView.deckView = self
            self.cardLayout.addWidget(cardView)
            self.showDefaultLayout(False)

    def setLabelText(self, text):
        self.tipLabel.setText(text)

    # 根据index获取相应的 行号和列号
    def getColAndRow(self, index=None):
        # 根据宽度自动变换行数
        col, row = 0, 0
        count = self.cardCount if (index is None) else index
        colMaxCount = math.ceil(self.size().width() / Card.WIDTH) - 1
        col = count % colMaxCount
        row = math.floor(count / colMaxCount)
        return col, row

    def addCard(self, cardView):
        cardView.deckView = self

        col, row = self.getColAndRow()
        self.cardLayout.addWidget(cardView, row, col)

        if self._model:
            self._model.addChard(cardView.model)
        self.showDefaultLayout(False)

    def removeCard(self, cardView):
        removeIndex = self.cardLayout.indexOf(cardView)
        # 后面的元素往前移
        self.moveCard(removeIndex+1, self.cardCount-1, -1)

        if self._model:
            self._model.removeCard(cardView.model)
        cardView.setParent(None)
        del cardView
        if self.cardLayout.count() == 0:
            self.showDefaultLayout(True)

    # cardView : 需要插入的牌
    # insertedView : 被插入的位置的牌
    def insertCard(self, cardView, insertedView):
        insertIndex = self.cardLayout.indexOf(insertedView)

        if insertIndex > 0:
            pos = self.cardLayout.getItemPosition(insertIndex)
            self.cardLayout.removeWidget(cardView)
            self.cardLayout.addWidget(cardView, pos[0], pos[1])
            if self._model:
                self._model.insertCard(insertIndex - 1, cardView.model)

    """
       移动牌
        @start 牌开始的索引
        @end   牌结束的索引
        @distance 移动的距离
    """
    def moveCard(self, start, end, distance):
        movedItem = []  # 需要移动的item
        for i in range(start, end + 1):
            item = self.cardLayout.itemAt(i)
            if item:
                movedItem.append(item)

        for item in movedItem:
            self.cardLayout.removeItem(item)

        # 重新加入到布局之中
        newStart = start + distance
        for item in movedItem:
            col, row = self.getColAndRow(newStart)
            self.cardLayout.addWidget(item.widget(), row, col)
            newStart += 1

    def getCardValueList(self):
        cardValueList = []
        # TODO
        return cardValueList

    def showDefaultLayout(self, isShow):
        if self._isDefaultLayout == isShow:
            return
        self._isDefaultLayout = isShow
        if isShow:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(1)

    def dragEnterEvent(self, e):
        if isinstance(e.source(), CardLabel):
            e.accept()

    def dropEvent(self, e):
        # 将牌添加到 列表中
        self.dropDownSign.emit(self, e)
        e.setDropAction(Qt.MoveAction)
        e.accept()
