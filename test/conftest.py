# standard imports
import os
from qtpy import QtCore, QtWidgets
import sys

# 3rd-party imports
from mantid.simpleapi import config
import pytest


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
            if os.path.isfile(file_path) is False:
                raise FileNotFoundError(f"File {basename} not found in data directory {self._directory}")  # noqa E713
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


@pytest.fixture
def file_finder_find_runs(data_server):
    """Fixture to add as side effect for mock of FileFinder.findRuns to locate runs in the test data directory

    Usage:
    @mock.patch("RefRed.calculations.locate_list_run.FileFinder.findRuns")
    def test_update_reduction_table(mock_file_finder_find_runs, file_finder_find_runs):
        mock_file_finder_find_runs.side_effect = file_finder_find_runs
    :return function: function to add as side effect to mock of FileFinder.findRuns
    """

    def _file_finder_find_runs(file_hint: str):
        """Get path to file in test data directory"""
        return data_server.path_to(f"{file_hint}.nxs.h5")

    return _file_finder_find_runs
