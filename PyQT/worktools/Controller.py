# -*- coding: utf-8 -*-
import os


class Controller(object):
    uploadFilePath = os.path.join(os.getcwd(), 'res', 'data', 'peipai.json')

    def __init__(self):
        # 初始化生成上传文件 和 服务器同步一次文件
        if not os.path.exists(Controller.uploadFilePath):
            open(Controller.uploadFilePath, 'w', encoding='utf-8')

    def getUploadJson(self):
        pass

    def genUploadJsonFile(self):
        pass
