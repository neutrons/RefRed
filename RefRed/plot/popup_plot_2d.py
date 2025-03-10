import os
from pathlib import Path

from qtpy.QtWidgets import QDialog, QFileDialog

import RefRed.colors
import RefRed.utilities
from RefRed.gui_handling.auto_tof_range_radio_button_handler import AutoTofRangeRadioButtonHandler
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.gui_handling.observer import SpinBoxObserver
from RefRed.interfaces import load_ui
from RefRed.plot.background_settings import BackgroundSettingsView, backgrounds_settings
from RefRed.plot.display_plots import DisplayPlots


class PopupPlot2d(QDialog):
    parent = None
    _open_instances = []  # registry of PopupPlot2d instances
    data = None
    data_type = "data"
    row = 0

    manual_min_tof = None
    manual_max_tof = None

    auto_min_tof = None
    auto_max_tof = None

    def __init__(self, parent=None, data_type="data", data=None, row=0):
        self.parent = parent
        self.data = data
        self.data_type = data_type
        self.row = row
        self.col = 0 if data_type == "data" else 1
        self.is_data = True if data_type == "data" else False
        self.is_row_with_highest_q = self.is_row_with_higest_q()
        self.spinbox_observer = SpinBoxObserver()  # backup for spinbox values
        self.background_settings = backgrounds_settings[data_type]
        QDialog.__init__(self, parent=parent)
        self.setWindowModality(False)
        self._open_instances.append(self)
        self.ui = load_ui("plot2d_dialog_refl_interface.ui", self)

        self.setWindowTitle("Detector and  Pixel vs TOF  views")
        self.init_gui()
        self.populate_widgets()

        self.update_detector_tab_plot()
        self.update_pixel_vs_tof_tab_plot()

        self.ui.y_pixel_vs_tof_plot.leaveFigure.connect(self.leave_figure_plot)
        self.ui.y_pixel_vs_tof_plot.toolbar.homeClicked.connect(self.home_clicked_plot)
        self.ui.y_pixel_vs_tof_plot.toolbar.exportClicked.connect(self.export_yt)

        self.ui.detector_plot.leaveFigure.connect(self.leave_figure_detector_plot)
        self.ui.detector_plot.toolbar.homeClicked.connect(self.home_clicked_detector_plot)
        self.ui.detector_plot.toolbar.exportClicked.connect(self.export_detector_view)

    def is_row_with_higest_q(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        return o_gui_utility.is_row_with_highest_q()

    def export_yt(self):
        _active_data = self.data
        run_number = _active_data.run_number
        path = Path(self.parent.path_ascii)
        default_filename = path / f"REFL_{run_number}_2dPxVsTof.txt"
        caption = "Create 2D Pixel VS TOF"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            caption,
            str(default_filename),
        )
        if filename:
            self.parent.path_ascii = os.path.dirname(filename)
            image = _active_data.ytofdata
            RefRed.utilities.output_2d_ascii_file(filename, image)

    def export_detector_view(self):
        _active_data = self.data
        run_number = _active_data.run_number
        path = Path(self.parent.path_ascii)
        default_filename = path / f"REFL_{run_number}_2dDetectorView.txt"
        caption = "Create 2D Y Pixel VS X Pixel (Detector View)"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            caption,
            str(default_filename),
        )
        if filename:
            self.parent.path_ascii = os.path.dirname(filename)
            image = _active_data.xydata
            RefRed.utilities.output_2d_ascii_file(filename, image)

    def leave_figure_plot(self):
        [xmin, xmax] = self.ui.y_pixel_vs_tof_plot.canvas.ax.xaxis.get_view_interval()
        [ymin, ymax] = self.ui.y_pixel_vs_tof_plot.canvas.ax.yaxis.get_view_interval()
        self.ui.y_pixel_vs_tof_plot.canvas.ax.xaxis.set_data_interval(xmin, xmax)
        self.ui.y_pixel_vs_tof_plot.canvas.ax.yaxis.set_data_interval(ymin, ymax)
        self.ui.y_pixel_vs_tof_plot.draw()
        self.data.all_plot_axis.yt_view_interval = [xmin, xmax, ymin, ymax]

    def home_clicked_plot(self):
        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yt_data_interval
        self.ui.y_pixel_vs_tof_plot.canvas.ax.set_xlim([xmin, xmax])
        self.ui.y_pixel_vs_tof_plot.canvas.ax.set_ylim([ymin, ymax])
        self.ui.y_pixel_vs_tof_plot.draw()

    def leave_figure_detector_plot(self):
        [xmin, xmax] = self.ui.detector_plot.canvas.ax.xaxis.get_view_interval()
        [ymin, ymax] = self.ui.detector_plot.canvas.ax.yaxis.get_view_interval()
        self.ui.detector_plot.canvas.ax.xaxis.set_data_interval(xmin, xmax)
        self.ui.detector_plot.canvas.ax.yaxis.set_data_interval(ymin, ymax)
        self.ui.detector_plot.draw()
        self.data.all_plot_axis.detector_view_interval = [xmin, xmax, ymin, ymax]

    def home_clicked_detector_plot(self):
        [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.detector_data_interval
        self.ui.detector_plot.canvas.ax.set_xlim([xmin, xmax])
        self.ui.detector_plot.canvas.ax.set_ylim([ymin, ymax])
        self.ui.detector_plot.draw()

    def update_detector_tab_plot(self):
        self.ui.detector_plot.clear()
        xydata = self.data.xydata
        self.ui.detector_plot.draw()

        [ymax, xmax] = xydata.shape
        self.ui.detector_plot.imshow(xydata, log=True, aspect="auto", origin="lower", extent=[0, xmax, 0, ymax])
        self.ui.detector_plot.set_xlabel("x (pixel)")
        self.ui.detector_plot.set_ylabel("y (pixel)")

        [
            lowres1,
            lowres2,
            lowresFlag,
            peak1,
            peak2,
            back1,
            back2,
            back2_from,
            back2_to,
        ] = self.retrieveLowResPeakBack()

        if lowresFlag:
            self.ui.detector_plot.canvas.ax.axvline(lowres1, color=RefRed.colors.LOWRESOLUTION_SELECTION_COLOR)
            self.ui.detector_plot.canvas.ax.axvline(lowres2, color=RefRed.colors.LOWRESOLUTION_SELECTION_COLOR)

        self.ui.detector_plot.canvas.ax.axhline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        self.ui.detector_plot.canvas.ax.axhline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if self.background_settings.subtract_background:
            self.ui.detector_plot.canvas.ax.axhline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            self.ui.detector_plot.canvas.ax.axhline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)
            if self.background_settings.two_backgrounds:
                self.ui.detector_plot.canvas.ax.axhline(back2_from, color=RefRed.colors.BACK2_SELECTION_COLOR)
                self.ui.detector_plot.canvas.ax.axhline(back2_to, color=RefRed.colors.BACK2_SELECTION_COLOR)

        if self.data.all_plot_axis.detector_data_interval is None:
            self.ui.detector_plot.draw()
            [xmin, xmax] = self.ui.detector_plot.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.ui.detector_plot.canvas.ax.yaxis.get_view_interval()
            self.data.all_plot_axis.detector_data_interval = [xmin, xmax, ymin, ymax]
            self.data.all_plot_axis.detector_view_interval = [xmin, xmax, ymin, ymax]
            self.ui.detector_plot.toolbar.home_settings = [xmin, xmax, ymin, ymax]
        else:
            [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.detector_view_interval
            self.ui.detector_plot.canvas.ax.set_xlim([xmin, xmax])
            self.ui.detector_plot.canvas.ax.set_ylim([ymin, ymax])
            self.ui.detector_plot.draw()

    def update_pixel_vs_tof_tab_plot(self):
        ytof = self.data.ytofdata
        tof_axis = self.data.tof_axis_auto_with_margin
        tof_from = tof_axis[0]
        tof_to = tof_axis[-1]
        if tof_from > 1000:  # stay in ms
            tof_from /= 1000.0
            tof_to /= 1000.0
        pixel_from = 0
        pixel_to = self.data.y.shape[0] - 1

        self.ui.y_pixel_vs_tof_plot.clear()
        self.ui.y_pixel_vs_tof_plot.imshow(
            ytof,
            log=True,
            aspect="auto",
            origin="lower",
            extent=[tof_from, tof_to, pixel_from, pixel_to],
        )
        self.ui.y_pixel_vs_tof_plot.set_xlabel("t (ms)")
        self.ui.y_pixel_vs_tof_plot.set_ylabel("y (pixel)")

        [tmin, tmax, peak1, peak2, back1, back2, back2_from, back2_to] = self.retrieveTofPeakBack()

        self.ui.y_pixel_vs_tof_plot.canvas.ax.axvline(tmin, color=RefRed.colors.TOF_SELECTION_COLOR)
        self.ui.y_pixel_vs_tof_plot.canvas.ax.axvline(tmax, color=RefRed.colors.TOF_SELECTION_COLOR)

        self.ui.y_pixel_vs_tof_plot.canvas.ax.axhline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        self.ui.y_pixel_vs_tof_plot.canvas.ax.axhline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if self.background_settings.subtract_background:
            self.ui.y_pixel_vs_tof_plot.canvas.ax.axhline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            self.ui.y_pixel_vs_tof_plot.canvas.ax.axhline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)
            if self.background_settings.two_backgrounds:
                self.ui.y_pixel_vs_tof_plot.canvas.ax.axhline(back2_from, color=RefRed.colors.BACK2_SELECTION_COLOR)
                self.ui.y_pixel_vs_tof_plot.canvas.ax.axhline(back2_to, color=RefRed.colors.BACK2_SELECTION_COLOR)

        if self.data.all_plot_axis.yt_data_interval is None:
            self.ui.y_pixel_vs_tof_plot.canvas.ax.set_ylim(0, pixel_to)
            self.ui.y_pixel_vs_tof_plot.canvas.draw_idle()
            [
                xmin,
                xmax,
            ] = self.ui.y_pixel_vs_tof_plot.canvas.ax.xaxis.get_view_interval()
            [
                ymin,
                ymax,
            ] = self.ui.y_pixel_vs_tof_plot.canvas.ax.yaxis.get_view_interval()
            self.data.all_plot_axis.yt_data_interval = [xmin, xmax, ymin, ymax]
            self.data.all_plot_axis.yt_view_interval = [xmin, xmax, ymin, ymax]
            self.ui.y_pixel_vs_tof_plot.toolbar.home_settings = [xmin, xmax, ymin, ymax]
        else:
            [xmin, xmax, ymin, ymax] = self.data.all_plot_axis.yt_view_interval
            self.ui.y_pixel_vs_tof_plot.canvas.ax.set_xlim([xmin, xmax])
            self.ui.y_pixel_vs_tof_plot.canvas.ax.set_ylim([ymin, ymax])
            self.ui.y_pixel_vs_tof_plot.draw()

    def retrievePeakBack(self):
        return [
            self.ui.plot2dPeakFromSpinBox.value(),
            self.ui.plot2dPeakToSpinBox.value(),
            self.ui.plot2dBackFromValue.value(),
            self.ui.plot2dBackToValue.value(),
            self.ui.plot2dBack2FromValue.value(),
            self.ui.plot2dBack2ToValue.value(),
        ]

    def retrieveTofPeakBack(self):
        tmin = float(self.ui.tof_from.text())
        tmax = float(self.ui.tof_to.text())
        return [tmin, tmax] + self.retrievePeakBack()

    def retrieveLowRes(self):
        return [self.ui.low_res1.value(), self.ui.low_res2.value(), self.ui.low_res_flag.isChecked()]

    def retrieveLowResPeakBack(self):
        return self.retrieveLowRes() + self.retrievePeakBack()

    def init_gui(self):
        # enable/disable background spinboxes based on the background settings
        self.background_settings.control_spinboxes_visibility(
            self.ui,
            first_background=("plot2dBackFromValue", "plot2dBackToValue"),
            second_background=("plot2dBack2FromValue", "plot2dBack2ToValue"),
        )
        # hide/show the background lines on the plots based on the background settings
        self.background_settings.signal_first_background.connect(self.update_plots)
        self.background_settings.signal_second_background.connect(self.update_plots)

    def populate_widgets(self):
        _data = self.data

        peak = _data.peak
        back = _data.back
        low_res = _data.low_res
        low_res_flag = RefRed.utilities.str2bool(_data.low_res_flag)
        tof_auto_flag = RefRed.utilities.str2bool(_data.tof_auto_flag)

        tof_range_auto = _data.tof_range_auto
        tof_range = _data.tof_range

        # make sure we are in ms
        tof_range_auto_min = float(tof_range_auto[0])
        tof_range_auto_max = float(tof_range_auto[1])
        if tof_range_auto_min > 1000:
            tof_range_auto_min /= 1000.0
            tof_range_auto_max /= 1000.0
        self.auto_max_tof = tof_range_auto_max
        self.auto_min_tof = tof_range_auto_min

        tof_range_manual_min = float(tof_range[0])
        tof_range_manual_max = float(tof_range[1])
        if tof_range_manual_min > 1000:
            tof_range_manual_min /= 1000.0
            tof_range_manual_max /= 1000.0
        self.manual_max_tof = tof_range_manual_max
        self.manual_min_tof = tof_range_manual_min

        if not tof_auto_flag:
            self.ui.tof_auto_flag.setChecked(False)
            self.ui.tof_manual_flag.setChecked(True)
        self.manual_auto_tof_clicked()

        self.ui.plot2dPeakFromSpinBox.setValue(int(peak[0]))
        self.ui.plot2dPeakToSpinBox.setValue(int(peak[1]))

        self.ui.plot2dBackFromValue.setValue(int(back[0]))
        self.ui.plot2dBackToValue.setValue(int(back[1]))

        self.ui.plot2dBack2FromValue.setValue(int(_data.back2[0]))
        self.ui.plot2dBack2ToValue.setValue(int(_data.back2[1]))

        self.activate_or_not_back_widgets()

        self.ui.low_res1.setValue(int(low_res[0]))
        self.ui.low_res2.setValue(int(low_res[1]))
        self.activate_or_not_low_res_widgets(low_res_flag)

    def activate_or_not_back_widgets(self):
        self.background_settings.control_spinboxes_visibility(
            parent=self.ui,
            first_background=("plot2dBackFromValue", "plot2dBackToValue"),
            second_background=("plot2dBack2FromValue", "plot2dBack2ToValue"),
        )
        self.update_plots()

    def activate_or_not_low_res_widgets(self, low_res_flag):
        self.ui.low_res1.setEnabled(low_res_flag)
        self.ui.low_res2.setEnabled(low_res_flag)
        self.ui.low_res1_label.setEnabled(low_res_flag)
        self.ui.low_res2_label.setEnabled(low_res_flag)
        self.update_detector_tab_plot()

    def sort_peak_back_input(self):
        peak1 = self.ui.plot2dPeakFromSpinBox.value()
        peak2 = self.ui.plot2dPeakToSpinBox.value()
        peak_min = min([peak1, peak2])
        # peak_max = max([peak1, peak2])
        if peak_min != peak1:
            self.ui.plot2dPeakFromSpinBox.setValue(peak2)
            self.ui.plot2dPeakToSpinBox.setValue(peak1)

        back1 = self.ui.plot2dBackFromValue.value()
        back2 = self.ui.plot2dBackToValue.value()
        back_min = min([back1, back2])
        if back_min != back1:
            self.ui.plot2dBackFromValue.setValue(back2)
            self.ui.plot2dBackToValue.setValue(back1)

        back1 = self.ui.plot2dBack2FromValue.value()
        back2 = self.ui.plot2dBack2ToValue.value()
        back_min = min([back1, back2])
        if back_min != back1:
            self.ui.plot2dBack2FromValue.setValue(back2)
            self.ui.plot2dBack2ToValue.setValue(back1)

    def update_plots(self):
        self.update_pixel_vs_tof_tab_plot()
        self.update_detector_tab_plot()

    def manual_input_peak1(self):
        self.sort_peak_back_input()
        self.update_plots()

    def manual_input_peak2(self):
        self.sort_peak_back_input()
        self.update_plots()

    def plot2d_peak_from_spinbox_value_changed(self):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox plot2dPeakFromSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.plot2dPeakFromSpinBox):
            self.manual_input_peak1()

    def plot2d_peak_to_spinbox_value_changed(self):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox plot2dPeakToSpinBox.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.plot2dPeakToSpinBox):
            self.manual_input_peak2()

    def manual_input_background(self):
        self.sort_peak_back_input()
        self.update_plots()

    def display_background_settings(self, *args, **kwargs):
        BackgroundSettingsView(parent=self, run_type=self.data_type).show()

    def plot2d_back_from_spinbox_value_changed(self):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox plot2dBackFromValue.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.plot2dBackFromValue):
            self.manual_input_background()

    def plot2d_back_to_spinbox_value_changed(self):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox plot2dBackToValue.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.plot2dBackToValue):
            self.manual_input_background()

    def plot2d_back2_from_spinbox_value_changed(self):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox plot2dBack2FromValue.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.plot2dBack2FromValue):
            self.manual_input_background()

    def plot2d_back2_to_spinbox_value_changed(self):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox plot2dBack2ToValue.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.plot2dBack2ToValue):
            self.manual_input_background()

    def manual_input_of_low_res_field(self):
        value1 = self.ui.low_res1.value()
        value2 = self.ui.low_res2.value()
        value_min = min([value1, value2])
        value_max = max([value1, value2])
        self.ui.low_res1.setValue(value_min)
        self.ui.low_res2.setValue(value_max)
        self.ui.detector_plot()

    def manual_input_of_tof_field(self):
        tof1 = float(self.ui.tof_from.text())
        tof2 = float(self.ui.tof_to.text())
        tof_min = min([tof1, tof2])
        tof_max = max([tof1, tof2])
        str_tof_min = "%.2f" % tof_min
        str_tof_max = "%.2f" % tof_max
        self.ui.tof_from.setText(str_tof_min)
        self.ui.tof_to.setText(str_tof_max)
        self.manual_min_tof = tof_min
        self.manual_max_tof = tof_max
        self.update_pixel_vs_tof_tab_plot()

    def manual_auto_tof_clicked(self):
        isManualChecked = self.ui.tof_manual_flag.isChecked()
        self.activate_tof_widgets(isManualChecked)
        if isManualChecked:
            _from_value = "%.2f" % self.manual_min_tof
            _to_value = "%.2f" % self.manual_max_tof
        else:
            _from_value = "%.2f" % self.auto_min_tof
            _to_value = "%.2f" % self.auto_max_tof
        self.ui.tof_from.setText(_from_value)
        self.ui.tof_to.setText(_to_value)

    def activate_tof_widgets(self, status):
        self.ui.tof_from.setEnabled(status)
        self.ui.tof_to.setEnabled(status)
        self.ui.tof_from_label.setEnabled(status)
        self.ui.tof_to_label.setEnabled(status)
        self.ui.tof_from_units.setEnabled(status)
        self.ui.tof_to_units.setEnabled(status)
        self.update_pixel_vs_tof_tab_plot()

    def closeEvent(self, event=None):
        [lowres1, lowres2, lowresFlag] = self.retrieveLowRes()
        [tof1, tof2, peak1, peak2, back1, back2, back2_from, back2_to] = self.retrieveTofPeakBack()
        tof_auto_switch = self.ui.tof_auto_flag.isChecked()

        big_table_data = self.parent.big_table_data

        _data = big_table_data[self.row, self.col]
        _data.peak = [str(peak1), str(peak2)]
        _data.back = [str(back1), str(back2)]
        _data.back2 = [str(back2_from), str(back2_to)]

        _data.tof_range_auto = [self.auto_min_tof * 1000, self.auto_max_tof * 1000]
        _data.tof_range = [self.manual_min_tof * 1000, self.manual_max_tof * 1000]
        _data.tof_range_manual = _data.tof_range
        _data.tof_range_auto_flag = tof_auto_switch
        _data.tof_auto_flag = tof_auto_switch

        _data.low_res = [str(lowres1), str(lowres2)]
        _data.low_res_flag = lowresFlag

        big_table_data[self.row, self.col] = _data
        if self.is_row_with_highest_q:
            _data = big_table_data[0, 0]
            index = 0
            while _data is not None:
                big_table_data[index, 0] = _data
                _data = big_table_data[index + 1, 0]
                index += 1

        self.parent.big_table_data = big_table_data

        # tof
        o_gui_utility = GuiUtility(parent=self.parent)
        o_gui_utility.set_auto_tof_range_radio_button(status=tof_auto_switch)
        self.parent.ui.TOFmanualFromValue.setText("%.2f" % tof1)
        self.parent.ui.TOFmanualToValue.setText("%.2f" % tof2)

        if self.data_type == "data":
            self.parent.ui.peakFromValue.setValue(peak1)
            self.parent.ui.peakToValue.setValue(peak2)

            self.parent.ui.backFromValue.setValue(back1)
            self.parent.ui.backToValue.setValue(back2)

            self.parent.ui.back2FromValue.setValue(back2_from)
            self.parent.ui.back2ToValue.setValue(back2_to)

            self.parent.ui.dataLowResFromValue.setValue(lowres1)
            self.parent.ui.dataLowResToValue.setValue(lowres2)

            self.parent.ui.dataLowResFromLabel.setEnabled(lowresFlag)
            self.parent.ui.dataLowResFromValue.setEnabled(lowresFlag)

            self.parent.ui.dataLowResToLabel.setEnabled(lowresFlag)
            self.parent.ui.dataLowResToValue.setEnabled(lowresFlag)
        else:
            self.parent.ui.normPeakFromValue.setValue(peak1)
            self.parent.ui.normPeakToValue.setValue(peak2)

            self.parent.ui.normBackFromValue.setValue(back1)
            self.parent.ui.normBackToValue.setValue(back2)

            self.parent.ui.normBack2FromValue.setValue(back2_from)
            self.parent.ui.normBack2ToValue.setValue(back2_to)

            self.parent.ui.normLowResFromValue.setValue(lowres1)
            self.parent.ui.normLowResToValue.setValue(lowres2)

            self.parent.ui.normLowResFromLabel.setEnabled(lowresFlag)
            self.parent.ui.normLowResFromValue.setEnabled(lowresFlag)

            self.parent.ui.normLowResToLabel.setEnabled(lowresFlag)
            self.parent.ui.normLowResToValue.setEnabled(lowresFlag)

        DisplayPlots(
            parent=self.parent,
            row=self.row,
            is_data=self.is_data,
            plot_yt=True,
            plot_yi=True,
            plot_it=True,
            plot_ix=True,
            refresh_reduction_table=False,
        )

        if not tof_auto_switch:
            o_auto_tof_range = AutoTofRangeRadioButtonHandler(parent=self.parent)
            o_auto_tof_range.setup()
            o_auto_tof_range.line_edit_validation()

        self._open_instances.remove(self)  # remove this plot from the registry
