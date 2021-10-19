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
        mainwindow = args[0]  # first argument is the mainwindow
        current_loaded_file = mainwindow.current_loaded_file
        str_new_window_title = "%s%s" % (window_title, current_loaded_file)
        mainwindow.setWindowTitle(str_new_window_title)
        function(*args, **kw)

    return new_function


def config_file_has_been_modified(function):

    @wraps(function)
    def new_function(*args, **kw):
        mainwindow = args[0]  # first argument is the ui
        current_loaded_file = mainwindow.current_loaded_file
        mainwindow.ui.reduceButton.setEnabled(True)
        str_new_window_title = "%s%s*" % (window_title, current_loaded_file)
        mainwindow.setWindowTitle(str_new_window_title)
        function(*args, **kw)

    return new_function


def waiting_effects(function):

    @wraps(function)
    def new_function(self, *args, **kw):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        function(self, *args, **kw)
        QtWidgets.QApplication.restoreOverrideCursor()

    return new_function
