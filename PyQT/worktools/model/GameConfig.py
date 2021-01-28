# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QSortFilterProxyModel, pyqtSignal, QModelIndex
from PyQt5.QtWidgets import QPushButton, QItemDelegate, QHBoxLayout, QWidget
import json

class GameConfig(object):
    def __init__(self):
        self._id = 0
        self._user = None
        self._game = None
        self._config = None
        self._platform = None
        self._name = ""

    @property
    def Config(self):
        return json.loads(self._config)

    @property
    def Name(self):
        return self._name

    @property
    def Id(self):
        return self._id

    @property
    def Game(self):
        return self._game
    
    @Game.setter
    def Game(self, v):
        self._game = v

    @property
    def User(self):
        return self._user

    @User.setter
    def User(self, v):
        self._user = v
    
    @property
    def Platform(self):
        return self._platform

    @Platform.setter
    def Platform(self, v):
        self._platform = v
    
    def parseQuery(self, query):
        self._id = query.value('id')
        self._config = query.value('config')
        self._name = query.value('name')

        return self

    def __str__(self):
        return "{GameConfig [name=%s]}" % self._name

class GameConfigTableModel(QAbstractTableModel):
    HheadLabels = ['ID', '名称', '操作']
    HheadKey = ['Id', 'Name']

    def headerData(self, p_int, Qt_Orientation, role=None):
        if role != Qt.DisplayRole:
            return QVariant()
        if Qt_Orientation == Qt.Horizontal:
            return self.HheadLabels[p_int]
        else:
            return QVariant()
    
    # def flags(self, index):
    #     print(index.column(), "flags")
    #     if (index.column() == 0):
    #         return Qt.ItemIsEditable | Qt.ItemIsEnabled
    #     else:
    #         return Qt.ItemIsEnabled

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.dataList)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.HheadLabels)

    def data(self, QModelIndex, role=None):
        if not QModelIndex.isValid():
            return QVariant()

        col = QModelIndex.column()
        row = QModelIndex.row()
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.DisplayRole:
            if col > len(self.HheadKey) - 1:
                return QVariant()
            else:
                key = self.HheadKey[col]
                pro = getattr(GameConfig, key)
                currentData = pro.fget(self.dataList[row])
                return currentData

    def getRowData(self, QModelIndex):
        if not QModelIndex.isValid():
            return QVariant()

        return self.dataList[QModelIndex.row()]

    def removeRow(self, qIndex):
        print("removeRow", qIndex.row())
        self.beginRemoveRows(qIndex.parent(), qIndex.row(), qIndex.row())
        del self.dataList[qIndex.row()]
        self.beginRemoveRows()
        return True

    def setDataList(self, dataList):
        self.beginResetModel()
        self.dataList = dataList
        self.endResetModel()


class GameConfigSortProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        #  If the value is -1, the keys will be read from all columns.
        self.setFilterKeyColumn(-1)

    def getRowData(self, itemIndex):
        sorceIndex = self.mapToSource(itemIndex)
        return self.sourceModel().getRowData(sorceIndex)

    def removeRow(self, itemIndex):
        sorceIndex = self.mapToSource(itemIndex)
        return self.sourceModel().removeRow(sorceIndex)

class ButtonDeletage(QItemDelegate):
    selectSignal = pyqtSignal(object)
    deleteSignal = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            selButton = QPushButton(
                self.tr('选择'),
                self.parent(),
            )
            delButton = QPushButton(
                self.tr('删除'),
                self.parent(),
            )
            delButton.index = index
            selButton.index = index
            delButton.setObjectName("delete")
            selButton.setObjectName("select")
            delButton.clicked.connect(self.onButtonClick)
            selButton.clicked.connect(self.onButtonClick)
            hBoxLayout = QHBoxLayout()
            hBoxLayout.addWidget(selButton)
            hBoxLayout.addWidget(delButton)
            hBoxLayout.setContentsMargins(0, 0, 0, 0)
            hBoxLayout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(hBoxLayout)
            self.parent().setIndexWidget(index, widget)

    def onButtonClick(self):
        sender = self.sender()
        print("onButtonClick", sender.objectName(), sender.index.row())
        if sender.objectName() == "delete":
            self.deleteSignal.emit(sender.index)
        elif sender.objectName() == "select":
            self.selectSignal.emit(sender.index)
