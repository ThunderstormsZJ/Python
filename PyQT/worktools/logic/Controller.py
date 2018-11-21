# -*- coding: utf-8 -*-
import os
import json
from utils import ServerHelper, Logger, singleton
from model import CardType, Card
from .DirPath import UploadFileLocalJson, UploadFileSSHJson
from .SqlManager import SqlManager

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
    uploadFileLocalPath = UploadFileLocalJson
    uploadFileSSHPath = UploadFileSSHJson

    def __init__(self):
        self.uploadDict = {}
        self.platformList = []
        self.currentPlatform = None
        self.sqlManager = SqlManager()

    def init(self):
        # 初始化生成上传文件
        if not os.path.exists(Controller.uploadFileLocalPath):
            open(Controller.uploadFileLocalPath, 'w', encoding='utf-8')
        # 服务器同步一次文件 已服务器准
        serverHelper = None
        try:
            serverHelper = self.getServerHelper()
            serverHelper.get_file(Controller.uploadFileLocalPath, Controller.uploadFileSSHPath)
        except Exception as e:
            log.error(str(e))
        finally:
            serverHelper.close()

        self.getUploadJson()
        self.getPlatFormInfo()

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

    def getUploadJson(self):
        with open(Controller.uploadFileLocalPath, 'r', encoding='utf-8') as f:
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
        with open(Controller.uploadFileLocalPath, 'w', encoding='utf-8') as f:
            json.dump(self.uploadDict, f)

    def uploadJsonFile(self):
        serverHelper = None
        try:
            serverHelper = self.getServerHelper()
            serverHelper.upload_file(Controller.uploadFileLocalPath, Controller.uploadFileSSHPath)
        except Exception as e:
            log.error(str(e))
            raise e
        finally:
            serverHelper.close()

    # 获取平台信息
    def getPlatFormInfo(self):
        self.platformList = self.sqlManager.getPlatformInfo()

    def getPlatformById(self, id):
        for platform in self.platformList:
            if platform.id == int(id):
                return platform

    def getServerHelper(self):
        return ServerHelper(**ServerConfig)

    def dispose(self):
        self.sqlManager.dispose()
