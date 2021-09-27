from qtpy import QtWidgets
from qtpy.QtCore import Qt

class MyTableWidget(QtWidgets.QTableWidget):
    
    parent = None
    ui = None
    
    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)
        
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            self.parent.table_reduction_cell_enter_pressed()
        else:
            super(MyTableWidget, self).keyPressEvent(event)
            
    def setUI(self, ui_parent):
        self.parent = ui_parent
