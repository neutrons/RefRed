from PyQt4 import QtGui
from PyQt4.QtCore import Qt

class MyTableWidget(QtGui.QTableWidget):
    
    def __init__(self, parent=None):
        self.parent = parent
        super(MyTableWidget, self).__init__(parent)
        
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            print('clicked enter')
        else:
            super(MyTableWidget, self).keyPressEvent(event)
            
            