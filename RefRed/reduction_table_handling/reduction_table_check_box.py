# standard imports

# third-party imports
import numpy as np
from qtpy.QtCore import Qt

# package imports
from RefRed.gui_handling.auto_tof_range_radio_button_handler import AutoTofRangeRadioButtonHandler
from RefRed.gui_handling.update_plot_widget_status import UpdatePlotWidgetStatus
from RefRed.plot.background_settings import backgrounds_settings
from RefRed.plot.clear_plots import ClearPlots
from RefRed.plot.display_plots import DisplayPlots


class ReductionTableCheckBox(object):

    BOX_CHECKED = 2  # value emited by qtpy.QtWidgets.QCheckBox.stateChanged when checked
    row_selected = -1
    prev_row_selected = -1
    size_check_box_state_table = None
    parent = None
    _reduction_table_check_box_state = None

    def __init__(self, parent=None, row_selected=-1):
        if row_selected == -1:
            return
        if parent is None:
            return

        self.prev_row_selected = parent.prev_table_reduction_row_selected
        self.parent = parent
        self.row_selected = row_selected
        self.handle_check_boxes_single_selection()
        self.launch_update_of_plot()
        self.update_gui()

    def handle_check_boxes_single_selection(self):
        if self.row_selected == self.parent.current_table_reduction_row_selected:
            self.parent.current_table_reduction_row_selected = -1
        else:
            self.parent.current_table_reduction_row_selected = self.row_selected

        if self.row_selected == self.prev_row_selected:
            pass
        else:
            _reduction_table_check_box_state = self.parent.reduction_table_check_box_state

            self.size_check_box_state_table = len(_reduction_table_check_box_state)
            old_check_box_state = _reduction_table_check_box_state[self.row_selected]
            _reduction_table_check_box_state = np.zeros((self.size_check_box_state_table), dtype=bool)

            _reduction_table_check_box_state[self.row_selected] = not old_check_box_state
            self._reduction_table_check_box_state = _reduction_table_check_box_state

            self.update_state_of_all_checkboxes()
            self.parent.reduction_table_check_box_state = _reduction_table_check_box_state

            self.parent.prev_table_reduction_row_selected = self.row_selected

    def launch_update_of_plot(self):
        _row_selected = self.row_selected
        _is_data_selected = self.is_data_tab_selected()
        if self.is_row_selected_checked(_row_selected):
            backgrounds_settings.update_from_table(_row_selected, is_data=_is_data_selected)
            DisplayPlots(parent=self.parent, row=self.row_selected, is_data=self.is_data_tab_selected())
        else:
            update_obj = UpdatePlotWidgetStatus(parent=self.parent)
            update_obj.disable_all()
            ClearPlots(self.parent, is_data=_is_data_selected, is_norm=not (_is_data_selected), all_plots=True)

    def update_gui(self):
        """will update widgets such as TOF auto/manual"""
        _row_selected = self.row_selected
        if self.is_row_selected_checked(_row_selected):
            _big_table_data = self.parent.big_table_data
            _lconfig = _big_table_data[_row_selected, 2]
            if not _lconfig:
                # no data loaded on this row
                return
            if bool(_lconfig.tof_auto_flag):
                self.parent.ui.dataTOFautoMode.setChecked(True)
            else:
                self.parent.ui.dataTOFmanualMode.setChecked(True)
            o_auto_tof_range = AutoTofRangeRadioButtonHandler(parent=self.parent)
            o_auto_tof_range.setup()
            o_auto_tof_range.radio_button_handler()

    def is_data_tab_selected(self):
        if self.parent.ui.dataNormTabWidget.currentIndex() == 0:
            return True
        else:
            return False

    def is_row_selected_checked(self, row_selected):
        _widget = self.parent.ui.reductionTable.cellWidget(row_selected, 0)
        current_state = _widget.checkState()
        if current_state == Qt.Unchecked:
            return False
        else:
            return True

    def update_state_of_all_checkboxes(self):
        for row in range(self.size_check_box_state_table):
            _state = self._reduction_table_check_box_state[row]
            _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
            _widget.setChecked(_state)
