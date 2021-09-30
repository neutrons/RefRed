# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//sf_preview_interface.ui'
#
# Created: Fri May 20 10:03:33 2016
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
        MainWindow.resize(1687, 531)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.full_name_of_sf_file = QtWidgets.QLabel(self.centralwidget)
        self.full_name_of_sf_file.setObjectName(_fromUtf8("full_name_of_sf_file"))
        self.horizontalLayout.addWidget(self.full_name_of_sf_file)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table_widget = QtWidgets.QTableWidget(self.centralwidget)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setObjectName(_fromUtf8("table_widget"))
        self.table_widget.setColumnCount(10)
        self.table_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(9, item)
        self.verticalLayout.addWidget(self.table_widget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1687, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Scaling Factor File Preview", None))
        self.full_name_of_sf_file.setText(_translate("MainWindow", "No Scaling Factor File Selected !", None))
        item = self.table_widget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "New Column", None))
        item = self.table_widget.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "New Column", None))
        self.label.setText(_translate("MainWindow", "Fitting Equation: y = a + b * x", None))

