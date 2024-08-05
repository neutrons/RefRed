'''
  Module for useful decorators
'''

from qtpy import QtGui, QtCore, QtWidgets
from RefRed import WINDOW_TITLE
from functools import wraps
from mantid.kernel import ConfigService, Logger


def _shouldShowLogs():
    '''Determine whether logs will be shown on startup'''
    levels = ['debug', 'information', 'notice', 'warning', 'error', 'critical', 'fatal']
    log_level_str = ConfigService.getString('logging.loggers.root.level')
    if log_level_str in levels:
        return levels.index('debug') >= levels.index(log_level_str)
    else:
        # default behavior is to let mantid sort things out
        return True


# finish setting up determining whether to log
SHOULD_LOG = _shouldShowLogs()
del _shouldShowLogs
_mantid_logger = Logger('RefRed')  # handle to the logger
_write_log = _mantid_logger.debug  # pointer to the object's method

#
# Wrapper functions to make logging call signatures "easy"
#


def _to_call_signature(func_ptr, ref_ptr=None, *args, **kwargs) -> str:
    '''Helper function to convert function call to an overly detailed string representation'''
    func_name = func_ptr.__name__
    if ref_ptr:
        func_name = f'{ref_ptr}.{func_name}'
    # check for log level and skip converting values to string if level is too high
    if SHOULD_LOG:
        args_str = ', '.join([f'{item}' for item in args] + [f'{key}={value}' for key, value in kwargs.items()])
    else:
        args_str = 'NOT SHOWN'
    return f'{func_name}({args_str})'


def log_qtpy_slot(function):
    '''qt slots are called with a unique signature that don't appear to match the native function signature'''

    @wraps(function)
    def wrapper_func(ref):
        _write_log('qtpy slot ' + _to_call_signature(function, ref))
        return function(ref)

    return wrapper_func


def log_function(function):
    @wraps(function)
    def wrapper_func(*args, **kwargs):
        _write_log(_to_call_signature(function, ref_ptr='', *args, **kwargs))
        return function(*args, **kwargs)

    return wrapper_func


def log_method(function):
    @wraps(function)
    def wrapper_func(ref, *args, **kwargs):
        _write_log(_to_call_signature(function, ref_ptr=ref, *args, **kwargs))
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
        str_new_window_title = "%s%s" % (WINDOW_TITLE, current_loaded_file)
        mainwindow.setWindowTitle(str_new_window_title)
        function(*args, **kw)

    return new_function


def config_file_has_been_modified(function):
    @wraps(function)
    def new_function(*args, **kw):
        mainwindow = args[0]  # first argument is the ui
        current_loaded_file = mainwindow.current_loaded_file
        mainwindow.ui.reduceButton.setEnabled(True)
        str_new_window_title = "%s%s*" % (WINDOW_TITLE, current_loaded_file)
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
