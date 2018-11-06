# -*- coding: utf-8 -*-
import os
import json
from utils import ServerHelper, Logger, singleton

log = Logger(__name__).get_log()


@singleton
class Controller(object):
    uploadFileLocalPath = os.path.join(os.getcwd(), 'res', 'data', 'peipai.json')
    uploadFileSSHPath = '/home/zhoujun/peipai.json'

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
                'handCards': {},
            }
        }
        gameid = model.id
        for player in model.players:
            uploadDict['default']['handCards'][str(player.seatId)] = player.handCardList.valueList

        self.uploadDict[gameid] = uploadDict
        # 储存到本地
        with open(Controller.uploadFileLocalPath, 'w', encoding='utf-8') as f:
            json.dump(self.uploadDict, f)
