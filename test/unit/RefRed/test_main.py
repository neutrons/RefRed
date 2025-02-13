import unittest.mock as mock

import pytest
from qtpy import QtCore, QtWidgets  # type: ignore

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
        self,
        mockMainWindowInit,
        mockLoadUI,
        mockInitializeGui,
        mockFileLoadedSignal,
        mockLoadConfiguration,
    ):
        parent = mock.Mock()
        mainGui = MainGui(parent=parent)
        mainGui.load_configuration()
        mockLoadConfiguration.assert_called()

    # Deadtime Settings tests

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

    # Instrument Settings tests

    def test_instrument_settings_checked(self, qtbot):
        """Test the toggle_instrument_settings function when the checkbox is checked."""
        # Ensure checkbox starts unchecked
        self.app.ui.instrument_settings_entry.applyCheckBox.setChecked(False)
        # Simulate checking the checkbox
        qtbot.mouseClick(self.app.ui.instrument_settings_entry.applyCheckBox, QtCore.Qt.LeftButton)
        # Assert that the apply_instrument_settings attribute is now True
        assert self.app.instrument_settings.apply_instrument_settings is True

    def test_instrument_settings_unchecked(self, qtbot):
        """Test the toggle_instrument_settings function when the checkbox is unchecked."""
        # Ensure checkbox starts checked
        self.app.ui.instrument_settings_entry.applyCheckBox.setChecked(True)
        # Simulate unchecking the checkbox
        qtbot.mouseClick(self.app.ui.instrument_settings_entry.applyCheckBox, QtCore.Qt.LeftButton)
        # Assert that the apply_instrument_settings attribute is now False
        assert self.app.instrument_settings.apply_instrument_settings is False

    def test_show_instrument_settings_default_values(self, monkeypatch):
        main_gui = self.app  # endow closure environment to MockInstrumentSettingsDialog

        class MockInstrumentSettingsDialog:
            def __init__(self, parent=None):
                r"""Mocking the InstrumentSettingsDialog to return default values without user interaction"""
                self.options = {
                    "source_detector_distance": main_gui.instrument_settings.source_detector_distance,
                    "sample_detector_distance": main_gui.instrument_settings.sample_detector_distance,
                    "num_x_pixels": main_gui.instrument_settings.num_x_pixels,
                    "num_y_pixels": main_gui.instrument_settings.num_y_pixels,
                    "pixel_width": main_gui.instrument_settings.pixel_width,
                    "xi_reference": main_gui.instrument_settings.xi_reference,
                    "s1_sample_distance": main_gui.instrument_settings.s1_sample_distance,
                }

            def exec_(self):
                return QtWidgets.QDialog.Accepted

            def set_state(
                self,
                source_detector_distance,
                sample_detector_distance,
                num_x_pixels,
                num_y_pixels,
                pixel_width,
                xi_reference,
                s1_sample_distance,
            ):
                self.options["source_detector_distance"] = source_detector_distance
                self.options["sample_detector_distance"] = sample_detector_distance
                self.options["num_x_pixels"] = num_x_pixels
                self.options["num_y_pixels"] = num_y_pixels
                self.options["pixel_width"] = pixel_width
                self.options["xi_reference"] = xi_reference
                self.options["s1_sample_distance"] = s1_sample_distance

        monkeypatch.setattr("RefRed.main.InstrumentSettingsDialog", MockInstrumentSettingsDialog)
        self.app.show_instrument_settings()
        assert self.app.instrument_settings.source_detector_distance == 15.75
        assert self.app.instrument_settings.sample_detector_distance == 1.83
        assert self.app.instrument_settings.num_x_pixels == 256
        assert self.app.instrument_settings.num_y_pixels == 304
        assert self.app.instrument_settings.pixel_width == 0.70
        assert self.app.instrument_settings.xi_reference == 445
        assert self.app.instrument_settings.s1_sample_distance == 1.485

    def test_show_instrument_settings_updated_values(self, monkeypatch):
        # endow closure environment to MockInstrumentSettingsDialog
        new_source_detector_distance = 1.0
        new_sample_detector_distance = 2.0
        new_num_x_pixels = 3
        new_num_y_pixels = 4
        new_pixel_width = 5.0
        new_xi_reference = 6.0
        new_s1_sample_distance = 7.0

        class MockInstrumentSettingsDialog:
            def __init__(self, parent=None):
                r"""Mocking the InstrumentSettingsDialog to return default values without user interaction"""
                self.options = {
                    "source_detector_distance": new_source_detector_distance,
                    "sample_detector_distance": new_sample_detector_distance,
                    "num_x_pixels": new_num_x_pixels,
                    "num_y_pixels": new_num_y_pixels,
                    "pixel_width": new_pixel_width,
                    "xi_reference": new_xi_reference,
                    "s1_sample_distance": new_s1_sample_distance,
                }

            def exec_(self):
                return QtWidgets.QDialog.Accepted

            def set_state(
                self,
                source_detector_distance,
                sample_detector_distance,
                num_x_pixels,
                num_y_pixels,
                pixel_width,
                xi_reference,
                s1_sample_distance,
            ):
                pass

        monkeypatch.setattr("RefRed.main.InstrumentSettingsDialog", MockInstrumentSettingsDialog)
        self.app.show_instrument_settings()
        assert self.app.instrument_settings.source_detector_distance == new_source_detector_distance
        assert self.app.instrument_settings.sample_detector_distance == new_sample_detector_distance
        assert self.app.instrument_settings.num_x_pixels == new_num_x_pixels
        assert self.app.instrument_settings.num_y_pixels == new_num_y_pixels
        assert self.app.instrument_settings.pixel_width == new_pixel_width
        assert self.app.instrument_settings.xi_reference == new_xi_reference
        assert self.app.instrument_settings.s1_sample_distance == new_s1_sample_distance


if __name__ == "__main__":
    pytest.main([__file__])
