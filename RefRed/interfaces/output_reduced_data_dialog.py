# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//output_reduced_data_dialog.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(544, 541)
        Dialog.setMinimumSize(QtCore.QSize(0, 500))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.output4thColumnFlag = QtWidgets.QCheckBox(Dialog)
        self.output4thColumnFlag.setObjectName(_fromUtf8("output4thColumnFlag"))
        self.verticalLayout.addWidget(self.output4thColumnFlag)
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.auto_qmin_button = QtWidgets.QRadioButton(self.frame_2)
        self.auto_qmin_button.setChecked(False)
        self.auto_qmin_button.setObjectName(_fromUtf8("auto_qmin_button"))
        self.horizontalLayout_3.addWidget(self.auto_qmin_button)
        self.manual_qmin_frame = QtWidgets.QFrame(self.frame_2)
        self.manual_qmin_frame.setEnabled(True)
        self.manual_qmin_frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.manual_qmin_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.manual_qmin_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.manual_qmin_frame.setObjectName(_fromUtf8("manual_qmin_frame"))
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.manual_qmin_frame)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtWidgets.QLabel(self.manual_qmin_frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.manual_qmin_value = QtWidgets.QLineEdit(self.manual_qmin_frame)
        self.manual_qmin_value.setMaximumSize(QtCore.QSize(16777215, 27))
        self.manual_qmin_value.setObjectName(_fromUtf8("manual_qmin_value"))
        self.horizontalLayout_5.addWidget(self.manual_qmin_value)
        self.label_6 = QtWidgets.QLabel(self.manual_qmin_frame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.manual_qmin_frame)
        self.verticalLayout.addWidget(self.frame_2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.dq0Value = QtWidgets.QLineEdit(self.groupBox)
        self.dq0Value.setObjectName(_fromUtf8("dq0Value"))
        self.horizontalLayout.addWidget(self.dq0Value)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.dQoverQvalue = QtWidgets.QLineEdit(self.groupBox)
        self.dQoverQvalue.setObjectName(_fromUtf8("dQoverQvalue"))
        self.horizontalLayout_2.addWidget(self.dQoverQvalue)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.one_ascii_format = QtWidgets.QRadioButton(self.groupBox_2)
        self.one_ascii_format.setChecked(True)
        self.one_ascii_format.setObjectName(_fromUtf8("one_ascii_format"))
        self.verticalLayout_4.addWidget(self.one_ascii_format)
        self.n_ascii_format = QtWidgets.QRadioButton(self.groupBox_2)
        self.n_ascii_format.setObjectName(_fromUtf8("n_ascii_format"))
        self.verticalLayout_4.addWidget(self.n_ascii_format)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.base_name_label = QtWidgets.QLabel(self.groupBox_2)
        self.base_name_label.setEnabled(False)
        self.base_name_label.setObjectName(_fromUtf8("base_name_label"))
        self.horizontalLayout_4.addWidget(self.base_name_label)
        self.prefix_name_value = QtWidgets.QLineEdit(self.groupBox_2)
        self.prefix_name_value.setEnabled(False)
        self.prefix_name_value.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.prefix_name_value.setObjectName(_fromUtf8("prefix_name_value"))
        self.horizontalLayout_4.addWidget(self.prefix_name_value)
        self.run_name_label = QtWidgets.QLabel(self.groupBox_2)
        self.run_name_label.setEnabled(False)
        self.run_name_label.setObjectName(_fromUtf8("run_name_label"))
        self.horizontalLayout_4.addWidget(self.run_name_label)
        self.suffix_name_value = QtWidgets.QLineEdit(self.groupBox_2)
        self.suffix_name_value.setEnabled(False)
        self.suffix_name_value.setObjectName(_fromUtf8("suffix_name_value"))
        self.horizontalLayout_4.addWidget(self.suffix_name_value)
        self.ext_name_label = QtWidgets.QLabel(self.groupBox_2)
        self.ext_name_label.setEnabled(False)
        self.ext_name_label.setObjectName(_fromUtf8("ext_name_label"))
        self.horizontalLayout_4.addWidget(self.ext_name_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.createAsciiButton = QtWidgets.QPushButton(Dialog)
        self.createAsciiButton.setObjectName(_fromUtf8("createAsciiButton"))
        self.verticalLayout.addWidget(self.createAsciiButton)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.folder_error = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.folder_error.sizePolicy().hasHeightForWidth())
        self.folder_error.setSizePolicy(sizePolicy)
        self.folder_error.setMaximumSize(QtCore.QSize(16777215, 25))
        self.folder_error.setAlignment(QtCore.Qt.AlignCenter)
        self.folder_error.setObjectName(_fromUtf8("folder_error"))
        self.verticalLayout_2.addWidget(self.folder_error)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(
            self.createAsciiButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.create_reduce_ascii_button_event
        )
        QtCore.QObject.connect(
            self.one_ascii_format, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.output_format_radio_buttons_event
        )
        QtCore.QObject.connect(
            self.n_ascii_format, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.output_format_radio_buttons_event
        )
        QtCore.QObject.connect(
            self.auto_qmin_button, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Dialog.auto_qmin_button
        )
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Export ASCII", None))
        self.output4thColumnFlag.setText(_translate("Dialog", "with 4th column (precision)", None))
        self.auto_qmin_button.setText(_translate("Dialog", "Auto Qmin", None))
        self.label.setText(_translate("Dialog", "Qmin", None))
        self.manual_qmin_value.setText(_translate("Dialog", "0.005", None))
        self.label_6.setText(_translate("Dialog", "1/Å", None))
        self.groupBox.setTitle(_translate("Dialog", "Resolution", None))
        self.label_3.setText(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Sans\'; font-size:10pt;"
                " font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                " text-indent:0px;\">dQ<span style=\" vertical-align:sub;\">0</span></p></body></html>",
                None,
            )
        )
        self.dq0Value.setText(_translate("Dialog", "0.0004", None))
        self.label_4.setText(_translate("Dialog", "1/Å", None))
        self.label_5.setText(
            _translate(
                "Dialog",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Sans\';"
                " font-size:10pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                " text-indent:0px;\">ΔQ<span style=\" vertical-align:sub;\">1</span>/Q</p></body></html>",
                None,
            )
        )
        self.dQoverQvalue.setText(_translate("Dialog", "0.005", None))
        self.groupBox_2.setTitle(_translate("Dialog", "  Output format", None))
        self.one_ascii_format.setText(_translate("Dialog", "1 Ascii File for All Reduced Data Set", None))
        self.n_ascii_format.setText(_translate("Dialog", "n Ascii Files (one for Each Reduced Data Set)", None))
        self.base_name_label.setText(_translate("Dialog", "Base Filenames:", None))
        self.prefix_name_value.setText(_translate("Dialog", "REF_L", None))
        self.run_name_label.setText(_translate("Dialog", "_###_", None))
        self.suffix_name_value.setText(_translate("Dialog", "reduced_data", None))
        self.ext_name_label.setText(_translate("Dialog", ".txt", None))
        self.createAsciiButton.setText(_translate("Dialog", "Create Ascii File ...", None))
        self.folder_error.setText(_translate("Dialog", "CHECK FOLDER PERMISSION !", None))
