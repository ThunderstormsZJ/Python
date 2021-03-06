# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QSortFilterProxyModel
from .enum import GameType
from .Card import CardList, Card
import random
import copy


class Game(object):
    def __init__(self, data):
        self._id = 0
        self._name = ""
        self._title = ""
        self._pkgName = ""
        self._type = None
        self._config = None
        self._playerList = []
        self._deployedCardList = CardList()

        self.parseData(data)

    @property
    def Id(self):
        return self._id

    @property
    def Name(self):
        return self._name

    @property
    def Title(self):
        return self._title

    @property
    def Type(self):
        return self._type

    @property
    def Config(self):
        return self._config

    @Config.setter
    def Config(self, value):
        tValue = copy.deepcopy(value)
        # 合并独立游戏配置
        if tValue.get(self._pkgName):
            for key, item in tValue[self._pkgName].items():
                tValue[key] = item

        self._config = tValue

    @property
    def DeployedCardList(self):
        return self._deployedCardList

    @DeployedCardList.setter
    def DeployedCardList(self, v):
        self._deployedCardList = v

    def addPlayer(self, player):
        self._playerList.append(player)

    @property
    def Players(self):
        return self._playerList

    # 根据每个用户的预分配 更新总的预分配列表
    # 不使用
    # def updateDeployedCardListByPlayer(self):
    #     # 保证每个用户的牌数量一样，才可以发到对应的牌
    #     maxDCLPlayer = self.players[0]
    #     for player in self.players:
    #         if maxDCLPlayer.deployedCardList.len < player.deployedCardList.len:
    #             maxDCLPlayer = player
    #     if maxDCLPlayer.deployedCardList.len == 0:
    #         return
    #     for player in self.players:
    #         for i in range(player.deployedCardList.len, maxDCLPlayer.deployedCardList.len):
    #             player.deployedCardList.addCard(self.genRandomCardModel(CardType.DealCard))
    #     zipedList = zip(*[x.deployedCardList.lists for x in self.players])
    #     self.deployedCardList.lists = [model for x in list(zipedList) for model in x]

    # 根据总的分牌列表 更新每个用户的预分配牌
    # 不使用
    # def updatePlayerDeployedCardListByList(self):
    #     if self.deployedCardList.len == 0:
    #         return
    #     for player in self.players:
    #         player.deployedCardList.clear()
    #     loopIndex = 0
    #     for model in self.deployedCardList.lists:
    #         if loopIndex >= len(self.players):
    #             loopIndex = 0
    #         self.players[loopIndex].deployedCardList.addCard(model)
    #         loopIndex += 1

    # 生成一张随机的牌
    def genRandomCardModel(self, type):
        if not self._config:
            return None
        valueList = [v for x in self._config['cards'] for v in x['content']]
        randomValue = valueList[random.randint(0, len(valueList) - 1)]
        return Card(randomValue, type)

    def __str__(self):
        return '{Game [ID:%s Name:%s Title:%s]}' % (self._id, self._name, self._title)

    def parseData(self, data):
        self._id = data['game_id']
        self._name = data['game_name']
        self._title = data['game_type_title']
        self._pkgName = data['pkg_name']
        self._type = GameType(int(data['game_type']))


class GameTableModel(QAbstractTableModel):
    HheadLabels = ['ID', '名称', '类型']
    # game_id game_name game_type_title game_type
    HheadKey = ['game_id', 'game_name', 'game_type_title']

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role != Qt.DisplayRole:
            return QVariant()
        if Qt_Orientation == Qt.Horizontal:
            return self.HheadLabels[p_int]
        else:
            return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.dataList)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.HheadLabels)

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return QVariant()

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.DisplayRole:
            currentData = self.dataList[QModelIndex.row()][self.HheadKey[QModelIndex.column()]]
            return currentData

    def getRowData(self, QModelIndex):
        if not QModelIndex.isValid():
            return QVariant()

        return self.dataList[QModelIndex.row()]

    def setDataList(self, dataList):
        self.beginResetModel()
        self.dataList = dataList
        self.endResetModel()


class GameSortProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        #  If the value is -1, the keys will be read from all columns.
        self.setFilterKeyColumn(-1)

    def getRowData(self, itemIndex):
        sorceIndex = self.mapToSource(itemIndex)
        return self.sourceModel().getRowData(sorceIndex)

    # def lessThan(self, indexLeft, indexRight):
    #     return super().lessThan(indexLeft, indexRight)
