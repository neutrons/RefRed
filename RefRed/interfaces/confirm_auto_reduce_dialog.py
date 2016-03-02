# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//confirm_auto_reduce_dialog.ui'
#
# Created: Wed Mar  2 12:45:46 2016
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(542, 130)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(542, 130))
        Dialog.setMaximumSize(QtCore.QSize(542, 130))
        font = QtGui.QFont()
        font.setPointSize(4)
        Dialog.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.file_name = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(12)
        self.file_name.setFont(font)
        self.file_name.setObjectName("file_name")
        self.verticalLayout.addWidget(self.file_name)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.folder_name = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(10)
        self.folder_name.setFont(font)
        self.folder_name.setObjectName("folder_name")
        self.horizontalLayout.addWidget(self.folder_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Abyssinica SIL")
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "CONFIRM NEW AUTO. REDUCTION TEMPLATE", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "You are about to replace the current Automatic Reduction template by:", None, QtGui.QApplication.UnicodeUTF8))
        self.file_name.setText(QtGui.QApplication.translate("Dialog", "N/A", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "File will be copied in: ", None, QtGui.QApplication.UnicodeUTF8))
        self.folder_name.setText(QtGui.QApplication.translate("Dialog", "N/A", None, QtGui.QApplication.UnicodeUTF8))

