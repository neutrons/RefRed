# standard imports
from unittest import mock

# third-party imports
import lr_reduction.scaling_factors.LRScalingFactors
import numpy as np
import pytest
import qtpy
import qtpy.QtWidgets
from qtpy.QtWidgets import QTableWidgetItem

# RefRed imports
from RefRed.main import MainGui
from RefRed.sf_calculator.reduction_sf_calculator import ReductionSfCalculator


def mock_table_row_count(*args, **kwargs):
    return GoldValues.gold_table_setting.shape[0]


def mock_table_row_item(row, col):
    # Map the real column to column that in the gold data
    index_col = [0, 1, 5, 10, 11, 12, 13, 14, 15]
    try:
        real_col = index_col.index(col)
    except ValueError:
        assert False, f'Column {col} content are not float/int'

    cell_value = str(GoldValues.gold_table_setting[row, real_col])

    return QTableWidgetItem(cell_value)


def mock_table_row_cell(row, col):
    # Map the real column to column that in the gold data
    index_col = [0, 1, 5, 10, 11, 12, 13, 14, 15]
    try:
        real_col = index_col.index(col)
        cell_value = GoldValues.gold_table_setting[row, real_col]
    except ValueError:
        assert False, f'Column {col} content are not float/int'

    spin_box_instance = qtpy.QtWidgets.QSpinBox()
    spin_box_instance.setValue(int(cell_value))

    return spin_box_instance


@mock.patch('RefRed.sf_calculator.reduction_sf_calculator.QApplication.processEvents')
def test_init_reduction_sf_calculator(processEvents_mock, qtbot):
    """Test reduction sf calculator"""
    main_app = MainGui()
    qtbot.addWidget(main_app)

    # Mock SF calculation
    sf_gui = mock.Mock()
    sf_gui.tableWidget = mock.Mock()

    sf_gui.tableWidget.rowCount = mock.MagicMock(side_effect=mock_table_row_count)
    sf_gui.tableWidget.cellWidget = mock.MagicMock(side_effect=mock_table_row_cell)
    sf_gui.tableWidget.item = mock.MagicMock(side_effect=mock_table_row_item)

    sf_gui.incidentMediumComboBox = qtpy.QtWidgets.QComboBox()
    sf_gui.incidentMediumComboBox.addItem('air')
    sf_gui.incidentMediumComboBox.setCurrentIndex(0)
    sf_gui.sfFileNameLabel = qtpy.QtWidgets.QLabel('/tmp/testscale.cfg')

    # Set up mock for mantid LRScalingFactors
    lr_reduction.scaling_factors.LRScalingFactors.LRScalingFactors = mock.Mock(side_effect=mock_lr_scaling_factor)

    # Initialize
    test_reducer = ReductionSfCalculator(sf_gui, False, True)
    assert test_reducer

    # Test: collect_table_information()
    test_reducer.collect_table_information()
    np.testing.assert_allclose(test_reducer.table_settings, GoldValues.gold_table_setting)

    # Test: self.generateIndexSameLambda()
    from_to_index_same_lambda = test_reducer.generateIndexSameLambda()
    np.testing.assert_allclose(from_to_index_same_lambda, GoldValues.gold_index_same_lambda)
    assert test_reducer.nbr_scripts == GoldValues.gold_nbr_scripts

    # Test: _handle_request
    test_reducer._handle_request()

    # Test
    assert processEvents_mock.iscalled


class GoldValues:
    gold_table_setting = np.array(
        [
            [184975.0, 0.0, 15.0, 136.0, 144.0, 133.0, 147.0, 51.98, 65.27],
            [184976.0, 0.0, 12.39, 136.0, 145.0, 133.0, 148.0, 41.76, 55.05],
            [184977.0, 0.0, 9.74, 136.0, 145.0, 133.0, 148.0, 31.42, 44.71],
            [184978.0, 0.0, 7.04, 136.0, 145.0, 133.0, 148.0, 20.88, 34.17],
            [184979.0, 1.0, 7.04, 136.0, 145.0, 133.0, 148.0, 20.88, 34.17],
            [184980.0, 1.0, 7.04, 136.0, 145.0, 133.0, 148.0, 20.88, 34.17],
            [184981.0, 0.0, 4.25, 137.0, 145.0, 134.0, 148.0, 9.97, 23.25],
            [184982.0, 1.0, 4.25, 137.0, 145.0, 134.0, 148.0, 9.97, 23.25],
            [184983.0, 1.0, 4.25, 136.0, 145.0, 133.0, 148.0, 9.97, 23.25],
            [184984.0, 2.0, 4.25, 136.0, 145.0, 133.0, 148.0, 9.97, 23.25],
            [184985.0, 2.0, 4.25, 136.0, 145.0, 133.0, 148.0, 9.97, 23.25],
            [184986.0, 2.0, 4.25, 136.0, 145.0, 133.0, 148.0, 9.97, 23.25],
            [184987.0, 2.0, 4.25, 135.0, 147.0, 132.0, 150.0, 9.97, 23.25],
            [184988.0, 3.0, 4.25, 135.0, 147.0, 132.0, 150.0, 9.97, 23.25],
            [184989.0, 3.0, 4.25, 135.0, 147.0, 132.0, 150.0, 9.97, 23.25],
        ]
    )

    gold_index_same_lambda = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 5.0], [6.0, 14.0]])

    gold_nbr_scripts = 5


def mock_lr_scaling_factor():
    class Algo:
        def PyInit(self):
            return None

        def setProperty(self, key, value):
            assert key in {
                'DirectBeamRuns',
                'IncidentMedium',
                'Attenuators',
                'TOFRange',
                'TOFSteps',
                'SignalPeakPixelRange',
                'SignalBackgroundPixelRange',
                'LowResolutionPixelRange',
                'ScalingFactorFile',
                'UseDeadTimeCorrection',
                'ParalyzableDeadTime',
                'DeadTime',
                'DeadTimeTOFStep',
            }

        def PyExec(self):
            return None

    return Algo()


if __name__ == '__main__':
    pytest.main([__file__])
