#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QApplication
from core import Logger
from widgets import Login, DeployCard, UpdateDialog
from logic import LoginSignLogic, SqlManager
from model import LoginStatus

if getattr(sys, 'frozen', False):
    # frozen
    dir_ = sys._MEIPASS
else:
    # unfrozen
    dir_ = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_)

log = Logger(__name__).get_log()


class MainWindow(object):
    def __init__(self):
        self._loginWindows = None
        self._toolWindows = None
        self._updateDialog = None

        self._loginLogic = LoginSignLogic()

        # check auto login
        cacheUser = self._loginLogic.getCacheUser()
        if cacheUser and self._loginLogic.autoLogin(cacheUser.Name, cacheUser.Password):
            self.showTools()
        else:
            self.showLogin()

    def showLogin(self):
        self._loginWindows = Login()
        self._loginWindows.loginSignal.connect(self.onLoginCallback)
        self._loginWindows.show()

    def showTools(self):
        self._toolWindows = DeployCard()
        self._toolWindows.show()
        self._updateDialog = UpdateDialog(self._toolWindows)

    def onLoginCallback(self, status):
        if status == LoginStatus.Success:
            self._loginWindows.close()
            self.showTools()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication相当于main函数，也就是整个程序（很多文件）的主入口函数。对于GUI程序必须至少有一个这样的实例来让程序运行。
    try:

        window = MainWindow()

        result = app.exec_()
        sys.exit(result)
    except Exception as e:
        log.error(str(e))
    finally:
        SqlManager().dispose()
