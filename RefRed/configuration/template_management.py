import glob
import os
import numpy as np
from PyQt4 import QtGui, QtCore
from RefRed.interfaces.template_management import Ui_MainWindow
from RefRed.preview_config.preview_config import PreviewConfig


class TemplateManagement(QtGui.QMainWindow):
    
    _window_title = "Template Management - "
    _filter = "*template*.cfg"
    _list_filter = ['*template*.cfg', '*.cfg', '*.txt', '*']
    _window_offset = np.array([25, 50])
    
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
        self._clear_table()
        self.ui.tableWidget.setColumnCount(2)

        _folder = self._folder
        _filter = self._filter
        _list_files = glob.glob(_folder + '/' + _filter)
        self._list_files = _list_files
        self.ui.tableWidget.setRowCount(len(_list_files))

        for _row, _file in enumerate(_list_files):
            if _row == 0:
                # put full path in window title
                _path = os.path.dirname(_file)
                self.setWindowTitle(self._window_title + _path)

            # name of file
            _short_file = os.path.basename(_file)
            _item = QtGui.QTableWidgetItem(_short_file)
            self.ui.tableWidget.setItem(_row, 0, _item)
        
            # preview button
            _button = QtGui.QPushButton("Preview")
            QtCore.QObject.connect(_button, QtCore.SIGNAL("clicked()"),
                                   lambda row=_row: self.preview_button(row))
            self.ui.tableWidget.setCellWidget(_row, 1, _button)
        
        _default_selection = QtGui.QTableWidgetSelectionRange(0, 0, 0, 1)
        self.ui.tableWidget.setRangeSelected(_default_selection, True)

    def preview_button(self, _row):
        o_preview_config = PreviewConfig(parent = self, 
                                         is_live = False,
                                         filename = self._list_files[_row],
                                         geometry_parent = self.geometry(),
                                         window_offset = _row * self._window_offset)
        o_preview_config.show()
        
    def _clear_table(self):
        self.ui.tableWidget.clear()
    
    def filterTemplateButton(self, filter_string):
        self._filter = str(filter_string)
    
    def templateFileSelectedButton(self):
        print('template')
    