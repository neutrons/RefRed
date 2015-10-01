from PyQt4 import QtGui, QtCore
import numpy as np
from RefRed.interfaces.sf_preview_interface import Ui_MainWindow
from RefRed.sf_preview.sf_file_handler import SFFileHandler


class SFPreview(QtGui.QMainWindow):
    
    col_width = 100
    col_width1 = col_width + 50
    column_widths = [230, 150, col_width, 
                    col_width, col_width,
                    col_width, 
                    col_width1, col_width1, col_width1, col_width1]
    
    def __init__(self, parent=None, filename=''):
        self.parent = parent
        
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        filename = self.parent.full_scaling_factor_file_name
        if filename == '':
            return
        
        self.filename = filename
        self.init_gui()
        
    def init_gui(self):
        o_sf_file_handler = SFFileHandler(filename = self.filename)
        o_sf_file_handler.retrieve_contain()
        self.labels = o_sf_file_handler.full_sf_factor_labels
        self.init_table_labels()
        self.big_table = o_sf_file_handler.full_sf_factor_table
        self.init_table_contain()
        self.init_name_of_file()
        
    def init_name_of_file(self):
        self.ui.full_name_of_sf_file.setText(self.filename)

    def init_table_labels(self):
        labels = self.labels
        self.ui.table_widget.setHorizontalHeaderLabels(labels)
        column_widths = self.column_widths
        for index, width in enumerate(column_widths):
            self.ui.table_widget.setColumnWidth(index, width)
    
    def init_table_contain(self):
        values = self.big_table
        [nbr_row, nbr_col] = np.shape(values)
        for _row in range(nbr_row):
            self.ui.table_widget.insertRow(_row)
            for _col in range(nbr_col):
                _value = values[_row][_col]
                _item = QtGui.QTableWidgetItem()
                _item.setText(_value)
                self.ui.table_widget.setItem(_row, _col, _item)