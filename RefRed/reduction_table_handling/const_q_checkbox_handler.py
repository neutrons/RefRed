# standard imports

# third-party imports
from qtpy.QtCore import Qt  # type: ignore

# package imports
from RefRed.tabledata import TableData


class ConstQCheckBoxHandler:
    def __init__(self, parent=None, row: int = -1, state: Qt.CheckState = 0):
        if row == -1:
            return
        if parent is None:
            return

        self.parent = parent

        # convert checkbox state to bool
        const_q = state == Qt.Checked

        # get the stored configuration
        big_table_data: TableData = parent.big_table_data
        data = big_table_data.reflectometry_data(row)
        norm = big_table_data.normalization_data(row)
        config = big_table_data.reduction_config(row)

        if data is None:
            return

        # update the stored configuration
        config.const_q = const_q
        data.const_q = const_q
        if norm is not None:
            norm.const_q = const_q
