# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//preview_configuration.ui'
#
# Created: Fri May 20 10:03:31 2016
#      by: qtpy UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1222, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(160, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.config_file_name = QtWidgets.QLabel(self.frame)
        self.config_file_name.setObjectName(_fromUtf8("config_file_name"))
        self.horizontalLayout.addWidget(self.config_file_name)
        self.verticalLayout.addWidget(self.frame)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_3.addWidget(self.label_2)
        self.previewTableWidget = QtWidgets.QTableWidget(self.tab)
        self.previewTableWidget.setAlternatingRowColors(True)
        self.previewTableWidget.setObjectName(_fromUtf8("previewTableWidget"))
        self.previewTableWidget.setColumnCount(0)
        self.previewTableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.previewTableWidget)
        self.systemTableWidget = QtWidgets.QTableWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.systemTableWidget.sizePolicy().hasHeightForWidth())
        self.systemTableWidget.setSizePolicy(sizePolicy)
        self.systemTableWidget.setMaximumSize(QtCore.QSize(16777215, 150))
        self.systemTableWidget.setAlternatingRowColors(True)
        self.systemTableWidget.setObjectName(_fromUtf8("systemTableWidget"))
        self.systemTableWidget.setColumnCount(0)
        self.systemTableWidget.setRowCount(0)
        self.systemTableWidget.horizontalHeader().setVisible(False)
        self.systemTableWidget.verticalHeader().setVisible(True)
        self.verticalLayout_3.addWidget(self.systemTableWidget)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.rawTextEdit = QtWidgets.QTextEdit(self.tab_2)
        self.rawTextEdit.setObjectName(_fromUtf8("rawTextEdit"))
        self.verticalLayout_2.addWidget(self.rawTextEdit)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1222, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionBrowse = QtWidgets.QAction(MainWindow)
        self.actionBrowse.setEnabled(True)
        self.actionBrowse.setObjectName(_fromUtf8("actionBrowse"))
        self.menuFile.addAction(self.actionBrowse)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionBrowse, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.action_browse_button)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Configuration File Name:", None))
        self.config_file_name.setText(_translate("MainWindow", "N/A", None))
        self.label_2.setText(_translate("MainWindow", "Runs", None))
        self.label_3.setText(_translate("MainWindow", "System", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Raw", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionBrowse.setText(_translate("MainWindow", "Browse ...", None))

