# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//manual_x_axis_interface.ui'
#
# Created: Fri Nov  6 15:19:44 2015
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(498, 46)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.x_min_value = QtGui.QLineEdit(Dialog)
        self.x_min_value.setObjectName("x_min_value")
        self.horizontalLayout.addWidget(self.x_min_value)
        spacerItem = QtGui.QSpacerItem(81, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.x_max_value = QtGui.QLineEdit(Dialog)
        self.x_max_value.setObjectName("x_max_value")
        self.horizontalLayout.addWidget(self.x_max_value)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.x_min_value, QtCore.SIGNAL("returnPressed()"), Dialog.x_min_event)
        QtCore.QObject.connect(self.x_max_value, QtCore.SIGNAL("returnPressed()"), Dialog.x_max_event)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Manual X Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "X min", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "X max", None, QtGui.QApplication.UnicodeUTF8))

