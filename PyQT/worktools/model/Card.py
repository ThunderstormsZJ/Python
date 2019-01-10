# -*- coding: utf-8 -*-
import operator


class Card(object):
    WIDTH = 82 / 2
    HIEGHT = 121 / 2

    def __init__(self, value, cardType):
        self._width = Card.WIDTH
        self._height = Card.HIEGHT
        self._value = int(value, 16) if isinstance(value, str) else value
        self._type = cardType

    def __str__(self):
        return '{Card [value=%s]}' % self.value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

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


# 牌列表
class CardList(object):
    def __init__(self):
        self._cardList = []

    @property
    def lists(self):
        return self._cardList

    @lists.setter
    def lists(self, v):
        self._cardList = v

    @property
    def len(self):
        return len(self._cardList)

    @property
    def valueList(self):
        return [model.value for model in self._cardList]

    def addCards(self, cards):
        self._cardList = self._cardList + cards

    def addCard(self, card):
        self._cardList.append(card)

    def removeCard(self, card):
        self._cardList.remove(card)

    def insertCard(self, insertIndex, card):
        self.removeCard(card)
        self._cardList.insert(insertIndex, card)

    def clear(self):
        self._cardList = []

    def __eq__(self, other):
        vList1 = [card.value for card in self.lists]
        vList2 = [card.value for card in other.lists]
        return operator.eq(vList1, vList2)

    def __reversed__(self):
        self._cardList = list(reversed(self._cardList))
        return self
