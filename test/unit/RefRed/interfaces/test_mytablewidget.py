# package imports
from RefRed.interfaces.mytablewidget import MyTableWidget

# third party packages
from qtpy import QtWidgets
from qtpy.QtCore import Qt

import mock
import pytest

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
        assert m.table_reduction_cell_enter_pressed().assert_called()

if __name__ == '__main__':
    pytest.main([__file__])