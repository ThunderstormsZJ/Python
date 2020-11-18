# -*- coding: utf-8 -*-
import os
import json
from core import ServerHelper, Logger, singleton
from model import CardType, Card
from .LoginSignLogic import LoginSignLogic
from .DirPath import UploadFileLocalPath
from .SqlManager import SqlManager
from . import __version__

log = Logger(__name__).get_log()

# 配置属性
ServerConfig = {
    # 本地项目路径
    'local_path': '',
    # 服务器项目路径
    'ssh_path': '',
    # ssh地址、端口、用户名、密码
    'hostname': '192.168.1.158',
    'port': 22,
    'username': 'zhoujun',
    'password': '13117960232',
}


@singleton
class DeployCardLogic(object):

    def __init__(self):
        self.uploadDict = {}
        self.platformList = []
        self._currentPlatform = None
        self._currentGame = None
        self._currentUser = None

    @property
    def CurrentUser(self):
        return self._currentUser

    @CurrentUser.setter
    def CurrentUser(self, v):
        self._currentUser = v

    @property
    def CurrentGame(self):
        return self._currentGame

    @CurrentGame.setter
    def CurrentGame(self, v):
        self._currentGame = v

    @property
    def CurrentPlatform(self):
        return self._currentPlatform

    @CurrentPlatform.setter
    def CurrentPlatform(self, v):
        self._currentPlatform = v
        if v:
            # 加载平台时 检查一次本地上传文件
            if not os.path.exists(self.LocalUploadFilePath):
                open(self.LocalUploadFilePath, 'w', encoding='utf-8')
            # 服务器同步一次文件
            self.downloadJsonFile()
            self.genUploadDictByJson()

    @property
    def LocalUploadFilePath(self):
        path = os.path.join(UploadFileLocalPath, ('peipai_%s.json' % self._currentPlatform.Appid))
        return path

    @property
    def SShUploadFilePath(self):
        path = '%speipai.json' % self._currentPlatform.ServerPath
        return path

    def init(self):
        self._currentUser = LoginSignLogic().getCacheUser()
        # 获取平台信息
        self.getPlatFormInfo()
        # 没有平台信息
        if len(self.platformList) > 0:
            self._currentPlatform = self.platformList[0]
        else:
            error = '无平台信息，请检查数据库后重启！！！'
            log.log(error)
            return

    # 初始化gameModel
    def initGameModel(self, game):
        gameid = game.Id
        if self.uploadDict.get(gameid) and self.uploadDict[gameid].get('default'):
            # 获取配牌信息
            info = self.uploadDict[gameid]['default']
            for dcv in info['dealCards']:
                game.DeployedCardList.addCard(Card(dcv, CardType.DealCard))
            for player in game.Players:
                for hcv in info['handCards'][player.seatId]:
                    player.handCardList.addCard(Card(hcv, CardType.HandCard))

        self._currentGame = game

    # 清除配牌信息
    def clearGameModel(self):
        game = self.CurrentGame
        gameid = game.Id
        game.DeployedCardList.clear()
        for player in game.Players:
            player.handCardList.clear()
            player.DeployedCardList.clear()

        if self.uploadDict.get(gameid):
            del self.uploadDict[gameid]
        self.writeToLocal()

    # 设置当前游戏牌配置信息
    def updateCardConfigByCurrentGame(self, data):
        if self._currentGame:
            gameid = self._currentGame.Id
            self.uploadDict[gameid] = data
            # 从新更新模型信息
            self.initGameModel(self._currentGame)

    def genUploadDictByJson(self):
        with open(self.LocalUploadFilePath, 'r', encoding='utf-8') as f:
            try:
                self.uploadDict = json.load(f)
            except Exception as e:
                self.uploadDict = {}
                log.error(str(e))

    def genUploadJsonDict(self):
        game = self.CurrentGame
        uploadDict = {
            'default': {
                'dealCards': list(reversed(game.DeployedCardList.valueList)),
                'handCards': [],
            }
        }
        gameid = game.Id
        for player in game.Players:
            uploadDict['default']['handCards'].append(player.handCardList.valueList)

        self.uploadDict[gameid] = uploadDict

        return uploadDict

    # 根据model信息生成json文件
    def genUploadJsonFile(self):
        self.genUploadJsonDict()
        # 储存到本地
        self.writeToLocal()

    # 下载配牌json
    def downloadJsonFile(self):
        serverHelper = None
        try:
            serverHelper = self.getServerHelper()
            serverHelper.get_file(self.LocalUploadFilePath, self.SShUploadFilePath)
        except Exception as e:
            log.error(str(e))
        finally:
            serverHelper.close()

    # 上传配牌json
    def uploadJsonFile(self):
        serverHelper = None
        try:
            serverHelper = self.getServerHelper()
            serverHelper.upload_file(self.LocalUploadFilePath, self.SShUploadFilePath)
        except Exception as e:
            log.error(str(e))
            raise e
        finally:
            serverHelper.close()

    # 写入到本地
    def writeToLocal(self):
        # 储存到本地
        with open(self.LocalUploadFilePath, 'w', encoding='utf-8') as f:
            json.dump(self.uploadDict, f)

    def saveCurrConfig(self, name):
        uploadJsonStr = json.dumps(self.genUploadJsonDict())
        return SqlManager().createGameConfig(self._currentUser, self._currentGame, self._currentPlatform, uploadJsonStr, name)

    def getConfigList(self):
        return SqlManager().getGameConfigList(self._currentUser, self._currentGame, self._currentPlatform)

    # 获取平台信息
    def getPlatFormInfo(self):
        self.platformList = SqlManager().getPlatformInfo()

    def getPlatformById(self, id):
        for platform in self.platformList:
            if platform.id == int(id):
                return platform

    def getServerHelper(self):
        return ServerHelper(**ServerConfig)

    def getVersion(self):
        return __version__
