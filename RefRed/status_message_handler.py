"""
    TODO: refactor this
"""
import time
from PyQt4 import QtCore
from RefRed.utilities import get_index_free_thread


class StatusMessageThreaded(QtCore.QThread):

    def setup(self, parent):
        self.parent = parent

    def run(self):
        time.sleep(5)
        self.parent.ui.statusbar.showMessage('')


class StatusMessageHandler(object):

    def __init__(self, parent=None, message='',
                 severity='good', is_threaded=True):
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
