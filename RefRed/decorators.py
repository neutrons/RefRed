'''
  Module for useful decorators
'''
from PyQt4 import QtGui, QtCore
from RefRed.version import window_title
#
# Help functions adopted from Michele Simionato's decorator module
# http://www.phyast.pitt.edu/~micheles/python/decorator.zip
#


def config_file_modification_reset(function):
    def new_function(self, *args, **kw):
        current_loaded_file = self.current_loaded_file
        str_new_window_title = ("%s%s" % (window_title, current_loaded_file))
        self.setWindowTitle(str_new_window_title)
        function(self, *args, **kw)
    return new_function


def config_file_has_been_modified(function):
    def new_function(self, *args, **kw):
        current_loaded_file = self.current_loaded_file
        self.ui.reduceButton.setEnabled(True)
        str_new_window_title = ("%s%s*" % (window_title, current_loaded_file))
        self.setWindowTitle(str_new_window_title)
        function(self, *args, **kw)
    return new_function


def waiting_effects(function):
    def new_function(self, *args, **kw):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        function(self, *args, **kw)
        QtGui.QApplication.restoreOverrideCursor()
    return new_function
