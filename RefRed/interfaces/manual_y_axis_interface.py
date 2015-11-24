# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//manual_y_axis_interface.ui'
#
# Created: Tue Nov 24 14:26:13 2015
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(310, 123)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.auto_rescale = QtGui.QPushButton(Dialog)
        self.auto_rescale.setObjectName("auto_rescale")
        self.verticalLayout.addWidget(self.auto_rescale)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.y_max_value = QtGui.QLineEdit(Dialog)
        self.y_max_value.setObjectName("y_max_value")
        self.gridLayout.addWidget(self.y_max_value, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.y_min_value = QtGui.QLineEdit(Dialog)
        self.y_min_value.setObjectName("y_min_value")
        self.gridLayout.addWidget(self.y_min_value, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.y_min_value, QtCore.SIGNAL("returnPressed()"), Dialog.y_min_event)
        QtCore.QObject.connect(self.y_max_value, QtCore.SIGNAL("returnPressed()"), Dialog.y_max_event)
        QtCore.QObject.connect(self.auto_rescale, QtCore.SIGNAL("clicked()"), Dialog.y_auto_rescale_event)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Manual Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.auto_rescale.setText(QtGui.QApplication.translate("Dialog", "AUTO RESCALE", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "OR", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Y max", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Y min", None, QtGui.QApplication.UnicodeUTF8))

