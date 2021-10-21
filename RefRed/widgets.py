"""
This module contains helper functions that wraps around Qt widgets
to make them more convenient to use.
Its current main purpose is to provide a uniformed way to deal with
the API breaking changes between PyQt4 and PyQt5.
"""

from typing import Tuple
from qtpy import QtWidgets


def getSaveFileName(
    parent,
    caption: str,
    default_filename:str,
    filter: str="All (*.*)",
    )->Tuple[str]:
    """
    Wrapper around QtWidgets.QFileDialog.getSaveFileName that returns
    the PyQt5 style output (filename and filter).
    """
    # NOTE:
    # Qt4 returns the filepath as a single string
    # Qt5 returns a tuple (filepath, filter)
    rst = QtWidgets.QFileDialog.getSaveFileName(
        parent,
        caption,
        default_filename,
        filter
        )
    # mock the Qt5 style
    if isinstance(rst, str):
        filename, filter = rst, ""
    else:
        filename, filter = rst
    return filename, filter
