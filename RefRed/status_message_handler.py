"""
    TODO: refactor this
"""
import sys
import time
from qtpy import QtCore
from RefRed.utilities import get_index_free_thread


class StatusMessageThreaded(QtCore.QThread):  # type: ignore
    def setup(self, parent):
        self.parent = parent

    # TODO solve the race condition (see comment after statement "except RuntimeError")
    def run(self):
        time.sleep(5)
        try:
            self.parent.ui.statusbar.showMessage('')
        except RuntimeError:
            # race condition: pytest-qt fixture qtbot kills the main window but fails to kill this thread.
            # As a result, after five seconds there's no self.parent and the previous line raises
            sys.stderr.write("Cannot find main GUI, no status bar to update.\n")


class StatusMessageHandler(object):
    def __init__(self, parent=None, message='', severity='good', is_threaded=True):
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
