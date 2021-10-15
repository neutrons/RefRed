'''
  Module for useful decorators
'''
from qtpy import QtGui, QtCore, QtWidgets
from RefRed.version import window_title
from functools import wraps

#
# Help functions adopted from Michele Simionato's decorator module
# http://www.phyast.pitt.edu/~micheles/python/decorator.zip
#


def config_file_modification_reset(function):

    @wraps(function)
    def new_function(*args, **kw):
        ui = args[0]  # first argument is the ui
        current_loaded_file = ui.current_loaded_file
        str_new_window_title = "%s%s" % (window_title, current_loaded_file)
        ui.setWindowTitle(str_new_window_title)
        function(*args, **kw)

    return new_function


def config_file_has_been_modified(function):

    @wraps(function)
    def new_function(self, *args, **kw):
        current_loaded_file = self.current_loaded_file
        self.ui.reduceButton.setEnabled(True)
        str_new_window_title = "%s%s*" % (window_title, current_loaded_file)
        self.setWindowTitle(str_new_window_title)
        function(self, *args, **kw)

    return new_function


def waiting_effects(function):

    @wraps(function)
    def new_function(self, *args, **kw):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        function(self, *args, **kw)
        QtWidgets.QApplication.restoreOverrideCursor()

    return new_function
