from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSettings
from RefRed.interfaces.settings import Ui_MainWindow as UiMainWindow
from RefRed.settings.settings_password_editor import SettingsPasswordEditor


class SettingsEditor(QtGui.QMainWindow):
    
    is_super_user = False
    
    def __init__(self, parent=None):
        self.parent = parent
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.populate_table()
    
    def populate_table(self):
        _gui_metadata = self.parent.gui_metadata

        _list_keys = _gui_metadata.keys()
        nbr_key = len(_list_keys)
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(nbr_key)
        self.ui.tableWidget.setVerticalHeaderLabels(_list_keys)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Value'])

        for _index, _key in enumerate(_gui_metadata.keys()):
            _item = QtGui.QTableWidgetItem()
            _item.setFlags(QtCore.Qt.ItemIsSelectable | 
                           QtCore.Qt.ItemIsEnabled | 
                           QtCore.Qt.ItemIsEditable)
            _value = str(_gui_metadata[_key])
            _item.setText(_value)
            self.ui.tableWidget.setItem(_index, 0, _item)

    def edit_button(self):
        if str(self.ui.lockButton.text()) == "LOCK !":
            self.ui.lockButton.setText("UNLOCK !")
            self.is_super_user = False
            self.check_editor_button()
            return

        o_pass = SettingsPasswordEditor(parent = self)
        o_pass.show()
                
    def check_editor_button(self):
        self.ui.tableWidget.setEnabled(self.is_super_user)
        self.ui.actionReset.setEnabled(self.is_super_user)
        self.ui.actionSave.setEnabled(self.is_super_user)

            