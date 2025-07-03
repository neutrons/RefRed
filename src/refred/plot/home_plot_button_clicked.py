from refred.gui_handling.gui_utility import GuiUtility


class HomePlotButtonClicked(object):
    parent = None

    def __init__(self, parent=None, plot_type=None):
        if plot_type is None:
            return
        self.parent = parent

        if plot_type == "stitching":
            data = parent.big_table_data[0, 0]
            if data.all_plot_axis.reduced_plot_stitching_tab_data_interval is None:
                return
            [xmin, xmax, ymin, ymax] = data.all_plot_axis.reduced_plot_stitching_tab_data_interval
            _plot_ui = parent.ui.data_stitching_plot.canvas
            [row, column] = [0, 0]

            self.update_manual_axis_input_dialog(xmin, xmax, ymin, ymax)

        else:
            o_gui_utility = GuiUtility(parent=self.parent)
            row = o_gui_utility.get_current_table_reduction_check_box_checked()
            column = 0 if o_gui_utility.is_data_tab_selected() else 1

            data = parent.big_table_data[row, column]

            if data is None:
                return

            if data.all_plot_axis.yi_data_interval is None:
                return

            if plot_type == "yi":
                [xmin, xmax, ymin, ymax] = data.all_plot_axis.yi_data_interval
                data.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
                if column == 0:
                    _plot_ui = parent.ui.data_yi_plot.canvas
                else:
                    _plot_ui = parent.ui.norm_yi_plot.canvas

            elif plot_type == "yt":
                [xmin, xmax, ymin, ymax] = data.all_plot_axis.yt_data_interval
                data.all_plot_axis.yt_view_interval = [xmin, xmax, ymin, ymax]
                if column == 0:
                    _plot_ui = parent.ui.data_yt_plot.canvas
                else:
                    _plot_ui = parent.ui.norm_yt_plot.canvas

            elif plot_type == "it":
                [xmin, xmax, ymin, ymax] = data.all_plot_axis.it_data_interval
                data.all_plot_axis.it_view_interval = [xmin, xmax, ymin, ymax]
                if column == 0:
                    _plot_ui = parent.ui.data_it_plot.canvas
                else:
                    _plot_ui = parent.ui.norm_it_plot.canvas

            elif plot_type == "ix":
                [xmin, xmax, ymin, ymax] = data.all_plot_axis.ix_data_interval
                data.all_plot_axis.ix_view_interval = [xmin, xmax, ymin, ymax]
                if column == 0:
                    _plot_ui = parent.ui.data_ix_plot.canvas
                else:
                    _plot_ui = parent.ui.norm_ix_plot.canvas

        parent.big_table_data[row, column] = data

        _plot_ui.ax.set_xlim([xmin, xmax])
        _plot_ui.ax.set_ylim([ymin, ymax])
        _plot_ui.draw()

    def update_manual_axis_input_dialog(self, xmin, xmax, ymin, ymax):
        if self.parent.manual_x_axis_dialog is not None:
            _xmin = "%.4f" % xmin
            _xmax = "%.4f" % xmax
            self.parent.manual_x_axis_dialog.ui.x_min_value.setText(_xmin)
            self.parent.manual_x_axis_dialog.ui.x_max_value.setText(_xmax)

        if self.parent.manual_y_axis_dialog is not None:
            _ymin = "%.4f" % ymin
            _ymax = "%.4f" % ymax
            self.parent.manual_y_axis_dialog.ui.y_min_value.setText(_ymin)
            self.parent.manual_y_axis_dialog.ui.y_max_value.setText(_ymax)
