# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import (QDialog, QHeaderView, QAbstractItemView,
                             QVBoxLayout, QTableView, QHBoxLayout, QLineEdit, QComboBox)
from core import HttpReq, Logger
from model import GameTableModel, Game, GameSortProxyModel, GameConfigTableModel, GameConfigSortProxyModel, ButtonDeletage
from logic import DeployCardLogic

log = Logger(__name__).get_log()


class SelectConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        WIDTH, HEIGHT = 540, 300
        self._logic = DeployCardLogic()
        self.setWindowTitle('选择配置')
        self.resize(WIDTH, HEIGHT)
        self.setWindowFlags(Qt.Window)

        self.iniUI()

    def iniUI(self):
        mLayout = QVBoxLayout()
        self.setLayout(mLayout)

        filterLayout = QHBoxLayout()

        filterLayout.addStretch()
        filterEdit = QLineEdit(self)
        filterEdit.setObjectName('filterEdit')
        filterEdit.setFixedWidth(160)
        filterEdit.setPlaceholderText('输入 id/名称 过滤')
        filterEdit.textChanged.connect(self.onFilterEditChange)
        filterLayout.addWidget(filterEdit)
        mLayout.addLayout(filterLayout)

        tableWidget = QTableView()
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 默认选择一行
        tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidget.setSortingEnabled(True)
        tableWidget.doubleClicked.connect(self.onItemSelect)
        # tableWidget.setItemDelegateForColumn(2, ButtonDeletage(tableWidget))
        self.tableWidget = tableWidget
        mLayout.addWidget(tableWidget)

        self.loadData(self._logic.getConfigList())

    def loadData(self, data):
        gameModel = GameConfigTableModel()
        gameModel.setDataList(data)

        gameProxyModel = GameConfigSortProxyModel()
        gameProxyModel.setSourceModel(gameModel)
        self.tableWidget.setModel(gameProxyModel)
        # for row in range(0, gameProxyModel.rowCount()):
        #     self.tableWidget.openPersistentEditor(gameProxyModel.index(row, 2))

    def onFilterEditChange(self, text):
        filterStr = text.strip()
        self.tableWidget.model().setFilterFixedString(filterStr)

    def onItemSelect(self, itemIndex):
        self._selectData = self.tableWidget.model().getRowData(itemIndex)
        self.accept()

    @property
    def SelectData(self):
        return self._selectData
