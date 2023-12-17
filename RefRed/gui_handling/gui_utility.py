# standard imports
from typing import List

# third party imports
from qtpy import QtWidgets
from qtpy.QtCore import Qt

# application imports
from RefRed import WINDOW_TITLE
from RefRed.interfaces.mytablewidget import ReductionTableColumIndex
from RefRed.tabledata import TableData


class GuiUtility(object):

    parent = None
    NULL_ACTIVE_ROW = -1  # fake row index when no active row found in the reduction table

    def __init__(self, parent=None):
        self.parent = parent

    def get_ipts(self, row=-1):
        if row == -1:
            return 'N/A'
        _data0 = self.parent.big_table_data.reflectometry_data(row)
        if _data0 is None:
            return 'N/A'
        return _data0.ipts

    def init_widgets_value(self):
        _gui_metadata = self.parent.gui_metadata

        # event tof bins
        _tof_bin = _gui_metadata['tof_bin']
        self.parent.ui.eventTofBins.setValue(_tof_bin)

        # q bin
        _q_bin = _gui_metadata['q_min']
        self.parent.ui.qStep.setText(str(_q_bin))

        # angle offset
        _angle_offset = "%.3f" % _gui_metadata['angle_offset']
        self.parent.ui.angleOffsetValue.setText(_angle_offset)

        # angle offset error
        _angle_offset_error = "%.3f" % _gui_metadata['angle_offset_error']
        self.parent.ui.angleOffsetError.setText(_angle_offset_error)

    def get_row_with_highest_q(self):
        big_table_data: TableData = self.parent.big_table_data
        index = 0
        _lrdata = big_table_data.reduction_config(index)
        while _lrdata is not None:
            _lrdata = big_table_data.reduction_config(index + 1)
            index += 1
        return index - 1

    def is_row_with_highest_q(self):
        row_selected = self.get_current_table_reduction_check_box_checked()
        big_table_data = self.parent.big_table_data
        if big_table_data[row_selected + 1, 0] is None:
            return True
        return False

    def data_norm_tab_widget_row_to_display(self):
        return self.parent.current_table_reduction_row_selected

    def get_current_table_reduction_row_selected(self):
        return int(self.parent.ui.reductionTable.currentRow())

    def get_current_table_reduction_column_selected(self):
        return int(self.parent.ui.reductionTable.currentColumn())

    def get_current_table_reduction_check_box_checked(self) -> int:
        r"""Find the active row in the reduction table, understood as the row having the checkbox enabled.

        Returns
        -------
        Row index, or `NULL_ACTIVE_ROW` if no row is active
        """
        column_index = int(ReductionTableColumIndex.PLOTTED)
        for row_index in range(self.parent.REDUCTIONTABLE_MAX_ROWCOUNT):
            check_box: QtWidgets.QCheckBox = self.parent.ui.reductionTable.cellWidget(row_index, column_index)
            if check_box.checkState() == Qt.Checked:
                return row_index
        return self.NULL_ACTIVE_ROW

    def get_all_rows(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        all_rows = []
        big_table_data = self.parent.big_table_data
        for _row in range(nbr_row):
            _lrdata = big_table_data[_row, 0]
            if _lrdata is None:
                return all_rows
            all_rows.append(_row)
        return all_rows

    def get_other_row_with_same_run_number_as_row(
        self, row: int = 0, is_data: bool = False, auto_mode: bool = False
    ) -> List[int]:
        r"""Find rows sharing the same run number as that of the input `row_index`

        Parameters
        ----------
        row
            The row number for which to find other rows with the same run number. Default is 0.
        is_data
            Flag indicating if the row represents reflectometry data (`True) or direct beam data (`False`).
        auto_mode
            TODO: add docstring here
        """

        def get_norm_runnumber(table_row_index: int) -> str:
            r"""run number of the direct beam run stored in row `index` of the reduction table"""
            table_column_index = int(ReductionTableColumIndex.NORM_RUN)
            return str(self.parent.ui.reductionTable.item(table_row_index, table_column_index).text())

        all_rows = [row]
        if is_data:  # there can be only one reflectometry (data) entry in the reduction table for any given run number
            return all_rows

        if self.parent.ui.TOFmanualApplyOnlyToRow.isChecked() and auto_mode is False:  # TODO: explain this
            return all_rows

        # Scan the direct beam runs (normalization runs) for their run number (guaranteed here that `is_data` == False)
        ref_runnumber = get_norm_runnumber(row)
        for row_index in range(self.parent.ui.reductionTable.rowCount()):
            if row_index == row:
                continue  # avoid counting it twice, since `row` already in `all_rows`
            if get_norm_runnumber(row_index) == ref_runnumber:
                all_rows.append(row_index)
        all_rows.sort()
        return all_rows

    def get_data_norm_tab_selected(self):
        return self.parent.ui.dataNormTabWidget.currentIndex()

    def is_data_tab_selected(self):
        if self.get_data_norm_tab_selected() == 0:
            return True
        return False

    def is_auto_tof_range_radio_button_selected(self):
        return self.parent.ui.dataTOFautoMode.isChecked()

    def set_auto_tof_range_radio_button(self, status=True):
        self.parent.ui.dataTOFautoMode.setChecked(status)
        self.parent.ui.dataTOFmanualMode.setChecked(not status)
        self.set_auto_tof_range_widgets(status=status)

    def set_auto_tof_range_widgets(self, status=True):
        self.parent.ui.TOFmanualFromLabel.setEnabled(not status)
        self.parent.ui.TOFmanualFromValue.setEnabled(not status)
        self.parent.ui.TOFmanualFromUnitsValue.setEnabled(not status)
        self.parent.ui.TOFmanualToValue.setEnabled(not status)
        self.parent.ui.TOFmanualToLabel.setEnabled(not status)
        self.parent.ui.TOFmanualToUnitsValue.setEnabled(not status)
        self.parent.ui.TOFmanualApplyOnlyToRow.setEnabled(not status)

    def clear_table(self, table_ui):
        nbr_row = table_ui.rowCount()
        for _row in range(nbr_row):
            table_ui.removeRow(_row)
            table_ui.insertRow(_row)

    def clear_reductionTable(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")

    def reductionTable_nbr_row(self):
        big_table_data = self.parent.big_table_data
        for _index_row, _ldata in enumerate(big_table_data[:, 0]):
            if _ldata is None:
                return _index_row
        return _index_row

    def new_config_file_loaded(self, config_file_name=None):
        self.parent.current_loaded_file = config_file_name
        dialog_title = WINDOW_TITLE + self.parent.current_loaded_file
        self.parent.setWindowTitle(dialog_title)

    def gui_has_been_modified(self):
        dialog_title = WINDOW_TITLE + self.parent.current_loaded_file
        new_dialog_title = dialog_title + '*'
        self.parent.setWindowTitle(new_dialog_title)

    def gui_not_modified(self):
        dialog_title = WINDOW_TITLE + self.parent.current_loaded_file
        new_dialog_title = dialog_title
        self.parent.setWindowTitle(new_dialog_title)

    def get_reduced_yaxis_type(self):
        if self.parent.ui.RvsQ.isChecked():
            return 'RvsQ'
        else:
            return 'RQ4vsQ'

    def getStitchingType(self):
        """
        return the type of stitching selected
        can be either 'auto', 'manual' or 'absolute'
        """
        if self.parent.ui.absolute_normalization_button.isChecked():
            return 'absolute'
        elif self.parent.ui.auto_stitching_button.isChecked():
            return 'auto'
        else:
            return 'manual'
