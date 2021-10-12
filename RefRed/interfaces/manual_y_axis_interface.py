# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//manual_y_axis_interface.ui'
#
# Created: Fri May 20 10:03:30 2016
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
        MainWindow.resize(413, 183)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 183))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 183))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.auto_rescale = QtWidgets.QPushButton(self.centralwidget)
        self.auto_rescale.setObjectName(_fromUtf8("auto_rescale"))
        self.verticalLayout.addWidget(self.auto_rescale)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.y_max_value = QtWidgets.QLineEdit(self.centralwidget)
        self.y_max_value.setObjectName(_fromUtf8("y_max_value"))
        self.gridLayout.addWidget(self.y_max_value, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.y_min_value = QtWidgets.QLineEdit(self.centralwidget)
        self.y_min_value.setObjectName(_fromUtf8("y_min_value"))
        self.gridLayout.addWidget(self.y_min_value, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 413, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.y_min_value, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.y_min_event)
        QtCore.QObject.connect(self.y_max_value, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.y_max_event)
        QtCore.QObject.connect(
            self.auto_rescale, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.y_auto_rescale_event
        )
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Manual Y Axis", None))
        self.auto_rescale.setText(_translate("MainWindow", "AUTO RESCALE", None))
        self.label.setText(_translate("MainWindow", "Y max", None))
        self.label_3.setText(_translate("MainWindow", "Y min", None))
        self.label_2.setText(_translate("MainWindow", "OR", None))
