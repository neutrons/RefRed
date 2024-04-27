# third party imports
import pytest
from qtpy.QtCore import Qt

# RefRed imports
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
        qtbot.mouseClick(self.app.ui.deadtime_entry.applyCheckBox, Qt.LeftButton)
        # Assert that the apply_deadtime attribute is now True
        assert self.app.apply_deadtime is True

    def test_apply_deadtime_update_unchecked(self, qtbot):
        """Test the apply_deadtime_update function when the checkbox is unchecked."""
        # Ensure checkbox starts checked
        self.app.ui.deadtime_entry.applyCheckBox.setChecked(True)
        # Simulate unchecking the checkbox
        qtbot.mouseClick(self.app.ui.deadtime_entry.applyCheckBox, Qt.LeftButton)
        # Assert that the apply_deadtime attribute is now False
        assert self.app.apply_deadtime is False


if __name__ == '__main__':
    pytest.main([__file__])
