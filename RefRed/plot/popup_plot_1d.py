import bisect
import os
from pathlib import Path
from typing import Optional

from qtpy.QtWidgets import QDialog, QFileDialog

import RefRed.colors
import RefRed.utilities
from RefRed.calculations.lr_data import LRData
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.gui_handling.observer import SpinBoxObserver
from RefRed.interfaces import load_ui
from RefRed.plot.background_settings import BackgroundSettingsView, backgrounds_settings
from RefRed.plot.display_plots import DisplayPlots


class PopupPlot1d(QDialog):
    parent = None
    data_type = "data"
    data = None
    is_data = True
    row = 0
    col = 0  # 0 for data, 1 for norm

    _open_instances = []  # registry of PopupPlot1d instances
    yaxis = None
    peak = None
    back = None

    _prev_peak1 = -1
    _prev_peak2 = -1
    _prev_back1 = -1
    _prev_back2 = -1
    _prev_back2_from = -1
    _prev_back2_to = -1

    isPlotLog = True

    nbr_pixel_y_axis = 304

    def __init__(self, parent=None, data_type: str = "data", data: Optional[LRData] = None, row: int = 0):
        self.data_type = data_type
        self.parent = parent
        # argument data is optional for historical reasons but it should always be passed, never use the default value
        assert data is not None
        self.data = data
        self.row = row
        self.col = 0 if data_type == "data" else 1
        self.is_data = True if data_type == "data" else False
        self.is_row_with_highest_q = self.is_row_with_higest_q()
        self.spinbox_observer = SpinBoxObserver()  # backup for spinbox values
        self.background_settings = backgrounds_settings[data_type]
        QDialog.__init__(self, parent=parent)
        self.setWindowModality(False)
        self._open_instances.append(self)
        self.ui = load_ui("plot_dialog_refl_interface.ui", self)

        self.setWindowTitle("Counts vs Y pixel")

        self.ui.plot_counts_vs_pixel.leaveFigure.connect(self.leave_plot_counts_vs_pixel)
        self.ui.plot_counts_vs_pixel.toolbar.homeClicked.connect(self.home_plot_counts_vs_pixel)
        self.ui.plot_counts_vs_pixel.toolbar.exportClicked.connect(self.export_counts_vs_pixel)

        # enable/disable background spinboxes based on the background settings
        self.background_settings.control_spinboxes_visibility(
            parent=self.ui,
            first_background=("plotBackFromSpinBox", "plotBackToSpinBox"),
            second_background=("plotBack2FromSpinBox", "plotBack2ToSpinBox"),
        )
        # hide/show the background lines on the plots based on the background settings
        self.background_settings.signal_first_background.connect(self.plot_back_flag_clicked)
        self.background_settings.signal_second_background.connect(self.plot_back_flag_clicked)

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

        back1 = self.ui.plotBack2FromSpinBox.value()
        back2 = self.ui.plotBack2ToSpinBox.value()
        back_min = min([back1, back2])
        if back_min != back1:
            self.ui.plotBack2FromSpinBox.setValue(back2)
            self.ui.plotBack2ToSpinBox.setValue(back1)

    def reset_max_ui_value(self):
        self.ui.plotPeakFromSpinBox.setMaximum(self.nbr_pixel_y_axis)
        self.ui.plotPeakToSpinBox.setMaximum(self.nbr_pixel_y_axis)
        self.ui.plotBackFromSpinBox.setMaximum(self.nbr_pixel_y_axis)
        self.ui.plotBackToSpinBox.setMaximum(self.nbr_pixel_y_axis)
        self.ui.plotBack2FromSpinBox.setMaximum(self.nbr_pixel_y_axis)
        self.ui.plotBack2ToSpinBox.setMaximum(self.nbr_pixel_y_axis)

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

        [peak1, peak2] = _peak  # lower and upper boundaries for the peak
        [back1, back2] = _back  # lower and upper boundaries for the background

        peak1 = int(peak1)
        peak2 = int(peak2)
        back1 = int(back1)
        back2 = int(back2)
        back2_from, back2_to = [int(x) for x in self.data.back2]  # boundaries for the second background

        self._prev_peak1 = peak1  # backup for lower peak boundary
        self._prev_peak2 = peak2  # backup for upper peak boundary
        self._prev_back1 = back1  # backup for lower background boundary
        self._prev_back2 = back2  # backup for upper background boundary
        self._prev_back2_from = back2_from  # backup for lower background boundary
        self._prev_back2_to = back2_to  # backup for upper background boundary

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

        if self.background_settings.subtract_background:
            ui_plot2.canvas.ax.axvline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot2.canvas.ax.axvline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)
            if self.background_settings.two_backgrounds:
                ui_plot2.canvas.ax.axvline(back2_from, color=RefRed.colors.BACK2_SELECTION_COLOR)
                ui_plot2.canvas.ax.axvline(back2_to, color=RefRed.colors.BACK2_SELECTION_COLOR)

        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])
        ui_plot2.draw()

        # Plot peak and back
        self.set_peak_value(peak1, peak2)
        self.set_back_value(back1, back2)
        self.set_back_value(back2_from, back2_to, spinbox_from="plotBack2FromSpinBox", spinbox_to="plotBack2ToSpinBox")

        ui_plot2.logtogy.connect(self.logtoggleylog)

    def logtoggleylog(self, status):
        self.isPlotLog = status == "log"

    def display_background_settings(self, *args, **kwargs):
        BackgroundSettingsView(parent=self, run_type=self.data_type).show()

    def plot_back_flag_clicked(self, _):
        self.update_plots()

    def set_peak_value(self, peak1, peak2):
        self.ui.plotPeakFromSpinBox.setValue(peak1)
        self.ui.plotPeakToSpinBox.setValue(peak2)

    def set_back_value(
        self,
        boundary_from,
        boundary_to,
        spinbox_from: str = "plotBackFromSpinBox",
        spinbox_to: str = "plotBackToSpinBox",
    ):
        assert boundary_from <= boundary_to
        getattr(self.ui, spinbox_from).setValue(boundary_from)
        getattr(self.ui, spinbox_to).setValue(boundary_to)

    def act_upon_changed_boundaries(self):
        r"""Actions after User changes any boundary value (peak or background) in the QSpinBox widgets"""
        self.sort_peak_back_input()
        self.update_plots()

    def plot_peak_from_spinbox_value_changed(self):
        r"""Slot associated to signal QSpinBox.valueChanged(int) for QSpinBox plotPeakFromSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox
        """
        if self.spinbox_observer.quantum_change(self.ui.plotPeakFromSpinBox):
            self.act_upon_changed_boundaries()

    def plot_peak_to_spinbox_value_changed(self):
        r"""Slot associated to signal QSpinBox.valueChanged(int) for QSpinBox plotPeakToSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox
        """
        if self.spinbox_observer.quantum_change(self.ui.plotPeakToSpinBox):
            self.act_upon_changed_boundaries()

    def plot_back_from_spinbox_value_changed(self):
        r"""Slot associated to signal QSpinBox.valueChanged(int) for QSpinBox plotBackFromSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox
        """
        if self.spinbox_observer.quantum_change(self.ui.plotBackFromSpinBox):
            self.act_upon_changed_boundaries()

    def plot_back_to_spinbox_value_changed(self):
        r"""Slot associated to signal QSpinBox.valueChanged(int) for QSpinBox plotBackToSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox
        """
        if self.spinbox_observer.quantum_change(self.ui.plotBackToSpinBox):
            self.act_upon_changed_boundaries()

    def plot_back2_from_spinbox_value_changed(self):
        r"""Slot associated to signal QSpinBox.valueChanged(int) for QSpinBox plotBack2FromSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox
        """
        if self.spinbox_observer.quantum_change(self.ui.plotBack2FromSpinBox):
            self.act_upon_changed_boundaries()

    def plot_back2_to_spinbox_value_changed(self):
        r"""Slot associated to signal QSpinBox.valueChanged(int) for QSpinBox plotBack2ToSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox
        """
        if self.spinbox_observer.quantum_change(self.ui.plotBack2ToSpinBox):
            self.act_upon_changed_boundaries()

    def update_plots(self):
        self.update_counts_vs_pixel_plot()

    def update_counts_vs_pixel_plot(self):
        self.ui.plot_counts_vs_pixel.clear()

        peak1 = self.ui.plotPeakFromSpinBox.value()
        peak2 = self.ui.plotPeakToSpinBox.value()
        back1 = self.ui.plotBackFromSpinBox.value()
        back2 = self.ui.plotBackToSpinBox.value()
        back2_from = self.ui.plotBack2FromSpinBox.value()
        back2_to = self.ui.plotBack2ToSpinBox.value()

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

        if backgrounds_settings[self.data_type].subtract_background:
            ui_plot2.canvas.ax.axvline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            ui_plot2.canvas.ax.axvline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)
            if backgrounds_settings[self.data_type].two_backgrounds:
                ui_plot2.canvas.ax.axvline(back2_from, color=RefRed.colors.BACK2_SELECTION_COLOR)
                ui_plot2.canvas.ax.axvline(back2_to, color=RefRed.colors.BACK2_SELECTION_COLOR)

        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yi_view_interval
        self.ui.plot_counts_vs_pixel.canvas.ax.set_xlim([ymin, ymax])
        self.ui.plot_counts_vs_pixel.canvas.ax.set_ylim([xmin, xmax])

        ui_plot2.canvas.draw_idle()

    def closeEvent(self, event=None):
        peak1 = self.ui.plotPeakFromSpinBox.value()
        peak2 = self.ui.plotPeakToSpinBox.value()
        back1 = self.ui.plotBackFromSpinBox.value()
        back2 = self.ui.plotBackToSpinBox.value()
        back2_from = self.ui.plotBack2FromSpinBox.value()
        back2_to = self.ui.plotBack2ToSpinBox.value()

        big_table_data = self.parent.big_table_data

        _data = big_table_data[self.row, self.col]
        _data.peak = [str(peak1), str(peak2)]
        _data.back = [str(back1), str(back2)]
        _data.back2 = [str(back2_from), str(back2_to)]

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
            self.parent.ui.backToValue.setValue(back2)
            self.parent.ui.back2FromValue.setValue(back2_from)
            self.parent.ui.back2ToValue.setValue(back2_to)
        else:
            self.parent.ui.normPeakFromValue.setValue(peak1)
            self.parent.ui.normPeakToValue.setValue(peak2)
            self.parent.ui.normBackFromValue.setValue(back1)
            self.parent.ui.normBackToValue.setValue(back2)
            self.parent.ui.normBack2FromValue.setValue(back2_from)
            self.parent.ui.normBack2ToValue.setValue(back2_to)

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
        self._open_instances.remove(self)  # remove this plot from the registry
