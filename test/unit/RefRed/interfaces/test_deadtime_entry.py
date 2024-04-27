# third party imports
import pytest
from qtpy.QtCore import Qt  # type: ignore

# RefRed imports
from RefRed.interfaces.deadtime_entry import DeadTimeEntryPoint  # Make sure to import your class correctly


@pytest.fixture
def dead_time_entry_point(qtbot):
    widget = DeadTimeEntryPoint()
    qtbot.addWidget(widget)
    return widget


def test_initial_state(dead_time_entry_point):
    assert not dead_time_entry_point.applyCheckBox.isChecked()
    assert not dead_time_entry_point.settingsButton.isEnabled()


def test_checkbox_interaction(dead_time_entry_point, qtbot):
    # Simulate checking the checkbox
    qtbot.mouseClick(dead_time_entry_point.applyCheckBox, Qt.LeftButton)
    # Test if the checkbox is checked
    assert dead_time_entry_point.applyCheckBox.isChecked()
    # Test if the settings button is now enabled
    assert dead_time_entry_point.settingsButton.isEnabled()


def test_uncheck_checkbox(dead_time_entry_point, qtbot):
    # First, check the checkbox
    qtbot.mouseClick(dead_time_entry_point.applyCheckBox, Qt.LeftButton)
    # Now, uncheck it
    qtbot.mouseClick(dead_time_entry_point.applyCheckBox, Qt.LeftButton)
    # Test if the checkbox is unchecked
    assert not dead_time_entry_point.applyCheckBox.isChecked()
    # Test if the settings button is now disabled
    assert not dead_time_entry_point.settingsButton.isEnabled()


if __name__ == '__main__':
    pytest.main([__file__])
