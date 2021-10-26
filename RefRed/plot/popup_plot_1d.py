from qtpy.QtGui import QPalette
from qtpy.QtWidgets import QDialog, QFileDialog
from qtpy.QtCore import Qt
import os
from pathlib import Path
import bisect

from RefRed.interfaces import load_ui
from RefRed.plot.display_plots import DisplayPlots
from RefRed.gui_handling.gui_utility import GuiUtility
import RefRed.colors
import RefRed.utilities


class PopupPlot1d(QDialog):

    parent = None
    data_type = "data"
    data = None
    is_data = True
    row = 0
    col = 0  # 0 for data, 1 for norm

    _open_instances = []
    yaxis = None
    peak = None
    back = None

    _prev_peak1 = -1
    _prev_peak2 = -1
    _prev_back1 = -1
    _prev_back2 = -1
    _prev_clock1 = -1
    _prev_clock2 = -1

    isJimLog = True
    isJohnLog = True

    nbr_pixel_y_axis = 304

    def __init__(self, parent=None, data_type="data", data=None, row=0):

        self.data_type = data_type
        self.parent = parent
        self.data = data
        self.row = row
        self.col = 0 if data_type == "data" else 1
        self.is_data = True if data_type == "data" else False
        self.is_row_with_highest_q = self.is_row_with_higest_q()

        QDialog.__init__(self, parent=parent)
        self.setWindowModality(False)
        self._open_instances.append(self)
        self.ui = load_ui("plot_dialog_refl_interface.ui", self)

        self.setWindowTitle("Counts vs Y pixel (Jim and John views)")
        self.hide_and_format_invalid_widgets()

        self.ui.plot_counts_vs_pixel.leaveFigure.connect(
            self.leave_plot_counts_vs_pixel
        )
        self.ui.plot_counts_vs_pixel.toolbar.homeClicked.connect(
            self.home_plot_counts_vs_pixel
        )
        self.ui.plot_counts_vs_pixel.toolbar.exportClicked.connect(
            self.export_counts_vs_pixel
        )

        self.ui.plot_pixel_vs_counts.leaveFigure.connect(
            self.leave_plot_pixel_vs_counts
        )
        self.ui.plot_pixel_vs_counts.toolbar.homeClicked.connect(
            self.home_plot_pixel_vs_counts
        )
        self.ui.plot_pixel_vs_counts.toolbar.exportClicked.connect(
            self.export_counts_vs_pixel
        )

        _new_detector_geometry_flag = self.data.new_detector_geometry_flag
        if not _new_detector_geometry_flag:
            self.reset_max_ui_value()
            self.nbr_pixel_y_axis = 256  # TODO MAGIC NUMBER

        self.widgets_to_show()
        self.init_plot()

    def is_row_with_higest_q(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        return o_gui_utility.is_row_with_highest_q()

    def export_counts_vs_pixel(self):
        _active_data = self.data
        run_number = _active_data.run_number
        default_filename = Path(self.parent.path_ascii) / f"REFL_{run_number}_rpx.txt"
        caption = "Create Counts vs Pixel ASCII File"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            caption,
            str(default_filename),
        )
        if filename:
            self.parent.path_ascii = os.path.dirname(filename)

            ycountsdata = _active_data.ycountsdata
            pixelaxis = list(range(len(ycountsdata)))

            text = ["#Couns vs Pixels", "#Pixel - Counts"]
            text += [f"{p} {y}" for p, y in zip(pixelaxis, ycountsdata)]

            RefRed.utilities.write_ascii_file(filename, text)

    def leave_plot_counts_vs_pixel(self):
        [xmin, xmax] = self.ui.plot_counts_vs_pixel.canvas.ax.yaxis.get_view_interval()
        [ymin, ymax] = self.ui.plot_counts_vs_pixel.canvas.ax.xaxis.get_view_interval()
        self.ui.plot_counts_vs_pixel.canvas.ax.xaxis.set_data_interval(xmin, xmax)
        self.ui.plot_counts_vs_pixel.canvas.ax.yaxis.set_data_interval(ymin, ymax)
        self.ui.plot_counts_vs_pixel.draw()
        self.ui.plot_pixel_vs_counts.canvas.ax.xaxis.set_data_interval(ymin, ymax)
        self.ui.plot_pixel_vs_counts.canvas.ax.yaxis.set_data_interval(xmin, xmax)
        # self.ui.plot_pixel_vs_counts.draw()
        self.data.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
        self.update_pixel_vs_counts_plot()

    def home_plot_counts_vs_pixel(self):
        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_data_interval
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.draw()
        self.ui.plot_pixel_vs_counts.canvas.ax.set_xlim([xmin, xmax])
        self.ui.plot_pixel_vs_counts.canvas.ax.set_ylim([ymin, ymax])
        self.ui.plot_pixel_vs_counts.draw()

    def leave_plot_pixel_vs_counts(self):
        [xmin, xmax] = self.ui.plot_pixel_vs_counts.canvas.ax.xaxis.get_view_interval()
        [ymin, ymax] = self.ui.plot_pixel_vs_counts.canvas.ax.yaxis.get_view_interval()
        self.ui.plot_pixel_vs_counts.canvas.ax.xaxis.set_data_interval(xmin, xmax)
        self.ui.plot_pixel_vs_counts.canvas.ax.yaxis.set_data_interval(ymin, ymax)
        self.ui.plot_pixel_vs_counts.draw()
        self.ui.plot_counts_vs_pixel.canvas.ax.xaxis.set_data_interval(ymin, ymax)
        self.ui.plot_counts_vs_pixel.canvas.ax.yaxis.set_data_interval(xmin, xmax)
        # self.ui.plot_counts_vs_pixel.draw()
        self.data.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
        self.update_counts_vs_pixel_plot()

    def home_plot_pixel_vs_counts(self):
        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_data_interval
        self.ui.plot_pixel_vs_counts.canvas.ax.set_xlim([xmin, xmax])
        self.ui.plot_pixel_vs_counts.canvas.ax.set_ylim([ymin, ymax])
        self.ui.plot_pixel_vs_counts.draw()
        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])
        self.ui.plot_counts_vs_pixel.draw()

    def hide_and_format_invalid_widgets(self):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.red)
        self.ui.jim_peak1_label.setVisible(False)
        self.ui.jim_peak1_label.setPalette(palette)
        self.ui.jim_peak2_label.setVisible(False)
        self.ui.jim_peak2_label.setPalette(palette)
        self.ui.jim_back1_label.setVisible(False)
        self.ui.jim_back1_label.setPalette(palette)
        self.ui.jim_back2_label.setVisible(False)
        self.ui.jim_back2_label.setPalette(palette)
        self.ui.john_peak1_label.setVisible(False)
        self.ui.john_peak1_label.setPalette(palette)
        self.ui.john_peak2_label.setVisible(False)
        self.ui.john_peak2_label.setPalette(palette)
        self.ui.john_back1_label.setVisible(False)
        self.ui.john_back1_label.setPalette(palette)
        self.ui.john_back2_label.setVisible(False)
        self.ui.john_back2_label.setPalette(palette)
        self.ui.invalid_selection_label.setVisible(False)
        self.ui.invalid_selection_label.setPalette(palette)

    def sort_peak_back_input(self):
        peak1 = self.ui.jim_peak1.value()
        peak2 = self.ui.jim_peak2.value()
        peak_min = min([peak1, peak2])
        # peak_max = max([peak1, peak2])
        if peak_min != peak1:
            self.ui.jim_peak1.setValue(peak2)
            self.ui.john_peak1.setValue(peak2)
            self.ui.jim_peak2.setValue(peak1)
            self.ui.john_peak2.setValue(peak1)

        back1 = self.ui.jim_back1.value()
        back2 = self.ui.jim_back2.value()
        back_min = min([back1, back2])
        # back_max = max([back1, back2])
        if back_min != back1:
            self.ui.jim_back1.setValue(back2)
            self.ui.john_back1.setValue(back2)
            self.ui.jim_back2.setValue(back1)
            self.ui.john_back2.setValue(back1)

    def check_peak_back_input_validity(self):
        peak1 = self.ui.jim_peak1.value()
        peak2 = self.ui.jim_peak2.value()
        back1 = self.ui.jim_back1.value()
        back2 = self.ui.jim_back2.value()

        _show_widgets_1 = False
        _show_widgets_2 = False

        if self.ui.jim_back_flag.isChecked():
            if back1 > peak1:
                _show_widgets_1 = True
            if back2 < peak2:
                _show_widgets_2 = True

        self.ui.jim_back1_label.setVisible(_show_widgets_1)
        self.ui.jim_peak1_label.setVisible(_show_widgets_1)
        self.ui.jim_back2_label.setVisible(_show_widgets_2)
        self.ui.jim_peak2_label.setVisible(_show_widgets_2)

        self.ui.john_back1_label.setVisible(_show_widgets_1)
        self.ui.john_peak1_label.setVisible(_show_widgets_1)
        self.ui.john_back2_label.setVisible(_show_widgets_2)
        self.ui.john_peak2_label.setVisible(_show_widgets_2)

        self.ui.invalid_selection_label.setVisible(_show_widgets_1 or _show_widgets_2)

    # def widgets_to_show(self, widget, status):
    def widgets_to_show(self):

        if self.is_row_with_highest_q:
            enable_status = True
        else:
            enable_status = False

        if not self.is_data:
            self.ui.john_clocking_box.setVisible(False)
            self.ui.jim_clocking_box.setVisible(False)
            return

        self.ui.jim_clocking_box.setEnabled(enable_status)
        self.ui.john_clocking_box.setEnabled(enable_status)

    def reset_max_ui_value(self):
        self.ui.john_peak1.setMaximum(255)
        self.ui.john_peak2.setMaximum(255)
        self.ui.jim_peak1.setMaximum(255)
        self.ui.jim_peak2.setMaximum(255)
        self.ui.john_back1.setMaximum(255)
        self.ui.john_back2.setMaximum(255)
        self.ui.jim_back1.setMaximum(255)
        self.ui.jim_back2.setMaximum(255)

    def get_ycountsdata_of_tof_range_selected(self):
        if self.data.tof_range_auto_flag:
            _tofRange = self.getTOFrangeInMs(self.data.tof_range_auto)
        else:
            _tofRange = self.getTOFrangeInMs(self.data.tof_range_manual)

        tmin = float(_tofRange[0])
        tmax = float(_tofRange[1])

        ytof = self.data.ytofdata
        tof = self.getFullTOFinMs(self.data.tof_axis_auto_with_margin)

        index_tof_left = bisect.bisect_left(tof, tmin)
        index_tof_right = bisect.bisect_right(tof, tmax)

        _new_ytof = ytof[:, index_tof_left:index_tof_right]
        _new_ycountsdata = _new_ytof.sum(axis=1)

        return _new_ycountsdata

    def getTOFrangeInMs(self, tof_axis):
        if float(tof_axis[-1]) > 1000:
            coeff = 1.0e-3
        else:
            coeff = 1.0
        return [float(tof_axis[0]) * coeff, float(tof_axis[-1]) * coeff]

    def getFullTOFinMs(self, tof_axis):
        if tof_axis[-1] > 1000:
            return tof_axis / float(1000)
        else:
            return tof_axis

    def init_plot(self):
        self.ycountsdata = self.get_ycountsdata_of_tof_range_selected()
        _yaxis = self.ycountsdata

        xaxis = list(range(len(_yaxis)))
        self.xaxis = xaxis

        _peak = self.data.peak
        _back = self.data.back
        _clock = self.data.clocking

        [peak1, peak2] = _peak
        [back1, back2] = _back
        [clock1, clock2] = _clock

        back_flag = RefRed.utilities.str2bool(self.data.back_flag)
        self.ui.jim_back_flag.setChecked(back_flag)
        self.ui.john_back_flag.setChecked(back_flag)

        peak1 = int(peak1)
        peak2 = int(peak2)
        back1 = int(back1)
        back2 = int(back2)
        clock1 = int(clock1)
        clock2 = int(clock2)

        self._prev_peak1 = peak1
        self._prev_peak2 = peak2
        self._prev_back1 = back1
        self._prev_back2 = back2
        self._prev_clock1 = clock1
        self._prev_clock2 = clock2

        # John
        ui_plot1 = self.ui.plot_pixel_vs_counts
        ui_plot1.plot(_yaxis, xaxis)
        ui_plot1.canvas.ax.set_xlabel("counts")
        ui_plot1.canvas.ax.set_ylabel("Pixels")
        if self.isJohnLog:
            ui_plot1.canvas.ax.set_xscale("log")
        else:
            ui_plot1.canvas.ax.set_xscale("linear")
        ui_plot1.canvas.ax.set_ylim(0, self.nbr_pixel_y_axis - 1)
        ui_plot1.canvas.ax.axhline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        ui_plot1.canvas.ax.axhline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if self.is_data:
            ui_plot1.canvas.ax.axhline(
                clock1, color=RefRed.colors.CLOCKING_SELECTION_COLOR
            )
            ui_plot1.canvas.ax.axhline(
                clock2, color=RefRed.colors.CLOCKING_SELECTION_COLOR
            )

        if back_flag:
            ui_plot1.canvas.ax.axhline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot1.canvas.ax.axhline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        if self.data.all_plot_axis.yi_data_interval is None:
            ui_plot1.draw()
            [
                xmin,
                xmax,
            ] = self.ui.plot_pixel_vs_counts.canvas.ax.xaxis.get_view_interval()
            [
                ymin,
                ymax,
            ] = self.ui.plot_pixel_vs_counts.canvas.ax.yaxis.get_view_interval()
            self.data.all_plot_axis.yi_data_interval = [xmin, xmax, ymin, ymax]
            self.data.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
            self.ui.plot_pixel_vs_counts.toolbar.home_settings = [
                xmin,
                xmax,
                ymin,
                ymax,
            ]
        else:
            [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_view_interval
            self.ui.plot_pixel_vs_counts.canvas.ax.set_xlim([xmin, xmax])
            self.ui.plot_pixel_vs_counts.canvas.ax.set_ylim([ymin, ymax])
            ui_plot1.draw()

        # Jim
        ui_plot2 = self.ui.plot_counts_vs_pixel
        ui_plot2.canvas.ax.plot(xaxis, _yaxis)
        ui_plot2.canvas.ax.set_xlabel("Pixels")
        ui_plot2.canvas.ax.set_ylabel("Counts")
        if self.isJimLog:
            ui_plot2.canvas.ax.set_yscale("log")
        else:
            ui_plot2.canvas.ax.set_yscale("linear")
        ui_plot2.canvas.ax.set_xlim(0, self.nbr_pixel_y_axis - 1)

        ui_plot2.canvas.ax.axvline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        ui_plot2.canvas.ax.axvline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if self.is_data:
            ui_plot2.canvas.ax.axvline(
                clock1, color=RefRed.colors.CLOCKING_SELECTION_COLOR
            )
            ui_plot2.canvas.ax.axvline(
                clock2, color=RefRed.colors.CLOCKING_SELECTION_COLOR
            )

        if back_flag:
            ui_plot2.canvas.ax.axvline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot2.canvas.ax.axvline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])
        ui_plot2.draw()

        # John and Jim peak and back
        self.set_peak_value(peak1, peak2)
        self.set_back_value(back1, back2)
        self.set_clock_value(clock1, clock2)

        ui_plot1.logtogx.connect(self.logtogglexlog)
        ui_plot2.logtogy.connect(self.logtoggleylog)

    def logtogglexlog(self, status):
        if status == "log":
            self.isJohnLog = True
        else:
            self.isJohnLog = False

    def logtoggleylog(self, status):
        if status == "log":
            self.isJimLog = True
        else:
            self.isJimLog = False

    def jim_back_flag_clicked(self, status):
        self.ui.john_back_flag.setChecked(status)
        self.data.back_flag = status
        self.update_plots()
        self.update_back_flag_widgets()
        self.check_peak_back_input_validity()

    def john_back_flag_clicked(self, status):
        self.ui.jim_back_flag.setChecked(status)
        self.data.back_flag = status
        self.update_plots()
        self.update_back_flag_widgets()
        self.check_peak_back_input_validity()

    def update_back_flag_widgets(self):
        status_flag = self.ui.jim_back_flag.isChecked()
        self.ui.jim_back1.setEnabled(status_flag)
        self.ui.jim_back2.setEnabled(status_flag)
        self.ui.john_back1.setEnabled(status_flag)
        self.ui.john_back2.setEnabled(status_flag)

    def set_peak_value(self, peak1, peak2):
        self.ui.john_peak1.setValue(peak1)
        self.ui.jim_peak1.setValue(peak1)
        self.ui.john_peak2.setValue(peak2)
        self.ui.jim_peak2.setValue(peak2)
        self.check_peak_back_input_validity()

    def set_back_value(self, back1, back2):
        self.ui.john_back1.setValue(back1)
        self.ui.jim_back1.setValue(back1)
        self.ui.john_back2.setValue(back2)
        self.ui.jim_back2.setValue(back2)
        self.check_peak_back_input_validity()

    def set_clock_value(self, clock1, clock2):
        self.ui.john_clock1.setValue(clock1)
        self.ui.jim_clock1.setValue(clock1)
        self.ui.john_clock2.setValue(clock2)
        self.ui.jim_clock2.setValue(clock2)

    # peak1
    def update_peak1(self, value, updateJimSpinbox=True, updateJohnSpinbox=True):
        if updateJimSpinbox:
            self.ui.jim_peak1.setValue(value)
        if updateJohnSpinbox:
            self.ui.john_peak1.setValue(value)
        self._prev_peak1 = value

    def jim_peak1_spinbox_signal(self):
        value = self.ui.jim_peak1.value()
        if value == self._prev_peak1:
            return
        self.update_peak1(value, updateJimSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    def john_peak1_spinbox_signal(self):
        value = self.ui.john_peak1.value()
        if value == self._prev_peak1:
            return
        self.update_peak1(value, updateJohnSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    # peak2
    def update_peak2(self, value, updateJimSpinbox=True, updateJohnSpinbox=True):
        if updateJimSpinbox:
            self.ui.jim_peak2.setValue(value)
        if updateJohnSpinbox:
            self.ui.john_peak2.setValue(value)
        self._prev_peak2 = value
        self.check_peak_back_input_validity()

    def jim_peak2_spinbox_signal(self):
        value = self.ui.jim_peak2.value()
        if value == self._prev_peak2:
            return
        self.update_peak2(value, updateJimSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    def john_peak2_spinbox_signal(self):
        value = self.ui.john_peak2.value()
        if value == self._prev_peak2:
            return
        self.update_peak2(value, updateJohnSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    # back1
    def update_back1(self, value, updateJimSpinbox=True, updateJohnSpinbox=True):
        if updateJimSpinbox:
            self.ui.jim_back1.setValue(value)
        if updateJohnSpinbox:
            self.ui.john_back1.setValue(value)
        self._prev_back1 = value
        self.check_peak_back_input_validity()

    def jim_back1_spinbox_signal(self):
        value = self.ui.jim_back1.value()
        if value == self._prev_back1:
            return
        self.update_back1(value, updateJimSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    def john_back1_spinbox_signal(self):
        value = self.ui.john_back1.value()
        if value == self._prev_back1:
            return
        self.update_back1(value, updateJohnSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    # back2
    def update_back2(self, value, updateJimSpinbox=True, updateJohnSpinbox=True):
        if updateJimSpinbox:
            self.ui.jim_back2.setValue(value)
        if updateJohnSpinbox:
            self.ui.john_back2.setValue(value)
        self._prev_back2 = value
        self.check_peak_back_input_validity()

    def jim_back2_spinbox_signal(self):
        value = self.ui.jim_back2.value()
        if value == self._prev_back2:
            return
        self.update_back2(value, updateJimSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    def john_back2_spinbox_signal(self):
        value = self.ui.john_back2.value()
        if value == self._prev_back2:
            return
        self.update_back2(value, updateJohnSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    def jim_clock_spinbox_signal(self):
        self.update_clock(updateJohnSpinBox=True)
        self.update_plots()

    def john_clock_spinbox_signal(self):
        self.update_clock(updateJohnSpinBox=False)
        self.update_plots()

    def update_clock(self, updateJohnSpinBox=True):
        if updateJohnSpinBox:
            self.ui.john_clock1.setValue(self.ui.jim_clock1.value())
            self.ui.john_clock2.setValue(self.ui.jim_clock2.value())
        else:
            self.ui.jim_clock1.setValue(self.ui.john_clock1.value())
            self.ui.jim_clock2.setValue(self.ui.john_clock2.value())

    def update_plots(self):
        self.update_pixel_vs_counts_plot()
        self.update_counts_vs_pixel_plot()

    def update_pixel_vs_counts_plot(self):
        self.ui.plot_pixel_vs_counts.clear()

        peak1 = self.ui.jim_peak1.value()
        peak2 = self.ui.jim_peak2.value()
        back1 = self.ui.jim_back1.value()
        back2 = self.ui.jim_back2.value()
        clock1 = self.ui.jim_clock1.value()
        clock2 = self.ui.jim_clock2.value()

        _yaxis = self.ycountsdata

        ui_plot1 = self.ui.plot_pixel_vs_counts
        ui_plot1.canvas.ax.plot(_yaxis, self.xaxis)
        ui_plot1.canvas.ax.set_xlabel("counts")
        ui_plot1.canvas.ax.set_ylabel("Pixels")
        if self.isJohnLog:
            ui_plot1.canvas.ax.set_xscale("log")
        else:
            ui_plot1.canvas.ax.set_xscale("linear")
        # 		ui_plot1.canvas.ax.set_ylim(0,self.nbr_pixel_y_axis-1)
        ui_plot1.canvas.ax.axhline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        ui_plot1.canvas.ax.axhline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        ui_plot1.canvas.ax.axhline(clock1, color=RefRed.colors.CLOCKING_SELECTION_COLOR)
        ui_plot1.canvas.ax.axhline(clock2, color=RefRed.colors.CLOCKING_SELECTION_COLOR)

        if self.data.back_flag:
            ui_plot1.canvas.ax.axhline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot1.canvas.ax.axhline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_view_interval
        self.ui.plot_pixel_vs_counts.canvas.ax.set_xlim([xmin, xmax])
        self.ui.plot_pixel_vs_counts.canvas.ax.set_ylim([ymin, ymax])

        ui_plot1.canvas.draw_idle()

    def update_counts_vs_pixel_plot(self):
        self.ui.plot_counts_vs_pixel.clear()

        peak1 = self.ui.jim_peak1.value()
        peak2 = self.ui.jim_peak2.value()
        back1 = self.ui.jim_back1.value()
        back2 = self.ui.jim_back2.value()
        clock1 = self.ui.jim_clock1.value()
        clock2 = self.ui.jim_clock2.value()

        _yaxis = self.ycountsdata

        ui_plot2 = self.ui.plot_counts_vs_pixel
        ui_plot2.canvas.ax.plot(self.xaxis, _yaxis)
        ui_plot2.canvas.ax.set_xlabel("Pixels")
        ui_plot2.canvas.ax.set_ylabel("Counts")
        if self.isJimLog:
            ui_plot2.canvas.ax.set_yscale("log")
        else:
            ui_plot2.canvas.ax.set_yscale("linear")
        # 		ui_plot2.canvas.ax.set_xlim(0,self.nbr_pixel_y_axis-1)

        ui_plot2.canvas.ax.axvline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        ui_plot2.canvas.ax.axvline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        ui_plot2.canvas.ax.axvline(clock1, color=RefRed.colors.CLOCKING_SELECTION_COLOR)
        ui_plot2.canvas.ax.axvline(clock2, color=RefRed.colors.CLOCKING_SELECTION_COLOR)

        if self.data.back_flag:
            ui_plot2.canvas.ax.axvline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot2.canvas.ax.axvline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_view_interval
        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])

        ui_plot2.canvas.draw_idle()

    def closeEvent(self, event=None):
        peak1 = self.ui.jim_peak1.value()
        peak2 = self.ui.jim_peak2.value()
        back1 = self.ui.jim_back1.value()
        back2 = self.ui.jim_back2.value()
        backFlag = self.ui.jim_back_flag.isChecked()

        big_table_data = self.parent.big_table_data

        _data = big_table_data[self.row, self.col]
        _data.peak = [str(peak1), str(peak2)]
        _data.back = [str(back1), str(back2)]
        _data.back_flag = backFlag

        big_table_data[self.row, self.col] = _data

        if self.is_row_with_highest_q:
            _clock1 = self.ui.jim_clock1.value()
            _clock2 = self.ui.jim_clock2.value()
            _clocking = [str(_clock1), str(_clock2)]
            _data = big_table_data[0, 0]
            index = 0
            while _data is not None:
                _data.clocking = _clocking
                big_table_data[index, 0] = _data
                _data = big_table_data[index + 1, 0]
                index += 1
            self.parent.ui.dataPrimFromValue.setValue(_clock1)
            self.parent.ui.dataPrimToValue.setValue(_clock2)

        self.parent.big_table_data = big_table_data

        if self.data_type == "data":
            self.parent.ui.dataPeakFromValue.setValue(peak1)
            self.parent.ui.dataPeakToValue.setValue(peak2)
            self.parent.ui.dataBackFromValue.setValue(back1)
            self.parent.ui.dataBackToValue.setValue(back2)
            self.parent.ui.dataBackgroundFlag.setChecked(backFlag)
            # 			self.parent.data_peak_and_back_validation(False)
            self.parent.ui.dataBackFromLabel.setEnabled(backFlag)
            self.parent.ui.dataBackFromValue.setEnabled(backFlag)
            self.parent.ui.dataBackToLabel.setEnabled(backFlag)
            self.parent.ui.dataBackToValue.setEnabled(backFlag)

        else:
            self.parent.ui.normPeakFromValue.setValue(peak1)
            self.parent.ui.normPeakToValue.setValue(peak2)
            self.parent.ui.normBackFromValue.setValue(back1)
            self.parent.ui.normBackToValue.setValue(back2)
            self.parent.ui.normBackgroundFlag.setChecked(backFlag)
            # 			self.parent.norm_peak_and_back_validation(False)
            self.parent.ui.normBackFromLabel.setEnabled(backFlag)
            self.parent.ui.normBackFromValue.setEnabled(backFlag)
            self.parent.ui.normBackToLabel.setEnabled(backFlag)
            self.parent.ui.normBackToValue.setEnabled(backFlag)

        DisplayPlots(
            parent=self.parent,
            row=self.row,
            is_data=self.is_data,
            plot_yt=True,
            plot_yi=True,
            plot_it=False,
            plot_ix=False,
            refresh_reduction_table=True,
        )
