# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//sf_preview_interface.ui'
#
# Created: Mon Oct 26 11:23:35 2015
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1687, 531)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.full_name_of_sf_file = QtGui.QLabel(self.centralwidget)
        self.full_name_of_sf_file.setObjectName("full_name_of_sf_file")
        self.horizontalLayout.addWidget(self.full_name_of_sf_file)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table_widget = QtGui.QTableWidget(self.centralwidget)
        self.table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(10)
        self.table_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(9, item)
        self.verticalLayout.addWidget(self.table_widget)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1687, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Scaling Factor File Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.full_name_of_sf_file.setText(QtGui.QApplication.translate("MainWindow", "No Scaling Factor File Selected !", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(8).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.table_widget.horizontalHeaderItem(9).setText(QtGui.QApplication.translate("MainWindow", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Fitting Equation: y = a + b * x", None, QtGui.QApplication.UnicodeUTF8))

