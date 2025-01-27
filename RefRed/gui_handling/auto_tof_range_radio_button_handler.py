from RefRed.calculations.update_reduction_table_metadata import UpdateReductionTableMetadata
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.plot.display_plots import DisplayPlots


class AutoTofRangeRadioButtonHandler(object):
    parent = None
    all_rows = []
    row = -1
    col = -1
    is_data = True

    new_tof_range = []

    def __init__(self, parent=None, enable=True):
        self.parent = parent

        self.parent.ui.dataTOFmanualLabel.setEnabled(enable)
        self.parent.ui.dataTOFautoMode.setEnabled(enable)
        self.parent.ui.dataTOFmanualMode.setEnabled(enable)
        if not enable:
            return

    def setup(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        is_auto_tof_selected = o_gui_utility.is_auto_tof_range_radio_button_selected()
        o_gui_utility.set_auto_tof_range_widgets(status=is_auto_tof_selected)

        self.row = o_gui_utility.get_current_table_reduction_check_box_checked()
        if self.row == -1:
            return

        self.all_rows = o_gui_utility.get_other_row_with_same_run_number_as_row(
            row=self.row, auto_mode=is_auto_tof_selected
        )
        self.col = o_gui_utility.get_data_norm_tab_selected()
        self.is_data = True if self.col == 0 else False

    def radio_button_handler(self):
        if self.row == -1:
            return

        o_gui_utility = GuiUtility(parent=self.parent)
        is_auto_tof_selected = o_gui_utility.is_auto_tof_range_radio_button_selected()

        big_table_data = self.parent.big_table_data
        for _row in self.all_rows:
            _data = big_table_data[_row, 0]
            _norm = big_table_data[_row, 1]
            _lconfig = big_table_data[_row, 2]

            if _data is None:
                return

            if is_auto_tof_selected:
                self.new_tof_range = _data.tof_range_auto
                _lconfig.tof_auto_flag = True
                _data.tof_range_auto_flag = True
                if _norm is not None:
                    _norm.tof_range_auto_flag = True
            else:
                self.new_tof_range = _data.tof_range_manual
                _data.tof_range_auto_flag = False
                _lconfig.tof_auto_flag = False
                if _norm is not None:
                    _norm.tof_range_auto_flag = False

            _data.tof_auto_flag = is_auto_tof_selected
            big_table_data[_row, 1] = _norm
            big_table_data[_row, 0] = _data
            self.parent.big_table_data = big_table_data

            self.replace_tof_range_displayed()
            if _row == self.row:
                self.refresh_plot()
            self.recalculate_reduction_table_metadata(row=_row)

    def recalculate_reduction_table_metadata(self, row=0):
        big_table_data = self.parent.big_table_data
        _lrdata = big_table_data[row, 0]
        _lrdata.calculate_lambda_range(self.new_tof_range)
        _lrdata.calculate_q_range()
        big_table_data[row, 0] = _lrdata
        self.parent.big_table_data = big_table_data
        UpdateReductionTableMetadata(parent=self.parent, lrdata=_lrdata, row=row)

    def line_edit_validation(self):
        if self.row == -1:
            return

        self.save_current_manual_tof_range()
        self.refresh_plot()
        for _row in self.all_rows:
            self.recalculate_reduction_table_metadata(row=_row)

    def refresh_plot(self):
        DisplayPlots(
            parent=self.parent,
            row=self.row,
            is_data=self.is_data,
            plot_yt=True,
            plot_yi=True,
            plot_it=True,
            plot_ix=False,
            refresh_reduction_table=False,
        )

    def save_current_manual_tof_range(self):
        big_table_data = self.parent.big_table_data
        _tof_range_manual = self.retrieve_tof_range_defined_by_user()
        for _col in range(2):
            for _row in self.all_rows:
                _data = big_table_data[_row, _col]
                if _data is None:
                    break
                _data.tof_range_manual = _tof_range_manual
                _data.tof_range = _tof_range_manual
                self.new_tof_range = _tof_range_manual
                big_table_data[_row, _col] = _data
        self.parent.big_table_data = big_table_data

    def save_manual_tof_range(self):
        big_table_data = self.parent.big_table_data
        for _col in range(2):
            _data = big_table_data[self.row, _col]
            _data.tof_range_auto_flag = False
            _data.tof_range_manual = self.new_tof_range
            big_table_data[self.row, _col] = _data
        self.parent.big_table_data = big_table_data

    def save_auto_tof_range(self):
        big_table_data = self.parent.big_table_data
        for _col in range(2):
            _data = big_table_data[self.row, _col]
            _data.tof_range_auto_flag = True
            big_table_data[self.row, _col] = _data
        self.parent.big_table_data = big_table_data

    def retrieve_tof_range_defined_by_user(self):
        tof1 = float(self.parent.ui.TOFmanualFromValue.text()) * 1000.0
        tof2 = float(self.parent.ui.TOFmanualToValue.text()) * 1000.0
        return [tof1, tof2]

    def replace_tof_range_displayed(self):
        tof_range = self.new_tof_range

        tof1 = "%.2f" % (tof_range[0] / 1000.0)
        tof2 = "%.2f" % (tof_range[1] / 1000.0)

        self.parent.ui.TOFmanualFromValue.setText(tof1)
        self.parent.ui.TOFmanualToValue.setText(tof2)
