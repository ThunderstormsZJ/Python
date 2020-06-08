# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Update.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Update(object):
    def setupUi(self, Update):
        Update.setObjectName("Update")
        Update.resize(273, 87)
        self.verticalLayoutWidget = QtWidgets.QWidget(Update)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 251, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tipLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.tipLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tipLabel.setObjectName("tipLabel")
        self.verticalLayout_2.addWidget(self.tipLabel)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.restartBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restartBtn.sizePolicy().hasHeightForWidth())
        self.restartBtn.setSizePolicy(sizePolicy)
        self.restartBtn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.restartBtn.setObjectName("restartBtn")
        self.verticalLayout_2.addWidget(self.restartBtn, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Update)
        QtCore.QMetaObject.connectSlotsByName(Update)

    def retranslateUi(self, Update):
        _translate = QtCore.QCoreApplication.translate
        Update.setWindowTitle(_translate("Update", "更新"))
        self.tipLabel.setText(_translate("Update", "检测更新中"))
        self.restartBtn.setText(_translate("Update", "重启"))

