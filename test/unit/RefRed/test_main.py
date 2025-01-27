# standard imports
import unittest.mock as mock

# third-party imports
import pytest
from qtpy import QtCore, QtWidgets  # type: ignore

# RefRed imports
from RefRed.main import MainGui


class TestMainGui:
    @pytest.fixture(autouse=True)
    def setup_class(self, qtbot):
        self.app = MainGui()
        qtbot.addWidget(self.app)

    def test_init(self):
        assert "Liquids Reflectometer Reduction" in self.app.windowTitle()

    def test_run_reduction_button(self):
        assert self.app.run_reduction_button() is None

    @mock.patch("RefRed.main.MainGui.file_loaded_signal")
    @mock.patch("RefRed.main.InitializeGui")
    @mock.patch("RefRed.main.load_ui")
    @mock.patch("qtpy.QtWidgets.QMainWindow.__init__")
    def test_mock_init(self, mockMainWindowInit, mockLoadUI, mockInitializeGui, mockFileLoadedSignal):
        parent = mock.Mock()
        MainGui(parent=parent)
        mockMainWindowInit.assert_called()
        mockLoadUI.assert_called()
        mockInitializeGui.assert_called()
        mockFileLoadedSignal.connect.assert_called()

    @mock.patch("RefRed.main.LoadingConfiguration")
    @mock.patch("RefRed.main.MainGui.file_loaded_signal")
    @mock.patch("RefRed.main.InitializeGui")
    @mock.patch("RefRed.main.load_ui")
    @mock.patch("qtpy.QtWidgets.QMainWindow.__init__")
    def test_load_configuration(
        self, mockMainWindowInit, mockLoadUI, mockInitializeGui, mockFileLoadedSignal, mockLoadConfiguration
    ):
        parent = mock.Mock()
        mainGui = MainGui(parent=parent)
        mainGui.load_configuration()
        mockLoadConfiguration.assert_called()

    def test_apply_deadtime_update_checked(self, qtbot):
        """Test the apply_deadtime_update function when the checkbox is checked."""
        # Ensure checkbox starts unchecked
        self.app.ui.deadtime_entry.applyCheckBox.setChecked(False)
        # Simulate checking the checkbox
        qtbot.mouseClick(self.app.ui.deadtime_entry.applyCheckBox, QtCore.Qt.LeftButton)
        # Assert that the apply_deadtime attribute is now True
        assert self.app.deadtime_settings.apply_deadtime is True

    def test_apply_deadtime_update_unchecked(self, qtbot):
        """Test the apply_deadtime_update function when the checkbox is unchecked."""
        # Ensure checkbox starts checked
        self.app.ui.deadtime_entry.applyCheckBox.setChecked(True)
        # Simulate unchecking the checkbox
        qtbot.mouseClick(self.app.ui.deadtime_entry.applyCheckBox, QtCore.Qt.LeftButton)
        # Assert that the apply_deadtime attribute is now False
        assert self.app.deadtime_settings.apply_deadtime is False

    def test_show_deadtime_settings_default_values(self, monkeypatch):
        main_gui = self.app  # endow closure environment to MockDeadTimeSettingsView

        class MockDeadTimeSettingsView:
            def __init__(self, parent=None):
                r"""Mocking the DeadTimeSettingsView to return default values without user interaction"""
                self.options = {
                    "paralyzable": main_gui.deadtime_settings.paralyzable,
                    "dead_time": main_gui.deadtime_settings.dead_time,
                    "tof_step": main_gui.deadtime_settings.tof_step,
                }

            def exec_(self):
                return QtWidgets.QDialog.Accepted

            def set_state(self, paralyzable, dead_time, tof_step):
                self.options["paralyzable"] = paralyzable
                self.options["dead_time"] = dead_time
                self.options["tof_step"] = tof_step

        monkeypatch.setattr("RefRed.main.DeadTimeSettingsView", MockDeadTimeSettingsView)
        self.app.show_deadtime_settings()
        assert self.app.deadtime_settings.paralyzable is True
        assert self.app.deadtime_settings.dead_time == 4.2
        assert self.app.deadtime_settings.tof_step == 150

    def test_show_deadtime_settings_updated_values(self, monkeypatch):
        # endow closure environment to MockDeadTimeSettingsView
        new_paralyzable = False
        new_dead_time = 5.0
        new_tof_step = 200

        class MockDeadTimeSettingsView:
            def __init__(self, parent=None):
                r"""Mocking the DeadTimeSettingsView to return default values without user interaction"""
                self.options = {
                    "paralyzable": new_paralyzable,
                    "dead_time": new_dead_time,
                    "tof_step": new_tof_step,
                }

            def exec_(self):
                return QtWidgets.QDialog.Accepted

            def set_state(self, paralyzable, dead_time, tof_step):
                pass

        monkeypatch.setattr("RefRed.main.DeadTimeSettingsView", MockDeadTimeSettingsView)
        self.app.show_deadtime_settings()
        assert self.app.deadtime_settings.paralyzable == new_paralyzable
        assert self.app.deadtime_settings.dead_time == new_dead_time
        assert self.app.deadtime_settings.tof_step == new_tof_step


if __name__ == "__main__":
    pytest.main([__file__])
