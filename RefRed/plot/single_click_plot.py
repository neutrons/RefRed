import time
from RefRed.plot.popup_plot_1d import PopupPlot1d
from RefRed.plot.popup_plot_2d import PopupPlot2d
from RefRed.plot.launch_stitching_manual_axis import LaunchStitchingManualXAxis
from RefRed.plot.launch_stitching_manual_axis import LaunchStitchingManualYAxis
from RefRed.gui_handling.gui_utility import GuiUtility


DOUBLE_CLICK_DELAY = 0.4  # seconds


class SingleClickPlot(object):

    parent = None
    data = None
    row = 0

    def __init__(
        self,
        parent,
        data_type='data',
        plot_type='yi',
        is_pan_or_zoom_activated=False,
        is_manual_zoom_requested=False,
        is_x_axis_manual_zoom_requested=False,
        mouse_x=0,
        mouse_y=0,
    ):

        self.parent = parent
        if plot_type == 'stitching':
            if is_manual_zoom_requested:
                self.right_click_stitching_plot(is_x_axis_manual_zoom_requested, mouse_x, mouse_y)
            return

        o_gui_utility = GuiUtility(parent=self.parent)
        row = o_gui_utility.get_current_table_reduction_check_box_checked()
        if row == -1:
            return
        self.row = row
        col = o_gui_utility.get_data_norm_tab_selected()

        self.data = parent.big_table_data[row, col]

        if plot_type in ['ix', 'it']:
            return

        if plot_type == 'yi':
            self.single_yi_plot_click(data_type=data_type)

        if plot_type == 'yt':
            self.single_yt_plot_click(data_type=data_type)

    def right_click_stitching_plot(self, is_x_axis_manual_zoom_requested, mouse_x, mouse_y):
        if is_x_axis_manual_zoom_requested:
            if self.parent.manual_x_axis_dialog is None:
                manual_axis = LaunchStitchingManualXAxis(parent=self.parent, mouse_x=mouse_x, mouse_y=mouse_y)
                self.parent.manual_x_axis_dialog = manual_axis
                manual_axis.show()
        else:
            if self.parent.manual_y_axis_dialog is None:
                manual_axis = LaunchStitchingManualYAxis(parent=self.parent, mouse_x=mouse_x, mouse_y=mouse_y)
                self.parent.manual_y_axis_dialog = manual_axis
                manual_axis.show()

    def single_yi_plot_click(self, data_type='data'):
        parent = self.parent
        if parent.time_click1 == -1:
            parent.time_click1 = time.time()
            return
        elif abs(parent.time_click1 - time.time()) > 0.5:
            parent.time_click1 = time.time()
            return
        else:
            _time_click2 = time.time()

        if (_time_click2 - parent.time_click1) <= DOUBLE_CLICK_DELAY:
            popup_plot = PopupPlot1d(parent=self.parent, data_type=data_type, data=self.data, row=self.row)
            popup_plot.show()

        parent.time_click1 = -1

    def single_yt_plot_click(self, data_type='data'):
        parent = self.parent
        if parent.time_click1 == -1:
            parent.time_click1 = time.time()
            return
        elif abs(parent.time_click1 - time.time()) > 0.5:
            parent.time_click1 = time.time()
            return
        else:
            _time_click2 = time.time()

        if (_time_click2 - parent.time_click1) <= DOUBLE_CLICK_DELAY:
            popup_plot = PopupPlot2d(parent=self.parent, data_type=data_type, data=self.data, row=self.row)
            popup_plot.show()
