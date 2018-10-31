# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHeaderView, QAbstractItemView, QVBoxLayout, QTableView, QHBoxLayout, QLineEdit
from utils import HttpReq
from model import GameTableModel, Game, GameSortProxyModel


class SelectGameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.httpReq = HttpReq()
        self.setWindowTitle('选择游戏')
        self.resize(540, 300)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        self.iniUI()
        self.reqData()

    def iniUI(self):
        mLayout = QVBoxLayout()
        self.setLayout(mLayout)

        filterLayout = QHBoxLayout()
        filterLayout.addStretch()
        filterEdit = QLineEdit(self)
        filterEdit.setObjectName('filterEdit')
        filterEdit.setFixedWidth(160)
        filterEdit.setPlaceholderText('输入 id/名称/类型 过滤')
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
        self.tableWidget = tableWidget
        mLayout.addWidget(tableWidget)

    def reqData(self):
        reqParam = {
            'gameParam': json.dumps({'sig': '534857b0288c69a01575460dfbe49bfa', 'sig_sitemid': 'ZGQqaHVhc29uZ2dhbWVoYWxs'}),
            'lmode': 3,
            'appid': 10,
            'demo': 1
        }
        self.httpReq.get('http://192.168.1.158/game/game/index.php', reqParam, self.reqSuccess, self.reqFail)

    def reqSuccess(self, result):
        allGameJson = result['data']['urls']['allGame']
        if allGameJson:
            self.httpReq.get(allGameJson, None, self.loadGameSuccess, self.loadGameFaile)

    def reqFail(self, error):
        print(error)

    def loadGameSuccess(self, result):
        gameModel = GameTableModel()
        gameModel.setDataList(result)

        gameProxyModel = GameSortProxyModel()
        gameProxyModel.setSourceModel(gameModel)
        self.tableWidget.setModel(gameProxyModel)

    def loadGameFaile(self, error):
        print(error)

    def onItemSelect(self, itemIndex):
        self._selectData = self.tableWidget.model().getRowData(itemIndex)
        self.accept()

    def onFilterEditChange(self, text):
        filterStr = text.strip()
        self.tableWidget.model().setFilterFixedString(filterStr)

    @property
    def selectGame(self):
        return Game(self._selectData)
