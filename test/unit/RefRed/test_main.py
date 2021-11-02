# package imports
from RefRed.main import MainGui
from RefRed.interfaces import load_ui

# third party packages
from qtpy import QtWidgets
from qtpy.QtCore import Qt

import unittest.mock as mock
import pytest

class TestMainGui(object):

    @mock.patch('RefRed.main.MainGui.file_loaded_signal')
    @mock.patch('RefRed.main.InitializeGui')
    @mock.patch('RefRed.main.load_ui')
    @mock.patch('qtpy.QtWidgets.QMainWindow.__init__')
    def test_init(self, mockMainWindowInit, mockLoadUI, mockInitializeGui, mockFileLoadedSignal):        
        parent  = mock.Mock()
        mainGui = MainGui(parent = parent)
        mockMainWindowInit.assert_called()
        mockLoadUI.assert_called()
        mockInitializeGui.assert_called()
        mockFileLoadedSignal.connect.assert_called()

    @mock.patch('RefRed.main.LoadingConfiguration')
    @mock.patch('RefRed.main.MainGui.file_loaded_signal')
    @mock.patch('RefRed.main.InitializeGui')
    @mock.patch('RefRed.main.load_ui')
    @mock.patch('qtpy.QtWidgets.QMainWindow.__init__')
    def test_load_configuration(self, mockMainWindowInit, mockLoadUI, mockInitializeGui, mockFileLoadedSignal, mockLoadConfiguration):        
        parent  = mock.Mock()
        mainGui = MainGui(parent = parent)
        mainGui.load_configuration()   
        mockLoadConfiguration.assert_called()

if __name__ == '__main__':
    pytest.main([__file__])