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

    @property
    def deployedCardList(self):
        return self._deployedCardList

    def createView(self):
        # 固定视图
        from widgets import DeckWidget
        deckWidget = DeckWidget(False)
        deckWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return deckWidget

    def createHandView(self):
        # 手牌视图
        from widgets import DeckWidget
        deckWidget = DeckWidget(True)
        deckWidget.model = self.handCardList
        deckWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return deckWidget

    def createDeployedView(self):
        # 分牌视图
        from widgets import DeckWidget
        deckWidget = DeckWidget(True)
        deckWidget.model = self.deployedCardList
        deckWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return deckWidget

    def __str__(self):
        return "{Player [seatId=%s]}" % self._seatId
