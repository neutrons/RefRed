'''
  Module for useful decorators
'''
from qtpy import QtGui, QtCore, QtWidgets
from RefRed.version import window_title
from functools import wraps
from mantid.kernel import Logger


_mantid_logger = Logger('RefRed')

#
# Wrapper functions to make logging call signatures "easy"
#


def _to_call_signature(func_ptr, ref='', *args, **kwargs) -> str:
    '''Helper function to convert function call to an overly detailed string representation'''
    result = func_ptr.__name__
    if ref:
        result = f'{ref}.{result}'
    # TODO check for log level and skip converting values to string if level is too high
    if True:
        args_str = ', '.join([f'{item}' for item in args] + [f'{key}={value}' for key, value in kwargs.items()])
    else:
        args_str = ''
    return f'{result}({args_str})'


def log_qtpy_slot(function):
    '''qt slots are called with a unique signature that don't appear to match the native function signature'''

    @wraps(function)
    def wrapper_func(ref):
        _mantid_logger.information('qtpy slot ' + _to_call_signature(function, ref))  # TODO change to mantid logging
        return function(ref)

    return wrapper_func


def log_function(function):
    @wraps(function)
    def wrapper_func(*args, **kwargs):
        _mantid_logger.information(
            _to_call_signature(function, ref='', *args, **kwargs)
        )  # TODO change to mantid logging
        print()
        return function(*args, **kwargs)

    return wrapper_func


def log_method(function):
    @wraps(function)
    def wrapper_func(ref, *args, **kwargs):
        _mantid_logger.information(
            _to_call_signature(function, ref=ref, *args, **kwargs)
        )  # TODO change to mantid logging
        return function(ref, *args, **kwargs)

    return wrapper_func


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
