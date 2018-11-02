# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QSizePolicy
from model import CardList


class Player(object):
    def __init__(self, seatId):
        self._handCardList = CardList()  # 手牌
        self._deployedCardList = CardList()  # 被分发牌
        self._seatId = seatId

    @property
    def seatId(self):
        return self._seatId

    @property
    def handCardList(self):
        return self._handCardList

    @handCardList.setter
    def handCardList(self, v):
        self._handCardList = v

    @property
    def deployedCardList(self):
        return self._deployedCardList

    @deployedCardList.setter
    def deployedCardList(self, v):
        self._deployedCardList = v

    def createView(self):
        # 固定视图
        from widgets import DeckWidget
        deckWidget = DeckWidget(False)
        deckWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return deckWidget

    def createModelView(self, model):
        # model 绑定视图
        # 可以管理model数据
        from widgets import DeckWidget
        deckWidget = DeckWidget(True)
        deckWidget.model = model
        deckWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return deckWidget

    def __str__(self):
        return "{Player [seatId=%s]}" % self._seatId
