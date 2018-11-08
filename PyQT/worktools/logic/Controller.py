# -*- coding: utf-8 -*-
import os
import json
from utils import ServerHelper, Logger, singleton
from model import CardType, Card
from .DirPath import UploadFileLocalJson, UploadFileSSHJson

log = Logger(__name__).get_log()


@singleton
class Controller(object):
    uploadFileLocalPath = UploadFileLocalJson
    uploadFileSSHPath = UploadFileSSHJson

    def __init__(self):
        self.uploadDict = {}

    def init(self):
        # 初始化生成上传文件
        if not os.path.exists(Controller.uploadFileLocalPath):
            open(Controller.uploadFileLocalPath, 'w', encoding='utf-8')
        # 服务器同步一次文件 已服务器准
        serverHelper = None
        try:
            serverHelper = ServerHelper()
            serverHelper.get_file(Controller.uploadFileLocalPath, Controller.uploadFileSSHPath)
        except Exception as e:
            log.error(str(e))
        finally:
            serverHelper.close()

        self.getUploadJson()

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

            model.updatePlayerDeployedCardListByList()

    # 清除配牌信息
    def clearGameModel(self, model):
        gameid = model.id
        model.deployedCardList.clear()
        for player in model.player:
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
                'dealCards': model.deployedCardList.valueList,
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
            serverHelper = ServerHelper()
            serverHelper.upload_file_with_compare(Controller.uploadFileLocalPath, Controller.uploadFileSSHPath)
        except Exception as e:
            log.error(str(e))
            raise e
        finally:
            serverHelper.close()
