from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from logic import LoginSignLogic
from ui import Ui_SignUp


class SignUpDialog(QDialog, Ui_SignUp):
    def __init__(self, parent):
        super(SignUpDialog, self).__init__(parent)
        self._logic = LoginSignLogic()
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.setWindowFlags(Qt.Window)
        self.tipLabel.setText("")
        self.confirmBtn.clicked.connect(self.onConfirmClick)

    def onConfirmClick(self):
        name = self.nameEdit.text()
        password = self.psdEdit.text()

        signUpStatus = self._logic.signUp(name, password)
        if signUpStatus == LoginSignLogic.SIGNUP_USER_EXISTS:
            self.tipLabel.setText("用户名已经存在！！")
        elif signUpStatus == LoginSignLogic.SIGNUP_SUCCESS:
            self.tipLabel.setText("注册成功！请继续登陆")
            self.accept()
        else:
            self.tipLabel.setText("注册失败！未知错误！")
