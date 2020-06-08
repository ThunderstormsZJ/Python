# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SignUp.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName("SignUp")
        SignUp.setWindowModality(QtCore.Qt.WindowModal)
        SignUp.resize(360, 172)
        SignUp.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(SignUp)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(20, 0, 20, 0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(SignUp)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.nameEdit = QtWidgets.QLineEdit(SignUp)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.nameEdit.setFont(font)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameEdit)
        self.label_2 = QtWidgets.QLabel(SignUp)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.psdEdit = QtWidgets.QLineEdit(SignUp)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.psdEdit.setFont(font)
        self.psdEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.psdEdit.setObjectName("psdEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.psdEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.tipLabel = QtWidgets.QLabel(SignUp)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tipLabel.setFont(font)
        self.tipLabel.setStyleSheet("color: rgb(170, 0, 0);")
        self.tipLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tipLabel.setObjectName("tipLabel")
        self.verticalLayout.addWidget(self.tipLabel)
        self.confirmBtn = QtWidgets.QPushButton(SignUp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confirmBtn.sizePolicy().hasHeightForWidth())
        self.confirmBtn.setSizePolicy(sizePolicy)
        self.confirmBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.confirmBtn.setObjectName("confirmBtn")
        self.verticalLayout.addWidget(self.confirmBtn, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(SignUp)
        QtCore.QMetaObject.connectSlotsByName(SignUp)

    def retranslateUi(self, SignUp):
        _translate = QtCore.QCoreApplication.translate
        SignUp.setWindowTitle(_translate("SignUp", "注册"))
        self.label.setText(_translate("SignUp", "姓名"))
        self.label_2.setText(_translate("SignUp", "密码"))
        self.tipLabel.setText(_translate("SignUp", "tip:提示"))
        self.confirmBtn.setText(_translate("SignUp", "确认"))

