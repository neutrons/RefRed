# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//manual_x_axis_interface.ui'
#
# Created: Fri May 20 10:03:29 2016
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
        MainWindow.resize(740, 92)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 80))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 92))
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.auto_rescale = QtGui.QPushButton(self.centralwidget)
        self.auto_rescale.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.auto_rescale.setObjectName(_fromUtf8("auto_rescale"))
        self.horizontalLayout.addWidget(self.auto_rescale)
        spacerItem = QtGui.QSpacerItem(52, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(53, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.x_min_value = QtGui.QLineEdit(self.centralwidget)
        self.x_min_value.setObjectName(_fromUtf8("x_min_value"))
        self.horizontalLayout.addWidget(self.x_min_value)
        spacerItem2 = QtGui.QSpacerItem(52, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.x_max_value = QtGui.QLineEdit(self.centralwidget)
        self.x_max_value.setObjectName(_fromUtf8("x_max_value"))
        self.horizontalLayout.addWidget(self.x_max_value)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 740, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.x_max_value, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.x_max_event)
        QtCore.QObject.connect(self.x_min_value, QtCore.SIGNAL(_fromUtf8("returnPressed()")), MainWindow.x_min_event)
        QtCore.QObject.connect(self.auto_rescale, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.x_auto_rescale_event)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Manual x Axis", None))
        self.auto_rescale.setText(_translate("MainWindow", "AUTO RESCALE", None))
        self.label_2.setText(_translate("MainWindow", "OR", None))
        self.label_3.setText(_translate("MainWindow", "X min", None))
        self.label.setText(_translate("MainWindow", "X max", None))

