from qtpy.QtWidgets import QMainWindow

from refred.calculations.lr_data import LRData
from refred.gui_handling.gui_utility import GuiUtility
from refred.interfaces import load_ui
from refred.reduction.reduced_data_handler import ReducedDataHandler
from refred.tabledata import TableData


class ChangeStitchingDataInterval(object):
    def __init__(self, parent=None, yaxis_type="RvsQ", x_min=None, x_max=None, y_min=None, y_max=None) -> None:
        self.parent = parent
        row = 0
        big_table_data: TableData = parent.big_table_data
        _lrdata: LRData = big_table_data.reflectometry_data(row)

        if yaxis_type == "RvsQ":
            [xmin_user, xmax_user] = _lrdata.all_plot_axis.reduced_plot_RQQ4userView_x  # type: ignore
            [ymin_user, ymax_user] = _lrdata.all_plot_axis.reduced_plot_RQuserView_y  # type: ignore

            if (x_min is None) and (x_max is None):
                _lrdata.all_plot_axis.reduced_plot_RQuserView_y = [y_min, y_max]
                _lrdata.all_plot_axis.reduced_plot_RQQ4userView_x = [xmin_user, xmax_user]

            else:
                _lrdata.all_plot_axis.reduced_plot_RQuserView_y = [ymin_user, ymax_user]
                _lrdata.all_plot_axis.reduced_plot_RQQ4userView_x = [x_min, x_max]

        else:
            [xmin_user, xmax_user] = _lrdata.all_plot_axis.reduced_plot_RQQ4userView_x  # type: ignore
            [ymin_user, ymax_user] = _lrdata.all_plot_axis.reduced_plot_RQ4userView_y  # type: ignore

            if (x_min is None) and (x_max is None):
                _lrdata.all_plot_axis.reduced_plot_RQ4userView_y = [y_min, y_max]
                _lrdata.all_plot_axis.reduced_plot_RQQ4userView_x = [xmin_user, xmax_user]

            else:
                _lrdata.all_plot_axis.reduced_plot_RQ4userView_y = [ymin_user, ymax_user]
                _lrdata.all_plot_axis.reduced_plot_RQQ4userView_x = [x_min, x_max]

        big_table_data.set_reflectometry_data(row, _lrdata)
        parent.big_table_data = big_table_data

        self.plot()

    def plot(self):
        o_reduced_handler = ReducedDataHandler(parent=self.parent)
        o_reduced_handler.plot()


class LaunchStitchingManualXAxis(QMainWindow):
    x_min = None
    x_max = None
    _lrdata = None
    yaxis_type = "RvsQ"

    def __init__(self, parent=None, mouse_x=0, mouse_y=0):
        QMainWindow.__init__(self, parent=parent)

        self.setWindowModality(False)
        self.ui = load_ui("manual_x_axis_interface.ui", self)
        self.parent = parent

        o_gui_utility = GuiUtility(parent=self.parent)
        self.yaxis_type = o_gui_utility.get_reduced_yaxis_type()

        big_table_data = self.parent.big_table_data
        self._lrdata = big_table_data[0, 0]

        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)

        self.parent.pos()
        plot_gui_pos = self.parent.ui.data_stitching_plot.pos()
        plot_gui_height = self.parent.ui.data_stitching_plot.frameGeometry().height()
        self.move(mouse_x + plot_gui_pos.x(), plot_gui_pos.y() + plot_gui_height + mouse_y - 50)

        self.init_widgets()

    def init_widgets(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        axis_type = o_gui_utility.get_reduced_yaxis_type()

        if axis_type == "RvsQ":
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ_view()
        else:
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ4Q_view()

        self.x_min = _x_min
        self.x_max = _x_max

        _x_min_str = "%.8f" % _x_min
        _x_max_str = "%.8f" % _x_max

        self.ui.x_min_value.setText(_x_min_str)
        self.ui.x_max_value.setText(_x_max_str)

    def closeEvent(self, event=None):
        self.parent.manual_x_axis_dialog = None

    def x_min_event(self):
        self.validate_changes()

    def x_max_event(self):
        self.validate_changes()

    def x_auto_rescale_event(self):
        #        [xmin_user, xmax_user] = self._lrdata.all_plot_axis.reduced_plot_RQQ4userView_x
        [xmin_auto, xmax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQQ4autoView_x
        self._lrdata.all_plot_axis.reduced_plot_RQQ4userView_x = [xmin_auto, xmax_auto]

        # [xmin_user, xmax_user, ymin_user, ymax_user] = self._lrdata.all_plot_axis.reduced_plot_RQuserView
        # [xmin_auto, xmax_auto, ymin_auto, ymax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQautoView
        # self._lrdata.all_plot_axis.reduced_plot_RQuserView = [xmin_auto, xmax_auto, ymin_user, ymax_user]

        big_table_data = self.parent.big_table_data
        big_table_data[0, 0] = self._lrdata
        self.parent.big_table_data = big_table_data

        o_reduced_handler = ReducedDataHandler(parent=self.parent)
        o_reduced_handler.plot()

    def validate_changes(self):
        self.x_min = float(str(self.ui.x_min_value.text()))
        self.x_max = float(str(self.ui.x_max_value.text()))
        ChangeStitchingDataInterval(parent=self.parent, yaxis_type=self.yaxis_type, x_min=self.x_min, x_max=self.x_max)


class LaunchStitchingManualYAxis(QMainWindow):
    y_min = None
    y_max = None
    _lrdata = None
    yaxis_type = "RvsQ"

    def __init__(self, parent=None, mouse_x=0, mouse_y=0):
        QMainWindow.__init__(self, parent=parent)
        self.setWindowModality(False)
        self.ui = load_ui("manual_y_axis_interface.ui", self)
        self.parent = parent

        o_gui_utility = GuiUtility(parent=self.parent)
        self.yaxis_type = o_gui_utility.get_reduced_yaxis_type()

        big_table_data = self.parent.big_table_data
        self._lrdata = big_table_data[0, 0]

        width = self.width()
        height = self.height()
        self.setFixedSize(width, height)

        self.parent.pos()
        plot_gui_pos = self.parent.ui.data_stitching_plot.pos()
        plot_gui_height = self.parent.ui.data_stitching_plot.frameGeometry().height()
        self.move(mouse_x + plot_gui_pos.x(), plot_gui_height - mouse_y + plot_gui_pos.y())

        self.init_widgets()

    def init_widgets(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        axis_type = o_gui_utility.get_reduced_yaxis_type()

        if axis_type == "RvsQ":
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ_view()
        else:
            [_x_min, _x_max, _y_min, _y_max] = self._lrdata.all_plot_axis.get_user_reduced_RQ4Q_view()

        self.y_min = _y_min
        self.y_max = _y_max

        _y_min_str = "%.8f" % _y_min
        _y_max_str = "%.8f" % _y_max

        self.ui.y_min_value.setText(_y_min_str)
        self.ui.y_max_value.setText(_y_max_str)

    def closeEvent(self, event=None):
        self.parent.manual_y_axis_dialog = None

    def y_min_event(self):
        self.validate_changes()

    def y_max_event(self):
        self.validate_changes()

    def y_auto_rescale_event(self):
        if self.yaxis_type == "RvsQ":
            [xmin_user, xmax_user] = self._lrdata.all_plot_axis.reduced_plot_RQQ4userView_x
            [ymin_user, ymax_user] = self._lrdata.all_plot_axis.reduced_plot_RQuserView_y
            [xmin_auto, xmax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQQ4autoView_x
            [ymin_auto, ymax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQautoView_y
            self._lrdata.all_plot_axis.reduced_plot_RQuserView_y = [ymin_auto, ymax_auto]
            ymin, ymax = ymin_auto, ymax_auto

            # self._lrdata.all_plot_axis.reduced_plot_RQQ4userView_x = [xmin_user, xmax_user]
            # [xmin_user, xmax_user, ymin_user, ymax_user] = self._lrdata.all_plot_axis.reduced_plot_RQuserView
            # [xmin_auto, xmax_auto, ymin_auto, ymax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQautoView
            # self._lrdata.all_plot_axis.reduced_plot_RQuserView = [xmin_user, xmax_user, ymin_auto, ymax_auto]

        else:
            [xmin_user, xmax_user] = self._lrdata.all_plot_axis.reduced_plot_RQQ4userView_x
            [ymin_user, ymax_user] = self._lrdata.all_plot_axis.reduced_plot_RQ4userView_y
            [xmin_auto, xmax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQQ4autoView_x
            [ymin_auto, ymax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQ4autoView_y
            self._lrdata.all_plot_axis.reduced_plot_RQ4userView_y = [ymin_auto, ymax_auto]
            ymin, ymax = ymin_auto, ymax_auto

            # [xmin_user, xmax_user, ymin_user, ymax_user] = self._lrdata.all_plot_axis.reduced_plot_RQ4QuserView
            # [xmin_auto, xmax_auto, ymin_auto, ymax_auto] = self._lrdata.all_plot_axis.reduced_plot_RQ4QautoView
            # self._lrdata.all_plot_axis.reduced_plot_RQ4QuserView = [xmin_user, xmax_user, ymin_auto, ymax_auto]

        _ymin_str = "%.8f" % ymin
        _ymax_str = "%.8f" % ymax

        self.ui.y_min_value.setText(_ymin_str)
        self.ui.y_max_value.setText(_ymax_str)

        big_table_data = self.parent.big_table_data
        big_table_data[0, 0] = self._lrdata
        self.parent.big_table_data = big_table_data

        o_reduced_handler = ReducedDataHandler(parent=self.parent)
        o_reduced_handler.plot()

    def validate_changes(self):
        self.y_min = float(str(self.ui.y_min_value.text()))
        self.y_max = float(str(self.ui.y_max_value.text()))
        ChangeStitchingDataInterval(parent=self.parent, yaxis_type=self.yaxis_type, y_min=self.y_min, y_max=self.y_max)
