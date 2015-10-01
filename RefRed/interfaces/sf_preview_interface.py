# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//sf_preview_interface.ui'
#
# Created: Thu Oct  1 10:05:34 2015
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(831, 670)
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
        self.preview_table_widget = QtGui.QTableWidget(self.centralwidget)
        self.preview_table_widget.setObjectName("preview_table_widget")
        self.preview_table_widget.setColumnCount(0)
        self.preview_table_widget.setRowCount(0)
        self.verticalLayout.addWidget(self.preview_table_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Scaling Factor File Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.full_name_of_sf_file.setText(QtGui.QApplication.translate("MainWindow", "N/A", None, QtGui.QApplication.UnicodeUTF8))

