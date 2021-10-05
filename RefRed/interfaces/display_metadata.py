# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore

# Form implementation generated from reading ui file 'designer//display_metadata.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1178, 979)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.Metadata = QtWidgets.QWidget()
        self.Metadata.setObjectName(_fromUtf8("Metadata"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Metadata)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.metadataTable = QtWidgets.QTableWidget(self.Metadata)
        self.metadataTable.setObjectName(_fromUtf8("metadataTable"))
        self.metadataTable.setColumnCount(3)
        self.metadataTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.metadataTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.metadataTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.metadataTable.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.metadataTable)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.saveMetadataAsAsciiButton = QtWidgets.QPushButton(self.Metadata)
        self.saveMetadataAsAsciiButton.setEnabled(False)
        self.saveMetadataAsAsciiButton.setObjectName(_fromUtf8("saveMetadataAsAsciiButton"))
        self.horizontalLayout_2.addWidget(self.saveMetadataAsAsciiButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.Metadata, _fromUtf8(""))
        self.Configure = QtWidgets.QWidget()
        self.Configure.setObjectName(_fromUtf8("Configure"))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.Configure)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.configureTable = QtWidgets.QTableWidget(self.Configure)
        self.configureTable.setAlternatingRowColors(True)
        self.configureTable.setObjectName(_fromUtf8("configureTable"))
        self.configureTable.setColumnCount(4)
        self.configureTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.configureTable.setHorizontalHeaderItem(3, item)
        self.configureTable.horizontalHeader().setSortIndicatorShown(False)
        self.configureTable.verticalHeader().setSortIndicatorShown(False)
        self.verticalLayout_5.addWidget(self.configureTable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.unselectAllButton = QtWidgets.QPushButton(self.Configure)
        self.unselectAllButton.setObjectName(_fromUtf8("unselectAllButton"))
        self.horizontalLayout.addWidget(self.unselectAllButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.exportConfigurationButton = QtWidgets.QPushButton(self.Configure)
        self.exportConfigurationButton.setObjectName(_fromUtf8("exportConfigurationButton"))
        self.horizontalLayout.addWidget(self.exportConfigurationButton)
        self.importConfigurationButton = QtWidgets.QPushButton(self.Configure)
        self.importConfigurationButton.setObjectName(_fromUtf8("importConfigurationButton"))
        self.horizontalLayout.addWidget(self.importConfigurationButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.Configure, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), Dialog.userChangedTab)
        QtCore.QObject.connect(
            self.saveMetadataAsAsciiButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.saveMetadataListAsAscii
        )
        QtCore.QObject.connect(
            self.exportConfigurationButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.exportConfiguration
        )
        QtCore.QObject.connect(
            self.importConfigurationButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.importConfiguration
        )
        QtCore.QObject.connect(self.unselectAllButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.unselectAll)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        item = self.metadataTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name", None))
        item = self.metadataTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Value", None))
        item = self.metadataTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Units", None))
        self.saveMetadataAsAsciiButton.setText(_translate("Dialog", "Save List of Metadata as ASCII ...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Metadata), _translate("Dialog", "Metadata", None))
        item = self.configureTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Display ?", None))
        item = self.configureTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Name", None))
        item = self.configureTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Value", None))
        item = self.configureTable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Units", None))
        self.unselectAllButton.setText(_translate("Dialog", "Unselect All", None))
        self.exportConfigurationButton.setText(_translate("Dialog", "Export Configuration ...", None))
        self.importConfigurationButton.setText(_translate("Dialog", "Import Configuration ...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Configure), _translate("Dialog", "Configure", None))
