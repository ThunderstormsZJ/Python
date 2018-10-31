# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QSortFilterProxyModel
from enum import Enum


class GameType(Enum):
    ZIPAI = 1
    POKER = 2
    MJ = 3


class Game(object):
    def __init__(self, data):
        self._id = 0
        self._name = ""
        self._title = ""
        self._type = None
        self._config = None
        self._playerList = []

        self.parseData(data)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._type

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def addPlayer(self, player):
        self._playerList.append(player)

    @property
    def players(self):
        return self._playerList

    def __str__(self):
        return '{Game [ID:%s Name:%s Title:%s]}' % (self.id, self.name, self.title)

    def parseData(self, data):
        self._id = data['game_id']
        self._name = data['game_name']
        self._title = data['game_type_title']
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
