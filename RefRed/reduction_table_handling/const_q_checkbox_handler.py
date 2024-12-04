# standard imports

# third-party imports
from qtpy.QtCore import Qt  # type: ignore

# package imports
from RefRed.tabledata import TableData


class ConstQCheckBoxHandler:
    """
    Handler for the constant Q binning checkbox in the reduction table.

    This class updates the `const_q` attribute in the reflectometry data, normalization data, and
    reduction configuration based on the state of the constant Q binning checkbox.
    """

    def __init__(self, parent=None, row: int = -1, state: Qt.CheckState = 0):
        """
        Initializes the handler and updates the stored configuration based on the checkbox state.
            - Converts the checkbox state to a boolean value.
            - Retrieves the reflectometry data, normalization data, and reduction configuration from the parent.

        Parameters
        ----------
        parent
            The parent object containing the big table data
        row
            The row index in the table
        state
            The state of the checkbox
        """
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
