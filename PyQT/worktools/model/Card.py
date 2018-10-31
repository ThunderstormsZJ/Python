# -*- coding: utf-8 -*-
from enum import Enum
from PyQt5.QtGui import QPixmap


class CardType(Enum):
    InitCard = 0
    HandCard = 1
    DealCard = 2


class Card(object):
    def __init__(self, value, cardType):
        self._width = 82
        self._height = 121
        self._value = int(value, 16) if isinstance(value, str) else value
        self._type = cardType

    def __str__(self):
        return '{Card [value=%s]}' % self.value

    @property
    def width(self):
        return self._width / 2

    @property
    def height(self):
        return self._height / 2

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def hexValue(self):
        return hex(self._value)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, cardType):
        self._type = cardType

    @property
    def pathName(self):
        suit = self._value >> 4
        face = self._value & 0x0F
        return "b%d_%d.png" % (suit, face)

    def createView(self):
        from widgets import CardLabel
        cardView = CardLabel()
        cardView.setFixedSize(self.width, self.height)
        cardImg = QPixmap('res/card/MJ/' + self.pathName)
        cardView.model = self
        cardView.setPixmap(cardImg)
        cardView.setScaledContents(True)
        return cardView


# 牌列表
class CardList(object):
    def __init__(self):
        self._cardList = []

    @property
    def lists(self):
        return self._cardList

    def addChard(self, card):
        self._cardList.append(card)

    def removeCard(self, card):
        self._cardList.remove(card)

    def insertCard(self, insertIndex, card):
        self.removeCard(card)
        self._cardList.insert(insertIndex, card)
