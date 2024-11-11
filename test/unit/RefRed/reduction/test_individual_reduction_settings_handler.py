# third party packages.
import pytest
from qtpy import QtWidgets
from unittest.mock import Mock

# RefRed imports
from RefRed.interfaces.mytablewidget import ReductionTableColumnIndex
from RefRed.main import MainGui
from RefRed.reduction.individual_reduction_settings_handler import IndividualReductionSettingsHandler


class TestIndividualReductionSettingsHandler:
    def test_get_back_range(self):
        # Mock class to customize __init__
        class MockHandler(IndividualReductionSettingsHandler):
            def __init__(self, **kwargs):
                pass

        handler = MockHandler()
        data = Mock(back=[3, 2], back2=[1, 0])
        assert handler.get_back_range(data, is_data=True) == [2, 3, 0, 1]

    def test_get_const_q(self, qtbot):
        # Mock class to customize __init__
        class MockHandler(IndividualReductionSettingsHandler):
            def __init__(self, parent, row_index, **kwargs):
                self.parent = parent
                self.row_index = row_index

        # test default is False
        app = MainGui()
        qtbot.addWidget(app)
        row = 0
        handler = MockHandler(app, row)
        assert handler.get_const_q() is False

        # test change checkbox state
        col = ReductionTableColumnIndex.CONST_Q_BINS
        checkbox = app.ui.reductionTable.cellWidget(row, col).findChild(QtWidgets.QCheckBox)
        checkbox.setChecked(True)
        assert handler.get_const_q() is True


if __name__ == '__main__':
    pytest.main([__file__])
