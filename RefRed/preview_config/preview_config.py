from PyQt4 import QtGui
from RefRed.interfaces.preview_configuration import Ui_MainWindow as UiMainWindow


class PreviewConfig(QtGui.QMainWindow):
    
    def __init__(self, parent=None, is_live=False):
        self.parent = parent
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        
        if not is_live:
            _file_name = self._browse_file_name()
            if _file_name == "":
                return
        else:
            _file_name = self.parent.current_loaded_file
            
        self.file_name = _file_name
        self._display_raw_file()
            
    def _display_raw_file(self):
        _file = open(self.file_name, 'r')
        data = _file.read()
        _file.close
        self.ui.rawTextEdit.setText(data)
            
    def _browse_file_name(self):
        _path = self.parent.path_config
        _title = "Select Configuration File"
        _filter = ("Config (*.xml)")
        filename = QtGui.QFileDialog.getOpenFileName(self,
                                                     _title,
                                                     _path,
                                                     _filter)
        return filename
        
        
        