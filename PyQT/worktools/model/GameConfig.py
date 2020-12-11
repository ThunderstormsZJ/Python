# -*- coding: utf-8 -*-
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant, QSortFilterProxyModel
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
    # game_id game_name game_type_title game_type
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

class ButtonDeletage(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            button_read = QPushButton(
                self.tr('读'),
                self.parent(),
                # clicked=self.parent().cellButtonClicked
            )
            button_write = QPushButton(
                self.tr('写'),
                self.parent(),
                # clicked=self.parent().cellButtonClicked
            )
            button_read.index = [index.row(), index.column()]
            button_write.index = [index.row(), index.column()]
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(button_read)
            h_box_layout.addWidget(button_write)
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(
                index,
                widget
            )

    # def createEditor(self, parent, option, index):
    #     combo = QPushButton(str(index.data()), parent)

    #     #self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
    #     # combo.clicked.connect(self.currentIndexChanged)
    #     return combo
        
    # def setEditorData(self, editor, index):
    #     print(index, "setEditorData")
    #     editor.blockSignals(True)
    #     #editor.setCurrentIndex(int(index.model().data(index)))
    #     editor.blockSignals(False)
        
    # def setModelData(self, editor, model, index):
    #     print(index, "setModelData")
    #     model.setData(index, editor.text())
        
    # @QtCore.pyqtSlot()
    # def currentIndexChanged(self):
    #     self.commitData.emit(self.sender())
