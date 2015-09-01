from PyQt4 import QtGui
import numpy as np


class ReductionTableRightClick(object):
    
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
    def run(self):
        menu = QtGui.QMenu(self.parent)
        remove_row = menu.addAction("Remove Row(s)")
        clear_table = menu.addAction("Clear Table")
        menu.addSeparator()
        display_metadata = menu.addAction("Display Metadata ...")
        action = menu.exec_(QtGui.QCursor.pos())
    
        if action == clear_table:
            self.clear_table()
        elif action == remove_row:
            self.remove_rows()
        elif action == display_metadata:
            self.display_metadata()
        
    def clear_table(self):
        self.clear_big_table_data()
        self.clear_reduction_table()

    def clear_reduction_table(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")
        
    def clear_big_table_data(self):
        self.parent.big_table_data = np.empty((self.parent.nbr_row_table_reduction,
                                               3), dtype = object)
        
    def remove_rows(self):
        print('remove_row')
        
    def display_metadata(self):
        print('display metadata')