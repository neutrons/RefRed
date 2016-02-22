from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSettings
from RefRed.interfaces.settings import Ui_MainWindow as UiMainWindow
from RefRed.settings.settings_password_editor import SettingsPasswordEditor
from RefRed.gui_handling.gui_utility import GuiUtility


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
            if _key == 'clocking_pixel':
                [_pixel1, _pixel2] = _gui_metadata[_key]
                _value = "%d, %d" %(_pixel1, _pixel2)
            else:
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

    def closeEvent(self, event=None):
        # saving back all the settings
        nbr_row = self.ui.tableWidget.rowCount()
        _gui_metadata = {}
        for _row in range(nbr_row):
            _label = str(self.ui.tableWidget.verticalHeaderItem(_row).text())
            if _label == 'clocking_pixel':
                _value = str(self.ui.tableWidget.item(_row, 0).text())
                [_pixel1, _pixel2] = _value.split(",")
                _value = [int(_pixel1), int(_pixel2)]
            else:
                _value = float(self.ui.tableWidget.item(_row, 0).text())
            _gui_metadata[_label] = _value
        self.parent.gui_metadata = _gui_metadata
        
        #update GUI widgets
        o_gui = GuiUtility(parent = self.parent)
        o_gui.init_widgets_value()