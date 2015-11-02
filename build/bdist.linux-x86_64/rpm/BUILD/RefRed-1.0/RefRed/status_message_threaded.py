from PyQt4 import QtCore
import time


class StatusMessageThreaded(QtCore.QThread):
    
    def setup(self, parent):
        self.parent = parent
        
    def run(self):
        time.sleep(5)
        self.parent.ui.statusbar.showMessage('')
        