# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import (QDialog, QHeaderView, QAbstractItemView,
                             QVBoxLayout, QTableView, QHBoxLayout, QLineEdit, QComboBox)
from core import HttpReq, Logger
from model import GameTableModel, Game, GameSortProxyModel
from logic import Controller

log = Logger(__name__).get_log()


class SelectGameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.httpReq = HttpReq()
        self.setWindowTitle('选择游戏')
        self.resize(540, 300)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        self.iniUI()
        self.setPlatform(Controller().currentPlatform)

    def iniUI(self):
        mLayout = QVBoxLayout()
        self.setLayout(mLayout)

        filterLayout = QHBoxLayout()

        # 平台选择
        platformBox = QComboBox()
        platformBox.setObjectName('platformBox')
        platformBox.addItem('请选择')
        for platform in Controller().platformList:
            platformBox.addItem(platform.name, QVariant(platform.id))
        platformBox.activated[int].connect(self.onPlatformSelect)
        filterLayout.addWidget(platformBox)

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

    def reqData(self, platform):
        reqParam = {
            'gameParam': json.dumps({'sig': '534857b0288c69a01575460dfbe49bfa', 'sig_sitemid': 'ZGQqaHVhc29uZ2dhbWVoYWxs'}),
            'lmode': 3,
            'appid': platform.appid,
            'demo': 1,
            'version': platform.version
        }
        self.httpReq.get(platform.url, reqParam, self.reqSuccess, self.reqFail)

    def reqSuccess(self, result):
        allGameJson = result['data']['urls']['allGame']
        if allGameJson:
            self.httpReq.get(allGameJson, None, self.loadGameSuccess, self.loadGameFaile)

    def reqFail(self, error):
        log.error(error)

    def loadGameSuccess(self, result):
        gameModel = GameTableModel()
        gameModel.setDataList(result)

        gameProxyModel = GameSortProxyModel()
        gameProxyModel.setSourceModel(gameModel)
        self.tableWidget.setModel(gameProxyModel)

    def loadGameFaile(self, error):
        log.error(error)

    def onItemSelect(self, itemIndex):
        self._selectData = self.tableWidget.model().getRowData(itemIndex)
        self.accept()

    def onFilterEditChange(self, text):
        filterStr = text.strip()
        self.tableWidget.model().setFilterFixedString(filterStr)

    def onPlatformSelect(self, index):
        platformBox = self.findChild(QComboBox, 'platformBox')
        idData = platformBox.itemData(index)
        if idData:
            platform = Controller().getPlatformById(idData)
            if Controller().currentPlatform != platform:
                self.setPlatform(platform)
        else:
            self.clearTableContents()

    # 设置当前平台
    def setPlatform(self, platform):
        if platform:
            # 设置默认选中
            platformBox = self.findChild(QComboBox, 'platformBox')
            platformBox.setCurrentIndex(platformBox.findData(platform.id))
            self.clearTableContents()
            self.reqData(platform)
            Controller().currentPlatform = platform

    def clearTableContents(self):
        tableModel = self.tableWidget.model()
        if tableModel:
            tableModel.deleteLater()

    @property
    def selectGame(self):
        return Game(self._selectData)
