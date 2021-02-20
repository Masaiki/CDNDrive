from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 350)
        MainWindow.setFixedSize(800, 350)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 350))
        self.tabWidget.setObjectName("tabWidget")
        self.download_tab = QtWidgets.QWidget()
        self.download_tab.setObjectName("download_tab")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.download_tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 560, 200))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.progressBar = QtWidgets.QProgressBar(self.download_tab)
        self.progressBar.setGeometry(QtCore.QRect(80, 260, 700, 25))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.downloadStartButton = QtWidgets.QPushButton(self.download_tab)
        self.downloadStartButton.setGeometry(QtCore.QRect(580, 10, 200, 28))
        self.downloadStartButton.setObjectName("downloadStartButton")
        self.clearInputButton = QtWidgets.QPushButton(self.download_tab)
        self.clearInputButton.setGeometry(QtCore.QRect(580, 40, 200, 28))
        self.clearInputButton.setObjectName("clearInputButton")
        self.lineEdit = QtWidgets.QLineEdit(self.download_tab)
        self.lineEdit.setGeometry(QtCore.QRect(10, 220, 560, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.selectDirectoryButton = QtWidgets.QPushButton(self.download_tab)
        self.selectDirectoryButton.setGeometry(QtCore.QRect(580, 220, 200, 28))
        self.selectDirectoryButton.setObjectName("selectDirectoryButton")
        self.label = QtWidgets.QLabel(self.download_tab)
        self.label.setGeometry(QtCore.QRect(10, 260, 50, 25))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.download_tab)
        self.label_2.setGeometry(QtCore.QRect(10, 290, 50, 25))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.download_tab, "")
        self.log_tab = QtWidgets.QWidget()
        self.log_tab.setObjectName("log_tab")
        self.logText = QtWidgets.QPlainTextEdit(self.log_tab)
        self.logText.setGeometry(QtCore.QRect(10, 10, 770, 275))
        self.logText.setObjectName("plainTextEdit")
        self.tabWidget.addTab(self.log_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("CDNdrive - GUI", "CDNdrive - GUI"))
        self.plainTextEdit.setPlaceholderText(_translate("Links: seperated by enter", "链接：以回车分隔多个链接"))
        self.downloadStartButton.setText(_translate("Download", "下载"))
        self.clearInputButton.setText(_translate("Clear", "清空"))
        self.lineEdit.setPlaceholderText(_translate("Download directory", "下载目录"))
        self.selectDirectoryButton.setText(_translate("Open", "打开"))
        self.label.setText(_translate("Total progress", "总进度"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.download_tab), _translate("Download tab", "下载"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.log_tab), _translate("Log tab", "日志"))
