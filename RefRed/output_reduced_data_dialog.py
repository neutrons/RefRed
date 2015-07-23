# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer/output_reduced_data_dialog.ui'
#
# Created: Thu Jul 23 09:35:00 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(406, 360)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.output4thColumnFlag = QtGui.QCheckBox(Dialog)
        self.output4thColumnFlag.setObjectName(_fromUtf8("output4thColumnFlag"))
        self.verticalLayout.addWidget(self.output4thColumnFlag)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.dq0Value = QtGui.QLineEdit(Dialog)
        self.dq0Value.setObjectName(_fromUtf8("dq0Value"))
        self.horizontalLayout.addWidget(self.dq0Value)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.dQoverQvalue = QtGui.QLineEdit(Dialog)
        self.dQoverQvalue.setObjectName(_fromUtf8("dQoverQvalue"))
        self.horizontalLayout_2.addWidget(self.dQoverQvalue)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.usingLessErrorValueFlag = QtGui.QRadioButton(self.groupBox_3)
        self.usingLessErrorValueFlag.setGeometry(QtCore.QRect(25, 24, 199, 22))
        self.usingLessErrorValueFlag.setChecked(True)
        self.usingLessErrorValueFlag.setObjectName(_fromUtf8("usingLessErrorValueFlag"))
        self.usingMeanValueFalg = QtGui.QRadioButton(self.groupBox_3)
        self.usingMeanValueFalg.setGeometry(QtCore.QRect(25, 51, 199, 22))
        self.usingMeanValueFalg.setObjectName(_fromUtf8("usingMeanValueFalg"))
        self.verticalLayout.addWidget(self.groupBox_3)
        self.createAsciiButton = QtGui.QPushButton(Dialog)
        self.createAsciiButton.setObjectName(_fromUtf8("createAsciiButton"))
        self.verticalLayout.addWidget(self.createAsciiButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.folder_error = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folder_error.sizePolicy().hasHeightForWidth())
        self.folder_error.setSizePolicy(sizePolicy)
        self.folder_error.setMaximumSize(QtCore.QSize(16777215, 25))
        self.folder_error.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_error.setObjectName(_fromUtf8("folder_error"))
        self.verticalLayout_2.addWidget(self.folder_error)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.createAsciiButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.create_reduce_ascii_button_event)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Export ASCII", None))
        self.output4thColumnFlag.setText(_translate("Dialog", "with 4th column (precision)", None))
        self.label_3.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">dQ<span style=\" vertical-align:sub;\">0</span></p></body></html>", None))
        self.dq0Value.setText(_translate("Dialog", "0.0004", None))
        self.label_4.setText(_translate("Dialog", "1/Å", None))
        self.label_5.setText(_translate("Dialog", "ΔQ/Q", None))
        self.dQoverQvalue.setText(_translate("Dialog", "0.01", None))
        self.groupBox_3.setTitle(_translate("Dialog", "  How to treat overlap values", None))
        self.usingLessErrorValueFlag.setText(_translate("Dialog", "use lowest error value", None))
        self.usingMeanValueFalg.setText(_translate("Dialog", "use mean value", None))
        self.createAsciiButton.setText(_translate("Dialog", "Create Reduce ASCII ...", None))
        self.folder_error.setText(_translate("Dialog", "CHECK FOLDER PERMISSION !", None))

