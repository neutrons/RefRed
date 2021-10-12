from qtpy import QtWidgets
from RefRed.interfaces.settings_password import Ui_Dialog as UiDialog


class SettingsPasswordEditor(QtWidgets.QDialog):

    password = '5'

    def __init__(self, parent=None):
        self.parent = parent
        QtWidgets.QDialog.__init__(self, parent=parent)
        self.ui = UiDialog()
        self.ui.setupUi(self)

    def closeEvent(self, event=None):
        pass

    def accept(self):
        _user_pass = str(self.ui.lineEdit.text())
        if _user_pass == self.password:
            self.parent.is_super_user = True
        else:
            self.parent.is_super_user = False
        self.parent.check_editor_button()
        if self.parent.is_super_user:
            self.parent.ui.lockButton.setText("LOCK !")
        self.close()
