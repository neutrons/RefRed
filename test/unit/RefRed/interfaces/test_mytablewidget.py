# package imports
import unittest.mock as mock

import pytest

# third party packages
from qtpy.QtCore import Qt  # type: ignore

from RefRed.interfaces.mytablewidget import MyTableWidget


class Event(object):
    val = None

    def __init__(self, val=None):
        self.val = val

    def key(self):
        return self.val


class TestMyTableWidget(object):
    @mock.patch("qtpy.QtWidgets.QTableWidget.keyPressEvent")
    @mock.patch("qtpy.QtWidgets.QTableWidget.__init__")
    def test_keypress_event_no_enter_key(self, mockSuperInit, mockSuperKeyPressEvent):
        widget = MyTableWidget()
        widget.keyPressEvent(Event())
        assert mockSuperInit.called
        assert mockSuperKeyPressEvent.called

    @mock.patch("qtpy.QtWidgets.QTableWidget.keyPressEvent")
    @mock.patch("qtpy.QtWidgets.QTableWidget.__init__")
    def test_keypress_event_enter_key(self, mockSuperInit, mockSuperKeyPressEvent):
        m = mock.Mock()
        widget = MyTableWidget()
        widget.parent = m
        widget.keyPressEvent(Event(Qt.Key_Return))
        assert mockSuperInit.called
        assert not mockSuperKeyPressEvent.called
        m.table_reduction_cell_enter_pressed.assert_called()


if __name__ == "__main__":
    pytest.main([__file__])
