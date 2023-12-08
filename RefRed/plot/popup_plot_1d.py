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

    isPlotLog = True

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

        self.setWindowTitle("Counts vs Y pixel")
        self.hide_and_format_invalid_widgets()

        self.ui.plot_counts_vs_pixel.leaveFigure.connect(self.leave_plot_counts_vs_pixel)
        self.ui.plot_counts_vs_pixel.toolbar.homeClicked.connect(self.home_plot_counts_vs_pixel)
        self.ui.plot_counts_vs_pixel.toolbar.exportClicked.connect(self.export_counts_vs_pixel)

        _new_detector_geometry_flag = self.data.new_detector_geometry_flag
        if not _new_detector_geometry_flag:
            self.reset_max_ui_value()
            self.nbr_pixel_y_axis = 256  # TODO MAGIC NUMBER

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
        self.data.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]

    def home_plot_counts_vs_pixel(self):
        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_data_interval
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.draw()

    def hide_and_format_invalid_widgets(self):
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.red)
        self.ui.plotPeakFromLabel.setVisible(False)
        self.ui.plotPeakFromLabel.setPalette(palette)
        self.ui.plotPeakToLabel.setVisible(False)
        self.ui.plotPeakToLabel.setPalette(palette)
        self.ui.plotBackFromLabel.setVisible(False)
        self.ui.plotBackFromLabel.setPalette(palette)
        self.ui.plotBackToLabel.setVisible(False)
        self.ui.plotBackToLabel.setPalette(palette)
        self.ui.invalid_selection_label.setVisible(False)
        self.ui.invalid_selection_label.setPalette(palette)

    def sort_peak_back_input(self):
        peak1 = self.ui.plotPeakFromSpinBox.value()
        peak2 = self.ui.plotPeakToSpinBox.value()
        peak_min = min([peak1, peak2])
        if peak_min != peak1:
            self.ui.plotPeakFromSpinBox.setValue(peak2)
            self.ui.plotPeakToSpinBox.setValue(peak1)

        back1 = self.ui.plotBackFromSpinBox.value()
        back2 = self.ui.plotBackToSpinBox.value()
        back_min = min([back1, back2])
        if back_min != back1:
            self.ui.plotBackFromSpinBox.setValue(back2)
            self.ui.plotBackToSpinBox.setValue(back1)

    def check_peak_back_input_validity(self):
        peak1 = self.ui.plotPeakFromSpinBox.value()
        peak2 = self.ui.plotPeakToSpinBox.value()
        back1 = self.ui.plotBackFromSpinBox.value()
        back2 = self.ui.plotBackToSpinBox.value()

        _show_widgets_1 = False
        _show_widgets_2 = False

        if self.ui.plot_back_flag.isChecked():
            if back1 > peak1:
                _show_widgets_1 = True
            if back2 < peak2:
                _show_widgets_2 = True

        self.ui.plotBackFromLabel.setVisible(_show_widgets_1)
        self.ui.plotPeakFromLabel.setVisible(_show_widgets_1)
        self.ui.plotBackToLabel.setVisible(_show_widgets_2)
        self.ui.plotPeakToLabel.setVisible(_show_widgets_2)

        self.ui.invalid_selection_label.setVisible(_show_widgets_1 or _show_widgets_2)

    def reset_max_ui_value(self):
        self.ui.plotPeakFromSpinBox.setMaximum(255)
        self.ui.plotPeakToSpinBox.setMaximum(255)
        self.ui.plotBackFromSpinBox.setMaximum(255)
        self.ui.plotBackToSpinBox.setMaximum(255)

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

        [peak1, peak2] = _peak
        [back1, back2] = _back

        back_flag = RefRed.utilities.str2bool(self.data.back_flag)
        self.ui.plot_back_flag.setChecked(back_flag)

        peak1 = int(peak1)
        peak2 = int(peak2)
        back1 = int(back1)
        back2 = int(back2)

        self._prev_peak1 = peak1
        self._prev_peak2 = peak2
        self._prev_back1 = back1
        self._prev_back2 = back2

        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_view_interval

        # Plot
        ui_plot2 = self.ui.plot_counts_vs_pixel
        ui_plot2.canvas.ax.plot(xaxis, _yaxis)
        ui_plot2.canvas.ax.set_xlabel("Pixels")
        ui_plot2.canvas.ax.set_ylabel("Counts")
        if self.isPlotLog:
            ui_plot2.canvas.ax.set_yscale("log")
        else:
            ui_plot2.canvas.ax.set_yscale("linear")
        ui_plot2.canvas.ax.set_xlim(0, self.nbr_pixel_y_axis - 1)

        ui_plot2.canvas.ax.axvline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        ui_plot2.canvas.ax.axvline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if back_flag:
            ui_plot2.canvas.ax.axvline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot2.canvas.ax.axvline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])
        ui_plot2.draw()

        # Plot peak and back
        self.set_peak_value(peak1, peak2)
        self.set_back_value(back1, back2)

        ui_plot2.logtogy.connect(self.logtoggleylog)

    def logtoggleylog(self, status):
        self.isPlotLog = status == "log"

    def plot_back_flag_clicked(self, status):
        self.data.back_flag = status
        self.update_plots()
        self.update_back_flag_widgets()
        self.check_peak_back_input_validity()

    def update_back_flag_widgets(self):
        status_flag = self.ui.plot_back_flag.isChecked()
        self.ui.plotBackFromSpinBox.setEnabled(status_flag)
        self.ui.plotBackToSpinBox.setEnabled(status_flag)

    def set_peak_value(self, peak1, peak2):
        self.ui.plotPeakFromSpinBox.setValue(peak1)
        self.ui.plotPeakToSpinBox.setValue(peak2)
        self.check_peak_back_input_validity()

    def set_back_value(self, back1, back2):
        self.ui.plotBackFromSpinBox.setValue(back1)
        self.ui.plotBackToSpinBox.setValue(back2)
        self.check_peak_back_input_validity()

    # peak1
    def update_peak1(self, value, updatePlotSpinbox=True):
        if updatePlotSpinbox:
            self.ui.plotPeakFromSpinBox.setValue(value)
        self._prev_peak1 = value

    def plot_peak_from_spinbox_signal(self):
        value = self.ui.plotPeakFromSpinBox.value()
        if value == self._prev_peak1:
            return
        self.update_peak1(value, updatePlotSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    # peak2
    def update_peak2(self, value, updatePlotSpinbox=True):
        if updatePlotSpinbox:
            self.ui.plotPeakToSpinBox.setValue(value)
        self._prev_peak2 = value
        self.check_peak_back_input_validity()

    def plot_peak_to_spinbox_signal(self):
        value = self.ui.plotPeakToSpinBox.value()
        if value == self._prev_peak2:
            return
        self.update_peak2(value, updatePlotSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    # back1
    def update_back1(self, value, updatePlotSpinbox=True):
        if updatePlotSpinbox:
            self.ui.plotBackFromSpinBox.setValue(value)
        self._prev_back1 = value
        self.check_peak_back_input_validity()

    def plot_back_from_spinbox_signal(self):
        value = self.ui.plotBackFromSpinBox.value()
        if value == self._prev_back1:
            return
        self.update_back1(value, updatePlotSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    # back2
    def update_back2(self, value, updatePlotSpinbox=True):
        if updatePlotSpinbox:
            self.ui.plotBackToSpinBox.setValue(value)
        self._prev_back2 = value
        self.check_peak_back_input_validity()

    def plot_back_to_spinbox_signal(self):
        value = self.ui.plotBackToSpinBox.value()
        if value == self._prev_back2:
            return
        self.update_back2(value, updatePlotSpinbox=False)
        self.sort_peak_back_input()
        self.check_peak_back_input_validity()
        self.update_plots()

    def update_plots(self):
        self.update_counts_vs_pixel_plot()

    def update_counts_vs_pixel_plot(self):
        self.ui.plot_counts_vs_pixel.clear()

        peak1 = self.ui.plotPeakFromSpinBox.value()
        peak2 = self.ui.plotPeakToSpinBox.value()
        back1 = self.ui.plotBackFromSpinBox.value()
        back2 = self.ui.plotBackToSpinBox.value()

        _yaxis = self.ycountsdata

        ui_plot2 = self.ui.plot_counts_vs_pixel
        ui_plot2.canvas.ax.plot(self.xaxis, _yaxis)
        ui_plot2.canvas.ax.set_xlabel("Pixels")
        ui_plot2.canvas.ax.set_ylabel("Counts")
        if self.isPlotLog:
            ui_plot2.canvas.ax.set_yscale("log")
        else:
            ui_plot2.canvas.ax.set_yscale("linear")

        ui_plot2.canvas.ax.axvline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        ui_plot2.canvas.ax.axvline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if self.data.back_flag:
            ui_plot2.canvas.ax.axvline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot2.canvas.ax.axvline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_view_interval
        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])

        ui_plot2.canvas.draw_idle()

    def closeEvent(self, event=None):
        peak1 = self.ui.plotPeakFromSpinBox.value()
        peak2 = self.ui.plotPeakToSpinBox.value()
        back1 = self.ui.plotBackFromSpinBox.value()
        back2 = self.ui.plotBackToSpinBox.value()
        backFlag = self.ui.plot_back_flag.isChecked()

        big_table_data = self.parent.big_table_data

        _data = big_table_data[self.row, self.col]
        _data.peak = [str(peak1), str(peak2)]
        _data.back = [str(back1), str(back2)]
        _data.back_flag = backFlag

        big_table_data[self.row, self.col] = _data

        if self.is_row_with_highest_q:
            _data = big_table_data[0, 0]
            index = 0
            while _data is not None:
                big_table_data[index, 0] = _data
                _data = big_table_data[index + 1, 0]
                index += 1

        self.parent.big_table_data = big_table_data

        if self.data_type == "data":
            self.parent.ui.peakFromValue.setValue(peak1)
            self.parent.ui.peakToValue.setValue(peak2)

            self.parent.ui.backFromValue.setValue(back1)
            self.parent.ui.backFromValue.setEnabled(backFlag)
            self.parent.ui.backToValue.setValue(back2)
            self.parent.ui.backToValue.setEnabled(backFlag)

            self.parent.ui.dataBackgroundFlag.setChecked(backFlag)
            self.parent.ui.backBoundariesLabel.setEnabled(backFlag)

        else:
            self.parent.ui.normPeakFromValue.setValue(peak1)
            self.parent.ui.normPeakToValue.setValue(peak2)
            self.parent.ui.normBackFromValue.setValue(back1)
            self.parent.ui.normBackToValue.setValue(back2)
            self.parent.ui.normBackgroundFlag.setChecked(backFlag)
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
