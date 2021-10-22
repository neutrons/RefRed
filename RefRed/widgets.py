"""
This module contains helper functions that wraps around Qt widgets
to make them more convenient to use.
Its current main purpose is to provide a uniformed way to deal with
the API breaking changes between PyQt4 and PyQt5.
"""

from typing import Tuple, Union
from qtpy import QtWidgets

# default filter is to show everything
FILTER_ALL = "All (*.*)"


def _convertSingleReturn(rst: Union[str, Tuple[str, str]]) -> Tuple[str, str]:
    """
    mock the Qt5 style
    """
    if isinstance(rst, str):
        filename, selected_filter = rst, ""
    else:
        filename, selected_filter = rst

    return filename, selected_filter


def getSaveFileName(
    parent,
    caption: str,
    default_filename: str,
    filter: str = FILTER_ALL,
) -> Tuple[str, str]:
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
        filter,
    )

    # mock the Qt5 style
    return _convertSingleReturn(rst)


def getOpenFileName(
    parent, caption: str, path: str = "", filter: str = FILTER_ALL
) -> Tuple[str, str]:
    """
    Wrapper around QtWidgets.QFileDialog.getSaveFileName that returns
    the PyQt5 style output (filename and filter).
    """
    rst = QtWidgets.QFileDialog.getOpenFileName(parent, caption, path, filter)

    # mock the Qt5 style
    return _convertSingleReturn(rst)
