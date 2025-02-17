from RefRed.gui_handling.gui_utility import GuiUtility


class LogPlotToggle(object):
    def __init__(self, parent=None, status="log", plot_type=None, is_y_log=True):
        status = str(status)
        if status == "log":
            isLog = True
        else:
            isLog = False

        if plot_type == "stitching":
            [row, column] = [0, 0]
        else:
            o_gui_utility = GuiUtility(parent=parent)
            row = o_gui_utility.get_current_table_reduction_check_box_checked()
            column = 0 if o_gui_utility.is_data_tab_selected() else 1

        data = parent.big_table_data[row, column]
        if data is None:
            return

        if plot_type == "stitching":
            if is_y_log:
                data.all_plot_axis.is_reduced_plot_stitching_tab_ylog = isLog
            else:
                data.all_plot_axis.is_reduced_plot_stitching_tab_xlog = isLog
        elif plot_type == "yi":
            if is_y_log:
                data.all_plot_axis.is_yi_ylog = isLog
            else:
                data.all_plot_axis.is_yi_xlog = isLog
        elif plot_type == "yt":
            if is_y_log:
                data.all_plot_axis.is_yt_ylog = isLog
            else:
                data.all_plot_axis.is_yt_xlog = isLog
        elif plot_type == "it":
            if is_y_log:
                data.all_plot_axis.is_it_ylog = isLog
            else:
                data.all_plot_axis.is_it_xlog = isLog
        elif plot_type == "ix":
            if is_y_log:
                data.all_plot_axis.is_ix_ylog = isLog
            else:
                data.all_plot_axis.is_ix_xlog = isLog

        parent.big_table_data[row, column] = data
