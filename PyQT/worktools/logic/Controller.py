# -*- coding: utf-8 -*-
import os
import json
from core import ServerHelper, Logger, singleton
from model import CardType, Card
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
class Controller(object):

    def __init__(self):
        self.uploadDict = {}
        self.platformList = []
        self._currentPlatform = None
        self.sqlManager = SqlManager()

    @property
    def currentPlatform(self):
        return self._currentPlatform

    @currentPlatform.setter
    def currentPlatform(self, v):
        self._currentPlatform = v
        if v:
            # 加载平台时 检查一次本地上传文件
            if not os.path.exists(self.localUploadFilePath):
                open(self.localUploadFilePath, 'w', encoding='utf-8')
            # 服务器同步一次文件
            self.downloadJsonFile()
            self.genUploadDictByJson()

    @property
    def localUploadFilePath(self):
        path = os.path.join(UploadFileLocalPath, ('peipai_%s.json' % self.currentPlatform.appid))
        return path

    @property
    def sshUploadFilePath(self):
        path = '%speipai.json' % self.currentPlatform.serverPath
        return path

    def init(self):
        # 获取平台信息
        self.getPlatFormInfo()
        # 没有平台信息
        if len(self.platformList) > 0:
            self.currentPlatform = self.platformList[0]
        else:
            error = '无平台信息，请检查数据库后重启！！！'
            log.log(error)
            return

    # 初始化gameModel
    def initGameModel(self, model):
        gameid = model.id
        if self.uploadDict.get(gameid) and self.uploadDict[gameid].get('default'):
            # 获取配牌信息
            info = self.uploadDict[gameid]['default']
            for dcv in info['dealCards']:
                model.deployedCardList.addCard(Card(dcv, CardType.DealCard))
            for player in model.players:
                for hcv in info['handCards'][player.seatId]:
                    player.handCardList.addCard(Card(hcv, CardType.HandCard))

            # model.updatePlayerDeployedCardListByList()

    # 清除配牌信息
    def clearGameModel(self, model):
        gameid = model.id
        model.deployedCardList.clear()
        for player in model.players:
            player.handCardList.clear()
            player.deployedCardList.clear()

        if self.uploadDict.get(gameid):
            del self.uploadDict[gameid]
        self.writeToLocal()

    def genUploadDictByJson(self):
        with open(self.localUploadFilePath, 'r', encoding='utf-8') as f:
            try:
                self.uploadDict = json.load(f)
            except Exception as e:
                self.uploadDict = {}
                log.error(str(e))

    # 更具model信息生成json
    def genUploadJsonFile(self, model):
        uploadDict = {
            'default': {
                'dealCards': list(reversed(model.deployedCardList.valueList)),
                'handCards': [],
            }
        }
        gameid = model.id
        for player in model.players:
            uploadDict['default']['handCards'].append(player.handCardList.valueList)

        self.uploadDict[gameid] = uploadDict
        # 储存到本地
        self.writeToLocal()

    # 下载配牌json
    def downloadJsonFile(self):
        serverHelper = None
        try:
            serverHelper = self.getServerHelper()
            serverHelper.get_file(self.localUploadFilePath, self.sshUploadFilePath)
        except Exception as e:
            log.error(str(e))
        finally:
            serverHelper.close()

    # 上传配牌json
    def uploadJsonFile(self):
        serverHelper = None
        try:
            serverHelper = self.getServerHelper()
            serverHelper.upload_file(self.localUploadFilePath, self.sshUploadFilePath)
        except Exception as e:
            log.error(str(e))
            raise e
        finally:
            serverHelper.close()

    # 写入到本地
    def writeToLocal(self):
        # 储存到本地
        with open(self.localUploadFilePath, 'w', encoding='utf-8') as f:
            json.dump(self.uploadDict, f)

    # 获取平台信息
    def getPlatFormInfo(self):
        self.platformList = self.sqlManager.getPlatformInfo()

    def getPlatformById(self, id):
        for platform in self.platformList:
            if platform.id == int(id):
                return platform

    def getServerHelper(self):
        return ServerHelper(**ServerConfig)

    def getVersion(self):
        return __version__

    def dispose(self):
        self.sqlManager.dispose()
