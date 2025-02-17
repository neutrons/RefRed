import pytest
from qtpy import QtCore, QtWidgets  # type: ignore

from RefRed.sf_calculator.sf_calculator import SFCalculator


class TestSFCalculator:
    @pytest.fixture(autouse=True)
    def setup_class(self, qtbot):
        self.app = SFCalculator()
        qtbot.addWidget(self.app)

    def test_apply_deadtime_update_checked(self, qtbot):
        """Test the apply_deadtime_update function when the checkbox is checked."""
        # Ensure checkbox starts unchecked
        self.app.ui.deadtime_entry.applyCheckBox.setChecked(False)
        # Simulate checking the checkbox
        qtbot.mouseClick(self.app.ui.deadtime_entry.applyCheckBox, QtCore.Qt.LeftButton)
        # Assert that the apply_deadtime attribute is now True
        assert self.app.apply_deadtime is True

    def test_apply_deadtime_update_unchecked(self, qtbot):
        """Test the apply_deadtime_update function when the checkbox is unchecked."""
        # Ensure checkbox starts checked
        self.app.ui.deadtime_entry.applyCheckBox.setChecked(True)
        # Simulate unchecking the checkbox
        qtbot.mouseClick(self.app.ui.deadtime_entry.applyCheckBox, QtCore.Qt.LeftButton)
        # Assert that the apply_deadtime attribute is now False
        assert self.app.apply_deadtime is False

    def test_show_dead_time_dialog_default_values(self, monkeypatch):
        calculator = self.app  # endow closure environment to MockDeadTimeSettingsView

        class MockDeadTimeSettingsView:
            def __init__(self, parent=None):
                r"""Mocking the DeadTimeSettingsView to return default values without user interaction"""
                self.options = {
                    "paralyzable": calculator.paralyzable_deadtime,
                    "dead_time": calculator.deadtime_value,
                    "tof_step": calculator.deadtime_tof_step,
                }

            def exec_(self):
                return QtWidgets.QDialog.Accepted

            def set_state(self, paralyzable, dead_time, tof_step):
                self.options["paralyzable"] = paralyzable
                self.options["dead_time"] = dead_time
                self.options["tof_step"] = tof_step

        monkeypatch.setattr("RefRed.sf_calculator.sf_calculator.DeadTimeSettingsView", MockDeadTimeSettingsView)
        self.app.show_dead_time_dialog()
        assert self.app.paralyzable_deadtime is True
        assert self.app.deadtime_value == 4.2
        assert self.app.deadtime_tof_step == 150

    def test_show_dead_time_dialog_updated_values(self, monkeypatch):
        # endow closure environment to MockDeadTimeSettingsView
        new_paralyzable = False
        new_dead_time = 5.0
        new_tof_step = 200

        class MockDeadTimeSettingsView:
            def __init__(self, parent=None):
                r"""Mocking the DeadTimeSettingsView to return values without user interaction"""
                self.options = {"paralyzable": new_paralyzable, "dead_time": new_dead_time, "tof_step": new_tof_step}

            def exec_(self):
                return QtWidgets.QDialog.Accepted

            def set_state(self, paralyzable, dead_time, tof_step):
                pass

        monkeypatch.setattr("RefRed.sf_calculator.sf_calculator.DeadTimeSettingsView", MockDeadTimeSettingsView)
        self.app.show_dead_time_dialog()
        assert self.app.paralyzable_deadtime == new_paralyzable
        assert self.app.deadtime_value == new_dead_time
        assert self.app.deadtime_tof_step == new_tof_step


if __name__ == "__main__":
    pytest.main([__file__])
