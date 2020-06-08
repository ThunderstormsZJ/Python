# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSettings
from core import Logger
from model import User
from .SqlManager import SqlManager
from .DirPath import ConfigPath
import base64
import hashlib
import os

log = Logger(__name__).get_log()

TOKEN_KEY = "token"


def encryptionPassword(password):
    h = hashlib.sha256(bytes(password, encoding="utf-8"))
    print("hash:", h.hexdigest())
    return h.hexdigest()


class LoginSignLogic(object):
    SIGNUP_FAIL = 0
    SIGNUP_SUCCESS = 1
    SIGNUP_USER_EXISTS = 2

    def __init__(self):
        self._sqlManager = SqlManager()
        self._setting = QSettings(os.path.join(ConfigPath, "config.ini"), QSettings.IniFormat)

    # 保存登陆信息
    def saveToken(self, user):
        if user:
            self._setting.setValue(TOKEN_KEY, base64.b64encode(bytes(user.serialize(), encoding="utf-8")))

    def getToken(self):
        token = self._setting.value(TOKEN_KEY)
        if token:
            return base64.b64decode(token)

        return None

    def removeToken(self):
        self._setting.remove(TOKEN_KEY)

    def getCacheUser(self):
        cacheUser = None
        token = self.getToken()
        if token:
            cacheUser = User()
            cacheUser.invertSerialize(token)

        return cacheUser

    def login(self, name, password):
        loginUser = self._sqlManager.getUserLoginInfo(name, encryptionPassword(password))
        self.saveToken(loginUser)
        return loginUser

    def autoLogin(self, name, password):
        loginUser = self._sqlManager.getUserLoginInfo(name, password)
        return loginUser

    def signUp(self, name, password):
        if self._sqlManager.checkUserExist(name):
            return LoginSignLogic.SIGNUP_USER_EXISTS
        elif self._sqlManager.createUser(name, encryptionPassword(password)):
            return LoginSignLogic.SIGNUP_SUCCESS
        else:
            return LoginSignLogic.SIGNUP_FAIL
