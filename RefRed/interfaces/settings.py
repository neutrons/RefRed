# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//settings.ui'
#
# Created: Mon Mar 14 12:19:08 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(2)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.lockButton = QtGui.QPushButton(self.centralwidget)
        self.lockButton.setObjectName(_fromUtf8("lockButton"))
        self.verticalLayout.addWidget(self.lockButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setEnabled(False)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionReset = QtGui.QAction(MainWindow)
        self.actionReset.setEnabled(True)
        self.actionReset.setObjectName(_fromUtf8("actionReset"))
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionReset)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lockButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.edit_button)
        QtCore.QObject.connect(self.actionReset, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.reset_button)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings", None))
        self.label.setText(_translate("MainWindow", "Default Values", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Row", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Row", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column", None))
        self.label_2.setText(_translate("MainWindow", "NB: Hit ENTER to validate changes in each cell!", None))
        self.lockButton.setText(_translate("MainWindow", "UNLOCK !", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionReset.setText(_translate("MainWindow", "Reset", None))

