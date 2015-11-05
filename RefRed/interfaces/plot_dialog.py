# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//plot_dialog.ui'
#
# Created: Thu Nov  5 10:48:06 2015
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/General/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plot = MPLWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.horizontalLayout.addWidget(self.plot)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ImaxLabel = QtGui.QLabel(Dialog)
        self.ImaxLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ImaxLabel.setObjectName("ImaxLabel")
        self.verticalLayout.addWidget(self.ImaxLabel)
        self.Imax = QtGui.QDoubleSpinBox(Dialog)
        self.Imax.setMinimum(-30.0)
        self.Imax.setMaximum(30.0)
        self.Imax.setSingleStep(0.1)
        self.Imax.setObjectName("Imax")
        self.verticalLayout.addWidget(self.Imax)
        spacerItem = QtGui.QSpacerItem(0, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.applyButton = QtGui.QPushButton(Dialog)
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.IminLabel = QtGui.QLabel(Dialog)
        self.IminLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.IminLabel.setObjectName("IminLabel")
        self.verticalLayout.addWidget(self.IminLabel)
        self.Imin = QtGui.QDoubleSpinBox(Dialog)
        self.Imin.setMinimum(-30.0)
        self.Imin.setMaximum(30.0)
        self.Imin.setSingleStep(0.1)
        self.Imin.setProperty("value", -6.0)
        self.Imin.setObjectName("Imin")
        self.verticalLayout.addWidget(self.Imin)
        self.clipButton = QtGui.QPushButton(Dialog)
        self.clipButton.setObjectName("clipButton")
        self.verticalLayout.addWidget(self.clipButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.Imin, QtCore.SIGNAL("valueChanged(double)"), Dialog.redrawColorscale)
        QtCore.QObject.connect(self.Imax, QtCore.SIGNAL("valueChanged(double)"), Dialog.redrawColorscale)
        QtCore.QObject.connect(self.clipButton, QtCore.SIGNAL("pressed()"), Dialog.clipData)
        QtCore.QObject.connect(self.applyButton, QtCore.SIGNAL("pressed()"), Dialog.applyScaling)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.ImaxLabel.setText(QtGui.QApplication.translate("Dialog", "Max\n"
"10^", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("Dialog", "Apply\n"
"scales\n"
"to\n"
"all", None, QtGui.QApplication.UnicodeUTF8))
        self.IminLabel.setText(QtGui.QApplication.translate("Dialog", "Min\n"
"10^", None, QtGui.QApplication.UnicodeUTF8))
        self.clipButton.setText(QtGui.QApplication.translate("Dialog", "Clip", None, QtGui.QApplication.UnicodeUTF8))

from .mplwidget import MPLWidget
import icons_rc
