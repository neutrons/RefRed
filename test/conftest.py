# package imports
from RefRed.main import MainGui

# 3rd-party imports
from mantid.simpleapi import config
import pytest

# standard imports
import os
from qtpy import QtCore, QtWidgets
import sys

this_module_path = sys.modules[__name__].__file__


@pytest.fixture(scope='session')
def data_server():
    r"""Object containing info and functionality for data files
    Also, it adds the data directory to the list of Mantid data directories
    """

    _options = ["datasearch.directories", "default.facility", "default.instrument"]
    _backup = {key: config[key] for key in _options}

    class _DataServe(object):
        def __init__(self):
            self._directory = os.path.join(os.path.dirname(this_module_path), 'data')
            config.appendDataSearchDir(self._directory)
            config["default.facility"] = "SNS"
            config["default.instrument"] = "REF_L"

        @property
        def directory(self):
            r"""Directory where to find the data files"""
            return self._directory

        def path_to(self, basename):
            r"""Absolute path to a data file"""
            file_path = os.path.join(self._directory, basename)
            if not os.path.isfile(file_path):
                raise IOError(f'File {basename} not found in data directory {self._directory}')
            return file_path

    yield _DataServe()
    for key, val in _backup.items():
        config[key] = val


@pytest.fixture(scope="function")
def qfiledialog_opensave(qtbot):
    r"""Enter a file name in a QFileDialog.

    :browse_button QtWidgets.QPushButton: the button that opens the QFileDialog
    :filename str: file name, only the basename. CAVEAT: If the file is to be read, the default directory of the
        QFileDialog to be opened should be the directory holding the file to be read.
    :parent QtWidgets.QWidget: the parent widget of the QFileDialog
    :lapse int: waiting time (in microseconds) for the QFileDialog to open before the file is entered.
    """

    def _qfiledialog_opensave(browse_button, filename, parent, lapse=500):
        def qfiledialog_handler():
            def handler():
                dialog = parent.findChild(QtWidgets.QFileDialog)
                line_edit = dialog.findChild(QtWidgets.QLineEdit)
                qtbot.keyClicks(line_edit, filename)
                qtbot.wait(100)
                qtbot.keyClick(line_edit, QtCore.Qt.Key_Enter)

            QtCore.QTimer.singleShot(lapse, handler)  # wait for `lapse` time, then execute `handler`

        # Lie in wait for the QFileDialog to open, then enter the file
        qfiledialog_handler()
        # open the QFileDialog
        qtbot.mouseClick(browse_button, QtCore.Qt.LeftButton)  # open the QFileDialog

    return _qfiledialog_opensave


@pytest.fixture(scope="function")
def main_gui(qtbot, data_server):
    r"""Spawn a MainGui object by loading a configuration file
    After loading the configuration, the first run-number will be plotted
    Usage:
        main_gui(configuration=data_server.path_to("some_conf.xml"), show=False)
    :configuration : absolute path to XML configuration file. Default is test/data/REF_L_188299_configuration.xml
    :show: whether to show the main window
    :return MainGUI: main window object
    """

    def _main_gui(configuration: str = data_server.path_to("REF_L_188299_configuration.xml"), show: bool = False):
        SECOND = 1000  # in miliseconds
        window = MainGui()
        qtbot.addWidget(window)
        if show:
            window.show()
        window.path_config = os.path.dirname(configuration)

        def qfiledialog_handler():
            def handler():
                dialog = window.findChild(QtWidgets.QFileDialog)
                line_edit = dialog.findChild(QtWidgets.QLineEdit)
                qtbot.keyClicks(line_edit, os.path.basename(configuration))
                qtbot.wait(0.1 * SECOND)
                qtbot.keyClick(line_edit, QtCore.Qt.Key_Enter)

            QtCore.QTimer.singleShot(0.5 * SECOND, handler)  # wait for `lapse` time, then execute `handler`

        qfiledialog_handler()
        window.load_configuration()
        # plot the first run number
        checkbox = window.ui.reductionTable.cellWidget(0, 0)
        checkbox.click()
        return window

    return _main_gui
