from PyQt4 import QtGui
from RefRed.interfaces.settings import Ui_MainWindow as UiMainWindow
from RefRed.settings.settings_password_editor import SettingsPasswordEditor


class SettingsEditor(QtGui.QMainWindow):
    
    is_super_user = False
    
    def __init__(self, parent=None):
        self.parent = parent
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

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

            