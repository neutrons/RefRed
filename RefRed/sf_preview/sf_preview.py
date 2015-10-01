from PyQt4 import QtGui, QtCore
from RefRed.interfaces.sf_preview_interface import Ui_MainWindow

class SFPreview(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        