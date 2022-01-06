from qtpy.QtCore import Qt
from RefRed.version import window_title


class GuiUtility(object):

    parent = None

    def __init__(self, parent=None):
        self.parent = parent

    def get_ipts(self, row=-1):
        big_table_data = self.parent.big_table_data
        _data0 = big_table_data[row, 0]
        if _data0 is None:
            return 'N/A'
        if row == -1:
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
        big_table_data = self.parent.big_table_data
        index = 0
        _lrdata = big_table_data[0, 2]
        while _lrdata is not None:
            _lrdata = big_table_data[index + 1, 2]
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

    def get_current_table_reduction_check_box_checked(self):
        nbr_row_table_reduction = self.parent.nbr_row_table_reduction
        for row in range(nbr_row_table_reduction):
            _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
            _state = _widget.checkState()
            if _state == Qt.Checked:
                return row
        return -1

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

    def get_other_row_with_same_run_number_as_row(self, row=0, is_data=False, auto_mode=False):
        all_rows = [row]
        if is_data:
            return all_rows

        if self.parent.ui.TOFmanualApplyOnlyToRow.isChecked() and (not auto_mode):
            return all_rows

        nbr_row = self.parent.ui.reductionTable.rowCount()
        ref_run_number = str(self.parent.ui.reductionTable.item(row, 2).text())
        for _row in range(nbr_row):
            if _row == row:
                continue
            _item = str(self.parent.ui.reductionTable.item(_row, 2).text())
            if _item == ref_run_number:
                all_rows.append(_row)
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
        dialog_title = window_title + self.parent.current_loaded_file
        self.parent.setWindowTitle(dialog_title)

    def gui_has_been_modified(self):
        dialog_title = window_title + self.parent.current_loaded_file
        new_dialog_title = dialog_title + '*'
        self.parent.setWindowTitle(new_dialog_title)

    def gui_not_modified(self):
        dialog_title = window_title + self.parent.current_loaded_file
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
