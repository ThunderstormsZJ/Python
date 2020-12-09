# -*- coding: utf-8 -*-
import codecs
import json
from PyQt5.QtCore import QSize, QPropertyAnimation, Qt
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QAction, QInputDialog, QMessageBox,
                             QAbstractItemView, QHeaderView, QPushButton, QDialog)
from model import Player, DeckType, Card
from widgets import SelectGameDialog, SelectConfigDialog, DealCardsDialog, ViewGenerator
from core import Logger
from logic import DeployCardLogic, DirPath
from ui import Ui_ToolWindow

log = Logger(__name__).get_log()
LINE_HEIGHT = 80

class DeployCard(QMainWindow, Ui_ToolWindow):
    def __init__(self):
        super().__init__()
        self._logic = DeployCardLogic()
        self._logic.init()

        self.playerViewList = []
        self.config = self.readConfig()
        self.setupUi(self)
        self.initUi()

    def readConfig(self):
        try:
            with codecs.open(DirPath.GameConfigFileJson, 'r', 'utf-8') as f:
                return json.loads(f.read())
        except Exception as e:
            # 配置文件加载失败
            log.error(e)

    def initUi(self):
        self.setWindowTitle('配牌工具[v%s]-[%s]' % (self._logic.getVersion(), self._logic.CurrentUser.Name))
        self.selectBtn.clicked.connect(self.onSelectGameClick)
        self.uploadBtn.clicked.connect(self.onUploadClick)
        self.clearBtn.clicked.connect(self.onClearClick)
        self.initMenu()
        self.initPlayerTable()

    def initMenu(self):
        operateMenu = self.menubar.addMenu("操作")
        saveAction = QAction("保存配牌", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("保存")
        loadAction = QAction("加载配牌", self)
        loadAction.setShortcut("Ctrl+R")
        loadAction.setStatusTip("加载")

        saveAction.triggered.connect(self.onSaveActionClick)
        loadAction.triggered.connect(self.onLoadActionClick)
        operateMenu.addAction(saveAction)
        operateMenu.addAction(loadAction)

    def initPlayerTable(self):
        tableWidget = self.playerTable
        tableWidget.setColumnCount(1)
        tableWidget.setHorizontalHeaderLabels(['手牌'])
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        tableWidget.verticalHeader().setStretchLastSection(True)  # 最后一行自动扩展
        tableWidget.setSelectionMode(QAbstractItemView.NoSelection)  # 不能选择
        tableWidget.clicked.connect(self.onEditPlayer)

    def getWindowSize(self, game):
        return QSize(game.Config['cardMaxNum'] * Card.WIDTH + 161, LINE_HEIGHT * (len(game.Config["cards"]) + game.Config['player']))

    def setCurrGame(self, game):
        log.info('Current Game %s' % game)
        uploadBtn = self.findChild(QPushButton, 'uploadBtn')
        uploadBtn.setEnabled(True)

        config = self.config.get(game.Type.name, None)
        playerTable = self.playerTable
        # 赋值
        game.Config = config

        self.changeSize(self.getWindowSize(game))

        for i in range(config['player']):
            player = Player(i)
            game.addPlayer(player)
        self._logic.initGameModel(game)
        # 设置当选全中的游戏 信息
        self.gameLabel.setText('当前游戏: %s ID: %s' % (game.Name, game.Id))

        # 初始化玩家视图
        labels = ['玩家' + str(i) for i in range(config['player'])] + ['预发牌']
        playerTable.setRowCount(len(labels))
        playerTable.setVerticalHeaderLabels(labels)
        self.playerViewList = []
        for i, player in enumerate(game.Players):
            playerView = ViewGenerator.createDefaultDeckView()
            playerView.setLabelText('点击编辑')
            playerView.deckType = DeckType.Hand
            self.playerViewList.append(playerView)
            playerTable.setRowHeight(i, LINE_HEIGHT)
            playerTable.setCellWidget(i, 0, playerView)

        # 初始化发牌组视图
        perDeployCardDeck = ViewGenerator.createDefaultDeckView()
        perDeployCardDeck.setObjectName('perDeployCardDeck')
        perDeployCardDeck.setLabelText('点击编辑')
        perDeployCardDeck.deckType = DeckType.PerDeploy
        playerTable.setCellWidget(len(self.playerViewList), 0, perDeployCardDeck)
        self.perDeployCardDeck = perDeployCardDeck

        # 更新视图
        self.updateView(game)

    def updateView(self, game):
        maxWidth = self.getWindowSize(game).width()
        self.perDeployCardDeck.initCards(reversed(game.DeployedCardList), None, maxWidth)
        for i, player in enumerate(game.Players):
            self.playerViewList[i].initCards(player.handCardList, None, maxWidth)

    def onEditPlayer(self, itemIndex):
        # deck 的 类型不同 响应不同的逻辑
        # print("SelectIndex:[col]=%s [row]=%s" % (itemIndex.column(), itemIndex.row()))
        playerTable = self.findChild(QTableWidget, 'playerTable')
        deckWidget = playerTable.cellWidget(itemIndex.row(), itemIndex.column())
        dialog = DealCardsDialog(itemIndex.row(), self._logic.CurrentGame, deckWidget.deckType, self)
        if dialog.exec_() == QDialog.Accepted:
            if deckWidget.deckType == DeckType.Hand:
                # 更新手牌
                deckWidget.initCards(dialog.handListModel)
                # 更新预分配牌界面
                self.perDeployCardDeck.initCards(self._logic.CurrentGame.DeployedCardList)
            elif deckWidget.deckType == DeckType.PerDeploy:
                # 更新预分配牌界面
                deckWidget.initCards(dialog.deployedListModel)

    def onSelectGameClick(self):
        dialog = SelectGameDialog(self)
        # exec()函数的真正含义是开启一个新的事件循环 可以理解成一个无限循环
        if dialog.exec_() == QDialog.Accepted:
            game = dialog.selectGame
            config = self.config.get(game.Type.name, None)
            if not config:
                self.statusbar.showMessage('[%s]游戏配置不存在' % game.Type.name, 2000)
                return
            self.setCurrGame(game)

    def onUploadClick(self):
        try:
            self._logic.downloadJsonFile()
            self._logic.genUploadDictByJson()

            self._logic.genUploadJsonFile()
            self._logic.uploadJsonFile()
            self.statusbar.showMessage('上传成功', 2000)
        except Exception as e:
            self.statusbar.showMessage('上传失败', 2000)

    def onClearClick(self):
        try:
            self._logic.downloadJsonFile()
            self._logic.genUploadDictByJson()

            self._logic.clearGameModel()
            self._logic.uploadJsonFile()

            self.perDeployCardDeck.clear()
            for playerView in self.playerViewList:
                playerView.clear()

            self.statusbar.showMessage('清除成功', 2000)
        except Exception as e:
            self.statusbar.showMessage('清除失败', 2000)

    def onSaveActionClick(self):
        if not self._logic.CurrentGame:
            QMessageBox.information(self, "提示", "请选择游戏！")
            return

        inputDialog = QInputDialog()
        inputDialog.setWindowTitle("保存当前配置")
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("牌型名称")
        inputDialog.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

        if inputDialog.exec():
            # 保存当前配置
            name = inputDialog.textValue()
            if self._logic.saveCurrConfig(name):
                QMessageBox.information(self, "提示", "保存成功！")
            else:
                QMessageBox.information(self, "提示", "保存失败！")

    def onLoadActionClick(self):
        if not self._logic.CurrentGame:
            QMessageBox.information(self, "提示", "请选择游戏！")
            return

        dialog = SelectConfigDialog(self)
        if dialog.exec():
            data = dialog.SelectData.Config
            self._logic.updateCardConfigByCurrentGame(data)
            self.updateView(self._logic.CurrentGame)


    # 动画效果修改窗体大小
    def changeSize(self, size):
        self.animation = QPropertyAnimation(self, b'geometry')
        currentGeometry = self.geometry()
        currentGeometry.setSize(size)

        self.animation.setDuration(200)
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(currentGeometry)
        self.animation.start()
