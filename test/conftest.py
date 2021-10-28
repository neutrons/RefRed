# 3rd-party imports
from mantid.simpleapi import config
import pytest

# standard imports
import os
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
                raise IOError('File {basename} not found in data directory {self._directory}')
            return file_path

    yield _DataServe()
    for key, val in _backup.items():
        config[key] = val
