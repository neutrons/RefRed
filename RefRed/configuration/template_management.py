import glob
from PyQt4 import QtGui, QtCore
from RefRed.interfaces.template_management import Ui_MainWindow


class TemplateManagement(QtGui.QMainWindow):
    
    _filter = "*template*.cfg"
    _list_filter = ['*template*.cfg', '*.cfg', '*.txt', '*']
    
    def __init__(self, parent=None):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._init_gui()
        
        
    def _init_gui(self):
        self.ui.template_filter_button.addItems(self._list_filter)
        
    def browseFolderButton(self):
        _path = self.parent.path_config
        pathQFileDialog = QtGui.QFileDialog(self.parent)
        folder = str(pathQFileDialog.getExistingDirectory(self, 
                                                      'Select Template Folder',
                                                      _path,
                                                      QtGui.QFileDialog.ShowDirsOnly))
        
        if folder == "":
            return
        
        self._folder = folder
        self._populate_table()

    def _populate_table(self):
        _folder = self._folder
        _filter = self._filter
        _list_files = glob.glob(_folder + '/' + _filter)
        
        self._clear_table()
        
        
    def _clear_table(self):
        self.ui.tableWidget.clear()
        
    
    def filterTemplateButton(self, filter_string):
        self._filter
    
    def templateFileSelectedButton(self):
        print('template')
    