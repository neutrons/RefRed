# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//manual_x_axis_interface.ui'
#
# Created: Tue Nov 24 13:27:48 2015
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(584, 45)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.auto_rescale = QtGui.QPushButton(Dialog)
        self.auto_rescale.setObjectName("auto_rescale")
        self.horizontalLayout.addWidget(self.auto_rescale)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.x_min_value = QtGui.QLineEdit(Dialog)
        self.x_min_value.setObjectName("x_min_value")
        self.horizontalLayout.addWidget(self.x_min_value)
        spacerItem2 = QtGui.QSpacerItem(81, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.x_max_value = QtGui.QLineEdit(Dialog)
        self.x_max_value.setObjectName("x_max_value")
        self.horizontalLayout.addWidget(self.x_max_value)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.x_min_value, QtCore.SIGNAL("returnPressed()"), Dialog.x_min_event)
        QtCore.QObject.connect(self.x_max_value, QtCore.SIGNAL("returnPressed()"), Dialog.x_max_event)
        QtCore.QObject.connect(self.auto_rescale, QtCore.SIGNAL("clicked()"), Dialog.x_auto_rescale_event)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Manual X Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.auto_rescale.setText(QtGui.QApplication.translate("Dialog", "AUTO RESCALE", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "OR", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "X min", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "X max", None, QtGui.QApplication.UnicodeUTF8))

