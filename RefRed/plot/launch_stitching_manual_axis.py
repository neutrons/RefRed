from PyQt4.QtGui import QDialog
from RefRed.interfaces.manual_x_axis_interface import Ui_Dialog as UiDialogXaxis
from RefRed.interfaces.manual_y_axis_interface import Ui_Dialog as UiDialogYaxis

class LaunchStitchingManualXAxis(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent = parent)
        self.setWindowModality(False)
        self.ui = UiDialogXaxis()
        self.ui.setupUi(self)
        self.parent = parent
        
        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)
        
    def closeEvent(self, event=None):
        self.parent.manual_x_axis_dialog = None


class LaunchStitchingManualYAxis(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent = parent)
        self.setWindowModality(False)
        self.ui = UiDialogYaxis()
        self.ui.setupUi(self)
        self.parent = parent

        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)

    def closeEvent(self, event=None):
        self.parent.manual_y_axis_dialog = None
        