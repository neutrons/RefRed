import pytest
from unittest import mock

import qtpy.QtWidgets

import RefRed.sf_calculator.sf_calculator
from RefRed.sf_calculator.reduction_sf_calculator import ReductionSfCalculator
from RefRed.sf_calculator.sf_calculator import SFCalculator
import numpy as np
from qtpy.QtWidgets import QTableWidgetItem, QTableWidget


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

    return MockQSpinBox(cell_value)


# FIXME NOT WORKING
# @mock.patch('qtpy.QtWidgets.QTableWidget.rowCount', side_effect=mock_table_row_count)
# def test_init_reduction_sft_calculator(tableWidgetRowCount):
#     # tableWidgetRowCount.side_effect = mock_table_row_count


@mock.patch('qtpy.QtWidgets.QApplication.processEvents')
def test_init_reduction_sft_calculator(sf_process_events):
    # set up mocks
    sf_gui = mock.Mock()
    sf_gui.tableWidget = mock.Mock()

    sf_gui.tableWidget.rowCount = mock.MagicMock(side_effect=mock_table_row_count)
    sf_gui.tableWidget.cellWidget = mock.MagicMock(side_effect=mock_table_row_cell)
    sf_gui.tableWidget.item = mock.MagicMock(side_effect=mock_table_row_item)

    sf_gui.incidentMediumComboBox = MockQComboBox('air')
    sf_gui.sfFileNameLabel = MockQLabel()
    sf_gui.sfFileNameLabel.setText('/tmp/testscale.cfg')

    import mantid.simpleapi
    mantid.simpleapi.LRScalingFactors = mock.Mock(side_effect=mock_lr_scaling_factor)

    # Start
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

    assert sf_process_events.iscalled


def old_test_class_reduction_sf_calculator(mocker):
    """Test class ReductionSfCalculator
    """
    # Set mockers
    set_mockers(mocker)

    # Set up mocking class and etc.
    sf_gui = SFCalculator()

    # Initialize
    test_reducer = ReductionSfCalculator(sf_gui, False, test_mode=True)
    # Validation
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


def set_mockers(mocker_fixture):
    mocker_fixture.patch('RefRed.sf_calculator.sf_calculator.SFCalculator.__init__',
                         MockSFCalculatorGui.init_sf_gui)
    mocker_fixture.patch('RefRed.sf_calculator.sf_calculator.SFCalculator.updateProgressBar',
                         MockSFCalculatorGui.sf_update_progress_bar)
    mocker_fixture.patch('RefRed.sf_calculator.sf_calculator.SFCalculator.displayConfigFile',
                         MockSFCalculatorGui.sf_display_config)
    mocker_fixture.patch('qtpy.QtWidgets.QFileDialog.getSaveFileName', MockSFCalculatorGui.qt_get_save_file_name)
    mocker_fixture.patch('qtpy.QtWidgets.QTableWidget.__init__', MockSFCalculatorGui.table_init)
    mocker_fixture.patch('qtpy.QtWidgets.QTableWidget.rowCount', MockSFCalculatorGui.row_count)
    mocker_fixture.patch('qtpy.QtWidgets.QTableWidget.item', MockSFCalculatorGui.table_item)
    mocker_fixture.patch('qtpy.QtWidgets.QTableWidget.cellWidget', MockSFCalculatorGui.table_cell)
    mocker_fixture.patch('qtpy.QtWidgets.QApplication.processEvents', MockSFCalculatorGui.process_events)

    mocker_fixture.patch('mantid.simpleapi.LRScalingFactors', mock_lr_scaling_factor)


class GoldValues:
    gold_table_setting = np.array([
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
        [184989.0, 3.0, 4.25, 135.0, 147.0, 132.0, 150.0, 9.97, 23.25]])

    gold_index_same_lambda = np.array([
        [0., 0.],
        [1., 1.],
        [2., 2.],
        [3., 5.],
        [6., 14.]])

    gold_nbr_scripts = 5


class MockSFCalculatorGui:
    """
    Mocking SF_gui
    """
    def init_sf_gui(self):
        """Mock SF_Calculator's constructor
        Note:
        # QComboBox
        # from qtpy.QtWidgets import QComboBox
        # self.incidentMediumComboBox = QComboBox()
        # test/unit/RefRed/sf_calculator/test_reduction_sf_calculator.py Fatal Python error: Aborted

        # Qlabel
        # from qtpy.QtWidgets import QLabel
        # self.sfFileNameLabel = QLabel()
        """
        self.name = 'Mock SF GUI'
        self.tableWidget = QTableWidget()
        self.incidentMediumComboBox = MockQComboBox('air')
        self.sfFileNameLabel = MockQLabel()
        self.sfFileNameLabel.setText('/tmp/testscale.cfg')

    def sf_display_config(self, file_name):
        """Mock SF_Calculator.displayConfigFile()
        """
        assert isinstance(file_name, str)

    def sf_update_progress_bar(self, progress):
        return

    def qt_get_save_file_name(parent, name, path, filter):
        return 'whatever.h5'

    def row_count(self) -> int:
        """Mock method QTableWidget.rowCount()
        """
        return GoldValues.gold_table_setting.shape[0]

    def table_init(self):
        return

    def table_item(self, row, col):
        """Mock method QTableWidget.item(row, col)

        Parameters
        ----------
        row: int
            row number
        col: int
            column number

        Returns
        -------
        QTableWidgetItem
            table widget time

        """
        # Map the real column to column that in the gold data
        index_col = [0, 1, 5, 10, 11, 12, 13, 14, 15]
        try:
            real_col = index_col.index(col)
        except ValueError:
            assert False, f'Column {col} content are not float/int'

        cell_value = str(GoldValues.gold_table_setting[row, real_col])

        return QTableWidgetItem(cell_value)

    def table_cell(self, row: int, col: int):
        """Mock QTableWidget.cell(row, col)

        Note: Not working!
        ..  from qtpy.QtWidgets import QSpinBox
        ..  spin_box = QSpinBox()
        causing test/unit/RefRed/sf_calculator/test_reduction_sf_calculator.py Fatal Python error: Aborted

        Returns
        -------
        MockQSpinBox
            mocked QSpinBox
        """
        # Map the real column to column that in the gold data
        index_col = [0, 1, 5, 10, 11, 12, 13, 14, 15]
        try:
            real_col = index_col.index(col)
            cell_value = GoldValues.gold_table_setting[row, real_col]
        except ValueError:
            assert False, f'Column {col} content are not float/int'

        return MockQSpinBox(cell_value)

    @staticmethod
    def process_events():
        return


class MockQSpinBox(object):
    def __init__(self, value):
        self._value = int(value)

    def value(self):
        return self._value


class MockQComboBox(object):
    def __init__(self, text):
        self._text = text

    def currentText(self):
        return self._text


class MockQLabel(object):
    def __init__(self):
        self._text = None

    def setText(self, text):
        self._text = str(text)

    def text(self):
        return self._text


def mock_lr_scaling_factor(DirectBeamRuns, IncidentMedium, TOFRange, TOFSteps, SignalPeakPixelRange,
                           SignalBackgroundPixelRange, LowResolutionPixelRange, ScalingFactorFile):
    """Verify the input parameters are correct

    It is assumed that the mantid algorithm is correct.
    The mantid algorithm shall be tested in a separate test
    """
    if len(DirectBeamRuns) == 3:
        # first calculation
        assert DirectBeamRuns == [184978, 184979, 184980]
        assert IncidentMedium == 'air'
        assert TOFRange == [20880.0, 34170.0]
        assert TOFSteps == 200
        assert SignalPeakPixelRange == [136, 145, 136, 145, 136, 145]
        assert SignalBackgroundPixelRange == [133, 148, 133, 148, 133, 148]
        assert LowResolutionPixelRange == [0, 256, 0, 256, 0, 256]
        assert ScalingFactorFile == '/tmp/testscale.cfg'

    elif len(DirectBeamRuns) == 9:
        # second calculation
        assert DirectBeamRuns == [184981, 184982, 184983, 184984, 184985, 184986, 184987, 184988, 184989]
        assert IncidentMedium == 'air'
        assert TOFRange == [9970.0, 23250.0]
        assert TOFSteps == 200
        assert SignalPeakPixelRange == \
               [137, 145, 137, 145, 136, 145, 136, 145, 136, 145, 136, 145, 135, 147, 135, 147, 135, 147]
        assert SignalBackgroundPixelRange == \
               [134, 148, 134, 148, 133, 148, 133, 148, 133, 148, 133, 148, 132, 150, 132, 150, 132, 150]
        assert LowResolutionPixelRange == [0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256, 0, 256]
        assert ScalingFactorFile == '/tmp/testscale.cfg'

    else:
        raise RuntimeError(f'Direct beam runs: {DirectBeamRuns} is not defined')


if __name__ == '__main__':
    pytest.main([__file__])
