from .default_interface_refl import Ui_MainWindow
from PyQt4 import QtGui


class MainGui(QtGui.QMainWindow):


    def __init__(self, argv=[], parent=None):
        if parent is None:
            QtGui.QMainWindow.__init__(self)
        else:
            QtGui.QMainWindow.__init__(self, parent, QtCore.Qt.Window)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
#        InitializeGui(self)
#        MakeGuiConnections(self)
        

    
