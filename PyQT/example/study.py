import sys

from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QDrag, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QToolTip, QAction,
                             QPushButton, QMessageBox, QDesktopWidget, QMenu, qApp, QFrame,
                             QLCDNumber, QSlider, QLabel, QGridLayout, QTextEdit, QLineEdit,
                             QColorDialog, QInputDialog, QFontDialog, QFileDialog)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        # 参数分别代表屏幕坐标的x、y和窗口大小的宽、高
        # resize()和move()的合体
        # self.setGeometry(300, 300, 300, 200)
        self.resize(300, 360)
        self.center()
        self.setWindowTitle("Example")
        self.setWindowIcon(QIcon("images/web.png"))

        mWidget = QWidget()
        self.setCentralWidget(mWidget)
        vgridLayout = QGridLayout()
        vgridLayout.setSpacing(10)
        mWidget.setLayout(vgridLayout)

        self.vgridLayout = vgridLayout
        self.mWidget = mWidget
        self.statusbar = self.statusBar()
        # 计算器窗口
        self.calWindow = CalculateWindow()
        self.editWindow = EditWindow()

        self.show()
        self.initUI()
        self.initMenu()
        self.initToolbar()

    # ------------------------ override ------------------------
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'message', 'Are you sure to quit', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event):
        # 右键菜单
        cmenu = QMenu(self)
        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, event):
        lab = self.findChild(QLabel, 'label')
        lab.setText('x: {0},y: {1}'.format(event.x(), event.y()))

    # ------------------------ override ------------------------
    def initToolbar(self):
        quitAct = QAction(QIcon('images/exit.jpg'), 'quit', self)
        quitAct.setShortcut('Ctrl+Q')
        quitAct.setStatusTip('Exit Application')
        quitAct.triggered.connect(qApp.quit)

        exitToolbar = self.addToolBar('Exit')
        exitToolbar.addAction(quitAct)

    def initMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('file')

        impMenu = QMenu('import', self)
        openAct = QAction('open', self)
        openAct.setObjectName('openAct')
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open File')
        openAct.triggered.connect(self.buttonClicked)
        quitAct = QAction('quit', self)
        quitAct.setShortcut('Ctrl+Q')
        quitAct.setStatusTip('Exit Application')
        quitAct.triggered.connect(qApp.quit)
        viewStatusAct = QAction('ShowStatus', self, checkable=True)
        viewStatusAct.setStatusTip('if show status')
        viewStatusAct.setChecked(True)
        viewStatusAct.triggered.connect(lambda state: self.statusbar.show() if state else self.statusbar.hide())

        fileMenu.addMenu(impMenu)
        fileMenu.addAction(openAct)
        fileMenu.addAction(quitAct)
        fileMenu.addAction(viewStatusAct)

    def initUI(self):
        # 提示框
        QToolTip.setFont(QFont("微软雅黑", 10))

        # 编辑框
        editBtn = QPushButton('Edit', self)
        editBtn.setObjectName('edit')
        editBtn.clicked.connect(self.buttonClicked)
        editBtn.setToolTip('this is a <b>Edit</b> Button')
        editBtn.resize(editBtn.sizeHint())
        self.vgridLayout.addWidget(editBtn, 0, 0)

        # 计算器
        calBtn = QPushButton('Cal', self)
        calBtn.setObjectName('cal')
        calBtn.clicked.connect(self.buttonClicked)
        self.vgridLayout.addWidget(calBtn, 0, 1)

        # lcd num
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        lab = QLabel('x: 0,y: 0', self)
        lab.setObjectName('label')

        self.vgridLayout.addWidget(lcd, 1, 0, 1, 0)
        self.vgridLayout.addWidget(sld, 2, 0, 1, 0)
        self.vgridLayout.addWidget(lab, 3, 0)

        self.setMouseTracking(True)
        sld.valueChanged.connect(lcd.display)

        # inputDialog
        textEdit = QLineEdit()
        textEdit.setDragEnabled(True)
        textEdit.setObjectName('name')
        inputBtn = Button('InputDig', self)
        inputBtn.setObjectName('inputDig')
        inputBtn.clicked.connect(self.buttonClicked)
        self.vgridLayout.addWidget(textEdit, 4, 0)
        self.vgridLayout.addWidget(inputBtn, 4, 1)

        # colorDialog
        colorFrame = QFrame()
        colorFrame.setObjectName('colorFrame')
        colorFrame.setStyleSheet("QWidget { background-color: %s }" % QColor(43, 43, 43).name())
        colorFrame.resize(100, 100)
        colorBtn = QPushButton('ColorDig')
        colorBtn.setObjectName('colorDig')
        colorBtn.clicked.connect(self.buttonClicked)
        self.vgridLayout.addWidget(colorFrame, 5, 0)
        self.vgridLayout.addWidget(colorBtn, 5, 1)

        # fontDialog
        fontLabel = QLabel('This is the font Label')
        fontLabel.setObjectName('fontLabel')
        fontBtn = QPushButton('FontDig', self)
        fontBtn.setObjectName('fontDig')
        fontBtn.clicked.connect(self.buttonClicked)
        self.vgridLayout.addWidget(fontLabel, 6, 0)
        self.vgridLayout.addWidget(fontBtn, 6, 1)

    def buttonClicked(self):
        sender = self.sender()
        if sender.objectName() == 'cal':
            self.calWindow.show()
        elif sender.objectName() == 'edit':
            self.editWindow.show()
        elif sender.objectName() == 'inputDig':
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name')
            if ok:
                self.findChild(QLineEdit, 'name').setText(str(text))
        elif sender.objectName() == 'colorDig':
            col = QColorDialog.getColor()
            if col.isValid():
                self.findChild(QFrame, 'colorFrame').setStyleSheet("QWidget { background-color: %s }" % col.name())
        elif sender.objectName() == 'fontDig':
            font, ok = QFontDialog.getFont()
            if ok:
                self.findChild(QLabel, 'fontLabel').setFont(font)
        elif sender.objectName() == 'openAct':
            fname = QFileDialog.getOpenFileName(self, 'Open File')
            if fname[0]:
                f = open(fname[0], 'r')
                with f:
                    data = f.read()
                    self.findChild(QLabel, 'fontLabel').setText(data)

        self.statusbar.showMessage(sender.text() + ' was passed')

    def center(self):
        qr = self.frameGeometry()
        # 获取显示器的分辨率，然后得到中间点的位置。
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class DragButton(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.icon().pixmap(QSize(60, 60)))
        drag.setHotSpot(self.rect().center())  # 设置跟随的中心点

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            print('press')


class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):

        self.setText(e.mimeData().text())


class CalculateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('Calculator')

    def dragEnterEvent(self, e):
        e.accept()
        print('dragEnterEvent')

    def dropEvent(self, e):
        e.source().move(e.pos())
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def initUI(self):
        self.setAcceptDrops(True)

        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            btn = DragButton(name, self)
            grid.addWidget(btn, *position)


class EditWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(350, 300)
        self.initUI()
        self.setWindowTitle('EditWindow')

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEidt = QLineEdit()
        authorEidt = QLineEdit()
        reviewEidt = QTextEdit()

        grid.addWidget(title, 0, 0)
        grid.addWidget(titleEidt, 0, 1)

        grid.addWidget(author, 1, 0)
        grid.addWidget(authorEidt, 1, 1)

        grid.addWidget(review, 2, 0)
        grid.addWidget(reviewEidt, 2, 1, 5, 1)

        self.setLayout(grid)


if __name__ == '__main__':
    # 每个PyQt5应用都必须创建一个应用对象。sys.argv是一组命令行参数的列表。
    # Python可以在shell里运行，这个参数提供对脚本控制的功能。
    app = QApplication(sys.argv)
    ex = Example()

    # 布局
    # QHBoxLayout，QVBoxLayout，QGridLayout

    # 最后，我们进入了应用的主循环中，事件处理器这个时候开始工作。
    # 主循环从窗口上接收事件，并把事件传入到派发到应用控件里。
    # 当调用exit()方法或直接销毁主控件时，主循环就会结束。
    # sys.exit()方法能确保主循环安全退出。外部环境能通知主控件怎么结束。
    sys.exit(app.exec_())
