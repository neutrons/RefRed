# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//compare_widget.ui'
#
# Created: Fri May 20 10:03:29 2016
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(851, 718)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.frame_7 = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_7.setObjectName(_fromUtf8("frame_7"))
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.comparePlot = MPLWidget(self.frame_7)
        self.comparePlot.setObjectName(_fromUtf8("comparePlot"))
        self.verticalLayout_6.addWidget(self.comparePlot)
        self.widget_6 = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_15.setMargin(0)
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.compareList = QtWidgets.QTableWidget(self.widget_6)
        self.compareList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.compareList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.compareList.setObjectName(_fromUtf8("compareList"))
        self.compareList.setColumnCount(3)
        self.compareList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.compareList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.compareList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.compareList.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_15.addWidget(self.compareList)
        self.frame_8 = QtWidgets.QFrame(self.widget_6)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName(_fromUtf8("frame_8"))
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.pushButton = QtWidgets.QPushButton(self.frame_8)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_10.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_8)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout_10.addWidget(self.pushButton_2)
        self.horizontalLayout_15.addWidget(self.frame_8)
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("pressed()")), Form.open_file)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("pressed()")), Form.clear_plot)
        QtCore.QObject.connect(self.compareList, QtCore.SIGNAL(_fromUtf8("itemChanged(QTableWidgetItem*)")), Form.draw)
        QtCore.QObject.connect(self.compareList, QtCore.SIGNAL(_fromUtf8("cellDoubleClicked(int,int)")), Form.edit_cell)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.compareList, self.pushButton_2)
        Form.setTabOrder(self.pushButton_2, self.pushButton)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        item = self.compareList.horizontalHeaderItem(0)
        item.setText(_translate("Form", "File", None))
        item = self.compareList.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Color", None))
        item = self.compareList.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Label", None))
        self.pushButton.setText(_translate("Form", "Clear", None))
        self.pushButton_2.setText(_translate("Form", "Open", None))

from .mplwidget import MPLWidget
