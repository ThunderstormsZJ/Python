from logic import LoginSignLogic
from ui import Ui_Login
from widgets import SignUpDialog
from model import LoginStatus
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QDialog


class Login(QMainWindow, Ui_Login):
    loginSignal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self._logic = LoginSignLogic()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.tipLabel.setText("")
        self.loginBtn.clicked.connect(self.onLoginClick)
        self.signUpBtn.clicked.connect(self.onSignUpClick)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            self.loginWithUi()
        else:
            super().keyPressEvent(qKeyEvent)

    def loginWithUi(self):
        name = self.nameEdit.text()
        password = self.psdEdit.text()
        loginUser = self._logic.login(name, password)
        if loginUser:
            self.loginSignal.emit(LoginStatus.Success)
            self.tipLabel.setText("提示：登陆成功！")
        else:
            self.loginSignal.emit(LoginStatus.Fail)
            self.tipLabel.setText("提示：用户名或密码错误！")

    def onLoginClick(self):
        self.loginWithUi()

    def onSignUpClick(self):
        dialog = SignUpDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            pass
