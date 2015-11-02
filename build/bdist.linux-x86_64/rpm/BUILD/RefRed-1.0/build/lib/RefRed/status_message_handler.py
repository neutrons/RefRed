from PyQt4 import QtCore
import time
from RefRed.status_message_threaded import StatusMessageThreaded
from RefRed.utilities import get_index_free_thread


class StatusMessageHandler(object):
    
    def __init__(self, parent=None, 
                 message='', 
                 severity='good', 
                 is_threaded=True):
        self.parent = parent
        
        if severity == 'good':
            self.parent.ui.statusbar.setStyleSheet("QStatusBar{color: black;}")            
        elif severity == 'bad':
            self.parent.ui.statusbar.setStyleSheet("QStatusBar{color: red;}")
        self.parent.ui.statusbar.showMessage(message)
        
        if is_threaded:
            index = get_index_free_thread(parent=self.parent)
            self.parent.loading_nxs_thread[index] = StatusMessageThreaded()
            self.parent.loading_nxs_thread[index].setup(parent=self.parent)
            self.parent.loading_nxs_thread[index].start()
            

        