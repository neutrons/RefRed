# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//metadata_finder_interface.ui'
#
# Created: Fri May 20 10:03:30 2016
#      by: qtpy UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtGui, QtWidgets

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
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.runNumberEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.runNumberEdit.setText(_fromUtf8(""))
        self.runNumberEdit.setObjectName(_fromUtf8("runNumberEdit"))
        self.horizontalLayout.addWidget(self.runNumberEdit)
        self.inputErrorLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputErrorLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.inputErrorLabel.setFont(font)
        self.inputErrorLabel.setObjectName(_fromUtf8("inputErrorLabel"))
        self.horizontalLayout.addWidget(self.inputErrorLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.searchLabel = QtWidgets.QLabel(self.centralwidget)
        self.searchLabel.setObjectName(_fromUtf8("searchLabel"))
        self.horizontalLayout.addWidget(self.searchLabel)
        self.searchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.horizontalLayout.addWidget(self.searchLineEdit)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setText(_fromUtf8(""))
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout.addWidget(self.clearButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.metadataTable = QtWidgets.QTableWidget(self.tab)
        self.metadataTable.setObjectName(_fromUtf8("metadataTable"))
        self.metadataTable.setColumnCount(2)
        self.metadataTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.metadataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.metadataTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.metadataTable)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.saveAsciiButton = QtWidgets.QPushButton(self.tab)
        self.saveAsciiButton.setObjectName(_fromUtf8("saveAsciiButton"))
        self.horizontalLayout_3.addWidget(self.saveAsciiButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.configureTable = QtWidgets.QTableWidget(self.tab_2)
        self.configureTable.setObjectName(_fromUtf8("configureTable"))
        self.configureTable.setColumnCount(4)
        self.configureTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(3, item)
        self.verticalLayout_3.addWidget(self.configureTable)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.unselectAll = QtWidgets.QPushButton(self.tab_2)
        self.unselectAll.setEnabled(False)
        self.unselectAll.setObjectName(_fromUtf8("unselectAll"))
        self.horizontalLayout_2.addWidget(self.unselectAll)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.exportConfiguration = QtWidgets.QPushButton(self.tab_2)
        self.exportConfiguration.setEnabled(False)
        self.exportConfiguration.setObjectName(_fromUtf8("exportConfiguration"))
        self.horizontalLayout_2.addWidget(self.exportConfiguration)
        self.importConfiguration = QtWidgets.QPushButton(self.tab_2)
        self.importConfiguration.setEnabled(False)
        self.importConfiguration.setObjectName(_fromUtf8("importConfiguration"))
        self.horizontalLayout_2.addWidget(self.importConfiguration)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.tabWidget)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(
            self.runNumberEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.runNumberEditEvent
        )
        QtCore.QObject.connect(self.unselectAll, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.unselectAll)
        QtCore.QObject.connect(
            self.exportConfiguration, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.exportConfiguration
        )
        QtCore.QObject.connect(
            self.importConfiguration, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.importConfiguration
        )
        QtCore.QObject.connect(
            self.tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), MainWindow.userChangedTab
        )
        QtCore.QObject.connect(
            self.saveAsciiButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.saveMetadataListAsAsciiFile
        )
        QtCore.QObject.connect(
            self.searchLineEdit, QtCore.SIGNAL(_fromUtf8("textEdited(QString)")), MainWindow.searchLineEditLive
        )
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.searchLineEditClear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Run(s) number:", None))
        self.runNumberEdit.setToolTip(_translate("MainWindow", "1234 or 1234,1236 or 1234-1238", None))
        self.inputErrorLabel.setText(_translate("MainWindow", "ERROR WHILE PARSING ! CHECK YOUR INPUT  ", None))
        self.searchLabel.setText(_translate("MainWindow", "loop", None))
        item = self.metadataTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Run #", None))
        item = self.metadataTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "IPTS", None))
        self.saveAsciiButton.setText(_translate("MainWindow", "Save List as ASCII ...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Metadata", None))
        self.configureTable.setSortingEnabled(True)
        item = self.configureTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Display ?", None))
        item = self.configureTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name", None))
        item = self.configureTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Value", None))
        item = self.configureTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Units", None))
        self.unselectAll.setText(_translate("MainWindow", "Unselect All", None))
        self.exportConfiguration.setText(_translate("MainWindow", "Export Configuration ...", None))
        self.importConfiguration.setText(_translate("MainWindow", "Import Configuration ...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Configuration", None))
