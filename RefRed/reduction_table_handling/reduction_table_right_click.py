from PyQt4 import QtGui

from RefRed.reduction_table_handling.reduction_table_handler import ReductionTableHandler
from RefRed.metadata.display_metadata import DisplayMetadata


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
        o_reduction_table_handler = ReductionTableHandler(parent = self.parent)
        o_reduction_table_handler.full_clear()
        
    def remove_rows(self):
        o_reduction_table_handler = ReductionTableHandler(parent = self.parent)
        o_reduction_table_handler.clear_rows_selected()
        
    def display_metadata(self):
        o_display_metadata = DisplayMetadata(parent = self.parent)
        o_display_metadata.show()