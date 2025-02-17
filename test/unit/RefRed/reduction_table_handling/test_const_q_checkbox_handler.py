from unittest import mock
from unittest.mock import Mock

from qtpy.QtCore import Qt  # type: ignore

from RefRed.calculations.lr_data import LRData
from RefRed.lconfigdataset import LConfigDataset
from RefRed.reduction_table_handling.const_q_checkbox_handler import ConstQCheckBoxHandler
from RefRed.tabledata import TableData


def test_const_q_checkbox_handler():
    big_table_data = TableData(max_row_count=1)
    row = 0

    with mock.patch.object(LRData, "__init__", return_value=None):
        instance = LRData()
        big_table_data.set_reflectometry_data(row, instance)
        big_table_data.set_normalization_data(row, instance)
    big_table_data.set_reduction_config(row, LConfigDataset())

    data = big_table_data.reflectometry_data(row)
    norm = big_table_data.normalization_data(row)
    config = big_table_data.reduction_config(row)

    parent = Mock()
    parent.big_table_data = big_table_data

    ConstQCheckBoxHandler(parent, row, state=Qt.Checked)
    assert data.const_q is True
    assert norm.const_q is True
    assert config.const_q is True

    ConstQCheckBoxHandler(parent, row, state=Qt.Unchecked)
    assert data.const_q is False
    assert norm.const_q is False
    assert config.const_q is False
