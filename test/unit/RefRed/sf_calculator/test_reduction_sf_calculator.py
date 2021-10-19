import pytest
from RefRed.sf_calculator.reduction_sf_calculator import ReductionSfCalculator
import numpy as np


def test_class_reduction_sf_calculator():
    """Test class ReductionSfCalculator
    """
    # Set up mocking class and etc.
    mock_sf_gui = MockSFGui()
    test_script_file_name = 'whatever.h5'

    # Init
    test_reducer = ReductionSfCalculator(mock_sf_gui, test_script_file_name, test_mode=True)

    # Validation
    assert test_reducer

    # Validate
    assert test_reducer.table_settings  # np.assert_all

    #
    from_to_index_same_lambda = test_reducer.generateIndexSameLambda()
    assert from_to_index_same_lambda
    assert test_reducer.nbr_scripts


class MockSFGui(object):
    """
    Mocking SF_gui
    """
    def __init__(self):
        """
        constructor
        """
        return


def create_mock_gui():
    """

    Returns
    -------

    """
    table_content = np.array([
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
    ])

    table_widgets = MockTableWidget()
    index_cols = [0, 1, 5, 10, 11, 12, 13, 14, 15]
    table_widgets.set_contents(table_content, index_cols)


class MockTableWidget(object):
    """
    Mocking table widget in SF GUI
    """
    def __init__(self):
        self._cells = None

    def rowCount(self) -> int:
        return 0

    def cellWidget(self, row_index, column_index):
        return self._cells[row_index][column_index]


class MockCellWidget(object):
    """

    """
    def __init__(self):
        self._value = None

    def value(self):
        return self._value

    def text(self):
        return str(self._value)


if __name__ == '__main__':
    pytest.main([__file__])
