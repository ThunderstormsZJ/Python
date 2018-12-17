# -*- coding: utf-8 -*-
# 更新模块
from pyupdater.client import Client
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QProgressDialog
from core import Logger
from .client_config import ClientConfig
from . import __version__

log = Logger(__name__).get_log()


class UpdateManager(QObject):
    updateSignal = pyqtSignal(object)

    def __init__(self, view):
        self._view = view

    def init(self):

        if self.check():
            self._progressDialog = self.showUpdateDialog()
            self._progressDialog.show()
            self.download()

    def check(self):
        client = Client(ClientConfig, refresh=True)
        client.add_progress_hook(self.updateHook)
        appUpdate = client.update_check(ClientConfig.APP_NAME, __version__)
        if appUpdate:
            self._appUpdate = appUpdate
            return True

        return False

    def updateHook(self, info):
        total = info.get(u'total')
        downloaded = info.get(u'downloaded')
        percent_complete = info.get(u'percent_complete')
        self._progressDialog.setRange(0, int(total))
        self._progressDialog.setValue(int(downloaded))
        log.info('[total:%s downloaded:%s percent_complete:%s]' % (total, downloaded, percent_complete))
        self.updateSignal.emit(info)

    def download(self):
        return self._appUpdate.download()

    def restart(self):
        pass

    def showUpdateDialog(self):
        progressDialog = QProgressDialog()
        progressDialog.setWindowTitle('更新')
        progressDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        progressDialog.setLabelText('更新[v%s-->v%s]' % (self._appUpdate.current_version, self._appUpdate.latest))
        progressDialog.setWindowModality(Qt.ApplicationModal)
        progressDialog.setCancelButtonText('重启')
        progressDialog.setAutoClose(False)
        progressDialog.setAutoReset(False)
        progressDialog.setMinimumDuration(10)

        log.info(progressDialog.parent())

        return progressDialog
