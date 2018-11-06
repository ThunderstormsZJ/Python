# -*- coding: utf-8 -*-
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

    def __str__(self):
        return "{Player [seatId=%s]}" % self._seatId
