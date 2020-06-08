# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Tools.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ToolWindow(object):
    def setupUi(self, ToolWindow):
        ToolWindow.setObjectName("ToolWindow")
        ToolWindow.resize(735, 500)
        self.centralwidget = QtWidgets.QWidget(ToolWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gameLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.gameLabel.setFont(font)
        self.gameLabel.setText("")
        self.gameLabel.setObjectName("gameLabel")
        self.horizontalLayout.addWidget(self.gameLabel)
        self.selectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.selectBtn.setObjectName("selectBtn")
        self.horizontalLayout.addWidget(self.selectBtn)
        self.uploadBtn = QtWidgets.QPushButton(self.centralwidget)
        self.uploadBtn.setObjectName("uploadBtn")
        self.horizontalLayout.addWidget(self.uploadBtn)
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.clearBtn.setObjectName("clearBtn")
        self.horizontalLayout.addWidget(self.clearBtn)
        self.horizontalLayout.setStretch(0, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.playerTable = QtWidgets.QTableWidget(self.centralwidget)
        self.playerTable.setObjectName("playerTable")
        self.playerTable.setColumnCount(0)
        self.playerTable.setRowCount(0)
        self.verticalLayout.addWidget(self.playerTable)
        ToolWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ToolWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 735, 23))
        self.menubar.setObjectName("menubar")
        ToolWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ToolWindow)
        self.statusbar.setObjectName("statusbar")
        ToolWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ToolWindow)
        QtCore.QMetaObject.connectSlotsByName(ToolWindow)

    def retranslateUi(self, ToolWindow):
        _translate = QtCore.QCoreApplication.translate
        ToolWindow.setWindowTitle(_translate("ToolWindow", "配牌工具"))
        self.selectBtn.setText(_translate("ToolWindow", "选择游戏"))
        self.uploadBtn.setText(_translate("ToolWindow", "上传配牌"))
        self.clearBtn.setText(_translate("ToolWindow", "清除配牌"))

