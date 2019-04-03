# -*- coding: utf-8 -*-
# 更新模块
import time
from pyupdater.client import Client
from pyupdater import settings
from PyQt5.QtCore import pyqtSignal, QThread
from core import Logger
from model.enum import UpdateStatus
from .client_config import ClientConfig
from . import __version__

log = Logger(__name__).get_log()


class UpdateManager(QThread):
    updateSignal = pyqtSignal(object, object)

    def __init__(self):
        super(UpdateManager, self).__init__()

    # 注意线程中不要直接访问GUI 要用线程
    def run(self):
        if self.check():
            # 延迟处理
            time.sleep(0.2)
            self.updateSignal.emit(UpdateStatus.Begin, self.appUpdate)

            if self.appUpdate.is_downloaded():
                self.updateSignal.emit(UpdateStatus.Downloaded, self.appUpdate)
            else:
                try:
                    downloadStatus = self.appUpdate.download()
                    if downloadStatus:
                        self.updateSignal.emit(UpdateStatus.Downloaded, self.appUpdate)
                except Exception as e:
                    # Download Fail
                    self.updateSignal.emit(UpdateStatus.Fail, e)
                    log.error('Dowload Error [%s]' % str(e))
        else:
            self.updateSignal.emit(UpdateStatus.Success, None)

    def getUpdateFileSize(self):
        if self.appUpdate:
            filename_key = '{}*{}*{}*{}*{}'.format(settings.UPDATES_KEY, self.appUpdate.name,
                                                   self.appUpdate.latest, self.appUpdate.platform, 'file_size')
            fileSize = self.appUpdate.easy_data.get(filename_key)
            return fileSize

        return 0

    def check(self):
        client = Client(ClientConfig, refresh=True)
        client.add_progress_hook(self.updateHook)
        appUpdate = client.update_check(ClientConfig.APP_NAME, __version__)
        if appUpdate:
            self.appUpdate = appUpdate
            return True

        return False

    def restart(self):
        if self.appUpdate and self.appUpdate.is_downloaded():
            self.appUpdate.extract_restart()

    def updateHook(self, info):
        self.updateSignal.emit(UpdateStatus.Downloading, info)
