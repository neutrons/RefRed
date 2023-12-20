from qtpy.QtWidgets import QApplication
import numpy as np

from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.gui_handling.fill_stitching_table import FillStitchingTable
import RefRed.colors
from RefRed.tabledata import TableData


class LiveReducedDataHandler(object):

    big_table_data = None
    colors = None
    row_index = 0

    def __init__(self, parent=None, row_index=0):
        self.parent = parent
        self.big_table_data: TableData = self.parent.big_table_data
        self.colors = RefRed.colors.COLOR_LIST
        self.row_index = row_index

    def populate_table(self):
        self.clear_stiching_table()
        o_fill_table = FillStitchingTable(parent=self.parent)
        o_fill_table.fillRow(row_index=self.row_index)

        if self.row_index == 0:
            self.activate_stitching_tab()

    def activate_stitching_tab(self):
        self.parent.ui.plotTab.setCurrentIndex(1)

    def clear_stiching_table(self):
        if self.row_index == 0:
            o_gui_utility = GuiUtility(parent=self.parent)
            o_gui_utility.clear_table(self.parent.ui.dataStitchingTable)

    def plot(self):
        self.parent.ui.data_stitching_plot.clear()
        self.parent.ui.data_stitching_plot.draw()
        big_table_data = self.big_table_data
        _data = big_table_data[0, 0]

        for index_row in range(self.row_index + 1):
            _lconfig = big_table_data.reduction_config(index_row)
            if _lconfig is None:
                return

            _q_axis = _lconfig.q_axis_for_display.copy()
            _y_axis = _lconfig.y_axis_for_display.copy()
            _e_axis = _lconfig.e_axis_for_display.copy()
            sf = self.generate_selected_sf(lconfig=_lconfig)

            _y_axis = np.array(_y_axis, dtype=float)
            _e_axis = np.array(_e_axis, dtype=float)

            _y_axis = _y_axis * sf
            _e_axis = _e_axis * sf

            o_produce_output = ProducedSelectedOutputScaled(
                parent=self.parent, q_axis=_q_axis, y_axis=_y_axis, e_axis=_e_axis
            )
            o_produce_output.calculate()
            y_axis = o_produce_output.output_y_axis
            e_axis = o_produce_output.output_e_axis

            self.parent.ui.data_stitching_plot.errorbar(
                _q_axis, y_axis, yerr=e_axis, color=self.get_current_color_plot(index_row)
            )

            if _data.all_plot_axis.is_reduced_plot_stitching_tab_ylog:
                self.parent.ui.data_stitching_plot.set_yscale('log')

            if _data.all_plot_axis.is_reduced_plot_stitching_tab_xlog:
                self.parent.ui.data_stitching_plot.set_xscale('log')

            self.parent.ui.data_stitching_plot.draw()
            self.parent.ui.data_stitching_plot.canvas.draw_idle()

            QApplication.processEvents()

    def live_plot(self):
        if self.row_index == 0:
            self.parent.ui.data_stitching_plot.clear()
            self.parent.ui.data_stitching_plot.draw()

        big_table_data = self.big_table_data
        _data = big_table_data[0, 0]

        _lconfig = big_table_data[self.row_index, 2]
        if _lconfig is None:
            return

        _q_axis = _lconfig.q_axis_for_display.copy()
        _y_axis = _lconfig.y_axis_for_display.copy()
        _e_axis = _lconfig.e_axis_for_display.copy()
        sf = self.generate_selected_sf(lconfig=_lconfig)

        _y_axis = np.array(_y_axis, dtype=float)
        _e_axis = np.array(_e_axis, dtype=float)

        _y_axis = _y_axis * sf
        _e_axis = _e_axis * sf

        o_produce_output = ProducedSelectedOutputScaled(
            parent=self.parent, q_axis=_q_axis, y_axis=_y_axis, e_axis=_e_axis
        )
        o_produce_output.calculate()
        y_axis = o_produce_output.output_y_axis
        e_axis = o_produce_output.output_e_axis

        self.parent.ui.data_stitching_plot.errorbar(
            _q_axis, y_axis, yerr=e_axis, color=self.get_current_color_plot(self.row_index)
        )

        if _data.all_plot_axis.is_reduced_plot_stitching_tab_ylog:
            self.parent.ui.data_stitching_plot.set_yscale('log')

        if _data.all_plot_axis.is_reduced_plot_stitching_tab_xlog:
            self.parent.ui.data_stitching_plot.set_xscale('log')

        QApplication.processEvents()

    def generate_selected_sf(self, lconfig=None):
        o_gui = GuiUtility(parent=self.parent)
        stitching_type = o_gui.getStitchingType()
        if stitching_type == "absolute":
            return lconfig.sf_abs_normalization
        elif stitching_type == "auto":
            return lconfig.sf_auto
        else:
            return lconfig.sf_manual

    def get_current_color_plot(self, index_color):
        _color_list = self.colors
        _modulo_index = index_color % len(_color_list)
        return _color_list[_modulo_index]


class ProducedSelectedOutputScaled(object):
    parent = None
    axis_type = 'RvsQ'

    def __init__(self, parent=None, q_axis=None, y_axis=None, e_axis=None):
        self.parent = parent
        self.input_q_axis = q_axis
        self.input_y_axis = y_axis
        self.input_e_axis = e_axis

        self.init_output()

    def init_output(self):
        self.output_y_axis = None
        self.output_e_axis = None

    def calculate(self):
        self.get_selected_scale_type()

        input_q_axis = self.input_q_axis
        input_y_axis = self.input_y_axis
        input_e_axis = self.input_e_axis

        # R vs Q selected
        if self.axis_type == 'RvsQ':
            self.output_y_axis = input_y_axis
            self.output_e_axis = input_e_axis
            return

        # RQ4 vs Q selected
        if self.axis_type == 'RQ4vsQ':
            _q_axis_4 = input_q_axis**4
            self.output_y_axis = input_y_axis * _q_axis_4
            self.output_e_axis = input_e_axis * _q_axis_4
            return

        # Log(R) vs Q
        # make sure there is no <= 0 values of _y_axis
        input_y_axis[input_y_axis <= 0] = np.nan
        self.output_y_axis = np.log(input_y_axis)
        self.output_e_axis = input_e_axis  # FIXME

    def get_selected_scale_type(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        self.axis_type = o_gui_utility.get_reduced_yaxis_type()
