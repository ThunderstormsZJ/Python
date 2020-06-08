from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from ui import Ui_Update
from logic import UpdateLogic
from model import UpdateStatus


class UpdateDialog(QDialog, Ui_Update):
    def __init__(self, parent):
        super(UpdateDialog, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

        # check update
        self._updateLogic = UpdateLogic()
        self._updateLogic.start()
        self._updateLogic.updateSignal.connect(self.onUpdateCallback)

    def initUi(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.CustomizeWindowHint)
        self.restartBtn.setVisible(False)

    def showRestartBtn(self):
        self.progressBar.setVisible(False)
        self.restartBtn.setVisible(True)

    def onUpdateCallback(self, status, obj):
        if status == UpdateStatus.Begin:
            self.show()

            self.tipLabel.setText("更新[v%s-->v%s]" % (obj.current_version, obj.latest))
            self.progressBar.setRange(0, self._updateLogic.getUpdateFileSize())
        elif status == UpdateStatus.Downloading:
            downloaded = obj.get(u'downloaded')
            self.progressBar.setValue(int(downloaded))
        elif status == UpdateStatus.Downloaded:
            self.progressBar.setValue(self._updateLogic.getUpdateFileSize())
            self.showRestartBtn()
        elif status == UpdateStatus.Fail:
            self.close()
            self._updateLogic.restart()
        elif status == UpdateStatus.Success:
            self._updateLogic.quit()
