import RefRed.colors as colors
import bisect
from RefRed.plot.clear_plots import ClearPlots
from RefRed.gui_handling.update_plot_widget_status import UpdatePlotWidgetStatus

# from RefRed.gui_handling.gui_utility import GuiUtility


class DisplayPlots(object):

    parent = None
    _data = None
    is_data = True

    row = -1
    col = -1

    xlim = 255
    ylim = 303

    def __init__(
        self,
        parent=None,
        row=-1,
        is_data=True,
        plot_yt=True,
        plot_yi=True,
        plot_it=True,
        plot_ix=True,
        plot_stitched=False,
        refresh_reduction_table=True,
    ):
        if row == -1:
            return

        self.parent = parent
        is_norm = not is_data
        self.is_data = is_data

        if is_data:
            col = 0
        else:
            col = 1
        self.row = row
        self.col = col

        _data = self.parent.big_table_data[row, col]

        if _data is None:
            ClearPlots(
                self.parent,
                is_data=is_data,
                is_norm=not is_data,
                plot_yt=plot_yt,
                plot_yi=plot_yi,
                plot_it=plot_it,
                plot_ix=plot_ix,
                stitched=plot_stitched,
            )
            return
        self._data = _data

        if not _data.new_detector_geometry_flag:
            self.xlim = 303
            self.ylim = 255

        # if self.parent.retain_all:
        # _active_data.all_plot_axis.yi_view_interval = self.parent.global_yi_view_interval
        # _active_data.all_plot_axis.yt_view_interval = self.parent.global_yt_view_interval
        # _active_data.all_plot_axis.it_view_interval = self.parent.global_it_view_interval
        # _active_data.all_plot_axis.ix_view_interval = self.parent.global_ix_view_interval
        # _active_data.all_plot_axis.yi_data_interval = self.parent.global_yi_view_interval
        # _active_data.all_plot_axis.yt_data_interval = self.parent.global_yt_view_interval
        # _active_data.all_plot_axis.it_data_interval = self.parent.global_it_view_interval
        # _active_data.all_plot_axis.ix_data_interval = self.parent.global_ix_view_interval

        # _active_data = self._data
        # _data.active_data = _active_data
        # parent.bigTableData[row,col] = _data

        if _data.tof_range_auto_flag:
            self.tofRangeAuto = self.getTOFrangeInMs(_data.tof_range_auto)
        else:
            self.tofRangeAuto = self.getTOFrangeInMs(_data.tof_range_manual)
        self.displayTOFrange(self.tofRangeAuto[0], self.tofRangeAuto[1], "ms")
        # print(self.tofRangeAuto)

        #        o_gui_utility = GuiUtility(parent = self.parent)
        #        o_gui_utility.set_auto_tof_range_widgets(status = _data.tof_range_auto_flag)

        self.tofAxis = self.getTOFrangeInMs(_data.tof_axis_auto_with_margin)
        self.fullTofAxis = self.getFullTOFinMs(_data.tof_axis_auto_with_margin)

        self.xy = _data.xydata
        self.ytof = _data.ytofdata
        self.countstofdata = _data.countstofdata
        self.countsxdata = _data.countsxdata
        self.ycountsdata = _data.ycountsdata

        self.peak = self.sortIntArray(_data.peak)
        self.back = self.sortIntArray(_data.back)
        self.clocking = self.sortIntArray(_data.clocking)

        self.lowRes = self.sortIntArray(_data.low_res)
        self.backFlag = bool(_data.back_flag)
        self.lowResFlag = bool(_data.low_res_flag)

        o_update_plot_widgets = UpdatePlotWidgetStatus(parent=parent)

        if is_data:
            self.workWithData(update_reduction_table=refresh_reduction_table)
            o_update_plot_widgets.enable_data()
        else:
            self.workWithNorm(update_reduction_table=refresh_reduction_table)
            o_update_plot_widgets.enable_norm()

        if plot_yt:
            ClearPlots(self.parent, plot_yt=True, is_data=is_data, is_norm=is_norm)
            self.plot_yt()

        if plot_it:
            ClearPlots(self.parent, plot_it=True, is_data=is_data, is_norm=is_norm)
            self.plot_it()

        if plot_yi:
            ClearPlots(self.parent, plot_yi=True, is_data=is_data, is_norm=is_norm)
            self.plot_yi()

        if plot_ix:
            ClearPlots(self.parent, plot_ix=True, is_data=is_data, is_norm=is_norm)
            self.plot_ix()

        if plot_yt or plot_it or plot_yi or plot_ix:
            if is_data:
                parent.ui.dataNameOfFile.setText("%s" % (_data.filename))
            else:
                parent.ui.normNameOfFile.setText("%s" % (_data.filename))
            self.displayMetadata()

    def displayMetadata(self):
        self.clearMetadataWidgets()
        d = self._data
        if d is None:
            return
        parent = self.parent
        parent.ui.metadataProtonChargeValue.setText("%.2e" % d.proton_charge)
        parent.ui.metadataProtonChargeUnits.setText("%s" % d.proton_charge_units)
        parent.ui.metadataLambdaRequestedValue.setText("%.2f" % d.lambda_requested)
        parent.ui.metadataLambdaRequestedUnits.setText("%s" % d.lambda_requested_units)
        parent.ui.metadatathiValue.setText("%.2f" % d.ths)
        parent.ui.metadatathiUnits.setText("%s" % d.ths_units)
        parent.ui.metadatatthdValue.setText("%.2f" % d.tthd)
        parent.ui.metadatatthdUnits.setText("%s" % d.tthd_units)
        parent.ui.metadataS1WValue.setText("%.2f" % d.S1W)
        parent.ui.metadataS1HValue.setText("%.2f" % d.S1H)
        parent.ui.metadataRunNumber.setText("%s" % d.run_number)
        if d.isSiThere:
            parent.ui.S2SiWlabel.setText("SiW:")
            parent.ui.S2SiHlabel.setText("SiH:")
            parent.ui.metadataS2WValue.setText("%.2f" % d.SiW)
            parent.ui.metadataS2HValue.setText("%.2f" % d.SiH)
        else:
            parent.ui.S2SiWlabel.setText("S2W:")
            parent.ui.S2SiHlabel.setText("S2H:")
            parent.ui.metadataS2WValue.setText("%.2f" % d.S2W)
            parent.ui.metadataS2HValue.setText("%.2f" % d.S2H)
        # nexus = d.filename
        if self.is_data:
            parent.ui.dataNameOfFile.setText("%s" % d.run_number)
        else:
            parent.ui.normNameOfFile.setText("%s" % d.run_number)

    def clearMetadataWidgets(self):
        parent = self.parent
        parent.ui.metadataProtonChargeValue.setText("N/A")
        parent.ui.metadataLambdaRequestedValue.setText("N/A")
        parent.ui.metadataS1HValue.setText("N/A")
        parent.ui.metadataS1WValue.setText("N/A")
        parent.ui.metadataS2HValue.setText("N/A")
        parent.ui.metadataS2WValue.setText("N/A")
        parent.ui.metadatathiValue.setText("N/A")
        parent.ui.metadatatthdValue.setText("N/A")
        parent.ui.dataNameOfFile.setText("")
        parent.ui.normNameOfFile.setText("")
        parent.ui.metadataRunNumber.setText("N/A")

    def plot_ix(self):
        _countsxdata = self.countsxdata
        self.ix_plot_ui.canvas.ax.plot(_countsxdata)
        self.ix_plot_ui.canvas.ax.set_xlabel("pixels")
        self.ix_plot_ui.canvas.ax.set_ylabel("counts")
        self.ix_plot_ui.canvas.ax.set_xlim(0, self.xlim)

        if self.lowResFlag:
            self.ix_plot_ui.canvas.ax.axvline(
                self.lowRes[0], color=colors.LOWRESOLUTION_SELECTION_COLOR
            )
            self.ix_plot_ui.canvas.ax.axvline(
                self.lowRes[1], color=colors.LOWRESOLUTION_SELECTION_COLOR
            )

        if self._data.all_plot_axis.is_ix_ylog:
            self.ix_plot_ui.canvas.ax.set_yscale("log")
        else:
            self.ix_plot_ui.canvas.ax.set_yscale("linear")

        if self._data.all_plot_axis.ix_data_interval is None:
            [xmin, xmax] = self.ix_plot_ui.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.ix_plot_ui.canvas.ax.yaxis.get_view_interval()
            self._data.all_plot_axis.ix_data_interval = [xmin, xmax, ymin, ymax]
            self._data.all_plot_axis.ix_view_interval = [xmin, xmax, ymin, ymax]
            self.ix_plot_ui.toolbar.home_settings = [xmin, xmax, ymin, ymax]
        else:
            [xmin, xmax, ymin, ymax] = self._data.all_plot_axis.ix_view_interval
            self.ix_plot_ui.canvas.ax.set_xlim([xmin, xmax])
            self.ix_plot_ui.canvas.ax.set_ylim([ymin, ymax])

        self.ix_plot_ui.canvas.draw_idle()

    def get_ycountsdata_of_tof_range_selected(self):
        autotmin = float(self.tofRangeAuto[0])
        autotmax = float(self.tofRangeAuto[1])

        [tmin, tmax] = self.getTOFrangeInMs([autotmin, autotmax])

        ytof = self.ytof
        tof = self.fullTofAxis

        index_tof_left = bisect.bisect_left(tof, tmin)
        index_tof_right = bisect.bisect_right(tof, tmax)

        _new_ytof = ytof[:, index_tof_left:index_tof_right]
        _new_ycountsdata = _new_ytof.sum(axis=1)

        return _new_ycountsdata

    def plot_yi(self):
        _ycountsdata = self.get_ycountsdata_of_tof_range_selected()

        _xaxis = list(range(len(_ycountsdata)))
        self.yi_plot_ui.canvas.ax.plot(_ycountsdata, _xaxis, color=colors.COLOR_LIST[1])
        self.yi_plot_ui.canvas.ax.set_xlabel("counts")
        self.yi_plot_ui.canvas.ax.set_ylabel("y (pixel)")

        if self._data.all_plot_axis.yi_data_interval is None:
            self.yi_plot_ui.canvas.ax.set_ylim(0, self.ylim)

        self.yi_plot_ui.canvas.ax.axhline(
            self.peak[0], color=colors.PEAK_SELECTION_COLOR
        )
        self.yi_plot_ui.canvas.ax.axhline(
            self.peak[1], color=colors.PEAK_SELECTION_COLOR
        )

        if self.backFlag:
            self.yi_plot_ui.canvas.ax.axhline(
                self.back[0], color=colors.BACK_SELECTION_COLOR
            )
            self.yi_plot_ui.canvas.ax.axhline(
                self.back[1], color=colors.BACK_SELECTION_COLOR
            )

        if self._data.all_plot_axis.is_yi_xlog:
            self.yi_plot_ui.canvas.ax.set_xscale("log")
        else:
            self.yi_plot_ui.canvas.ax.set_xscale("linear")

        if self.is_data:
            self.yi_plot_ui.canvas.ax.axhline(
                self.clocking[0], color=colors.CLOCKING_SELECTION_COLOR
            )
            self.yi_plot_ui.canvas.ax.axhline(
                self.clocking[1], color=colors.CLOCKING_SELECTION_COLOR
            )

        if self._data.all_plot_axis.yi_data_interval is None:
            [xmin, xmax] = self.yi_plot_ui.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.yi_plot_ui.canvas.ax.yaxis.get_view_interval()
            self._data.all_plot_axis.yi_data_interval = [xmin, xmax, ymin, ymax]
            self._data.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
            self.yi_plot_ui.toolbar.home_settings = [xmin, xmax, ymin, ymax]
        else:
            [xmin, xmax, ymin, ymax] = self._data.all_plot_axis.yi_view_interval
            self.yi_plot_ui.canvas.ax.set_xlim([xmin, xmax])
            self.yi_plot_ui.canvas.ax.set_ylim([ymin, ymax])

        self.yi_plot_ui.canvas.draw_idle()

    def plot_it(self):
        _tof_axis = self.fullTofAxis
        _countstofdata = self.countstofdata

        self.it_plot_ui.canvas.ax.plot(_tof_axis[0:-1], _countstofdata)
        self.it_plot_ui.canvas.ax.set_xlabel("t (ms)")
        self.it_plot_ui.canvas.ax.set_ylabel("Counts")

        autotmin = float(self.tofRangeAuto[0])
        autotmax = float(self.tofRangeAuto[1])
        self.it_plot_ui.canvas.ax.axvline(autotmin, color=colors.TOF_SELECTION_COLOR)
        self.it_plot_ui.canvas.ax.axvline(autotmax, color=colors.TOF_SELECTION_COLOR)

        if self._data.all_plot_axis.is_it_ylog:
            self.it_plot_ui.canvas.ax.set_yscale("log")
        else:
            self.it_plot_ui.canvas.ax.set_yscale("linear")

        if self._data.all_plot_axis.it_data_interval is None:
            [xmin, xmax] = self.it_plot_ui.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.it_plot_ui.canvas.ax.yaxis.get_view_interval()
            self._data.all_plot_axis.it_data_interval = [xmin, xmax, ymin, ymax]
            self._data.all_plot_axis.it_view_interval = [xmin, xmax, ymin, ymax]
            self.it_plot_ui.toolbar.home_settings = [xmin, xmax, ymin, ymax]
        else:
            [xmin, xmax, ymin, ymax] = self._data.all_plot_axis.it_view_interval
            self.it_plot_ui.canvas.ax.set_xlim([xmin, xmax])
            self.it_plot_ui.canvas.ax.set_ylim([ymin, ymax])

        self.it_plot_ui.canvas.draw_idle()

    def plot_yt(self):

        _ytof = self.ytof
        _isLog = True
        _tof_axis = self.tofAxis
        _extent = [_tof_axis[0], _tof_axis[1], 0, self.ylim]
        self.yt_plot_ui.imshow(
            _ytof, log=_isLog, aspect="auto", origin="lower", extent=_extent
        )
        self.yt_plot_ui.set_xlabel("t (ms)")
        self.yt_plot_ui.set_ylabel("y (pixel)")

        autotmin = float(self.tofRangeAuto[0])
        autotmax = float(self.tofRangeAuto[1])

        [tmin, tmax] = self.getTOFrangeInMs([autotmin, autotmax])
        self.yt_plot_ui.canvas.ax.axvline(tmin, color=colors.TOF_SELECTION_COLOR)
        self.yt_plot_ui.canvas.ax.axvline(tmax, color=colors.TOF_SELECTION_COLOR)
        self.yt_plot_ui.canvas.ax.axhline(
            self.peak[0], color=colors.PEAK_SELECTION_COLOR
        )
        self.yt_plot_ui.canvas.ax.axhline(
            self.peak[1], color=colors.PEAK_SELECTION_COLOR
        )

        if self.is_data:
            self.yi_plot_ui.canvas.ax.axhline(
                self.clocking[0], color=colors.CLOCKING_SELECTION_COLOR
            )
            self.yi_plot_ui.canvas.ax.axhline(
                self.clocking[1], color=colors.CLOCKING_SELECTION_COLOR
            )

        if self.backFlag:
            self.yt_plot_ui.canvas.ax.axhline(
                self.back[0], color=colors.BACK_SELECTION_COLOR
            )
            self.yt_plot_ui.canvas.ax.axhline(
                self.back[1], color=colors.BACK_SELECTION_COLOR
            )

        if self.is_data:
            self.yt_plot_ui.canvas.ax.axhline(
                self.clocking[0], color=colors.CLOCKING_SELECTION_COLOR
            )
            self.yt_plot_ui.canvas.ax.axhline(
                self.clocking[1], color=colors.CLOCKING_SELECTION_COLOR
            )

        if self._data.all_plot_axis.is_yt_ylog:
            self.yt_plot_ui.canvas.ax.set_yscale("log")
        else:
            self.yt_plot_ui.canvas.ax.set_yscale("linear")

        if self._data.all_plot_axis.yt_data_interval is None:
            self.yt_plot_ui.canvas.ax.set_ylim(0, self.ylim)
            [xmin, xmax] = self.yt_plot_ui.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.yt_plot_ui.canvas.ax.yaxis.get_view_interval()
            self._data.all_plot_axis.yt_data_interval = [xmin, xmax, ymin, ymax]
            self._data.all_plot_axis.yt_view_interval = [xmin, xmax, ymin, ymax]
            self.yt_plot_ui.toolbar.home_settings = [xmin, xmax, ymin, ymax]
        else:
            [xmin, xmax, ymin, ymax] = self._data.all_plot_axis.yt_view_interval
            self.yt_plot_ui.canvas.ax.set_xlim([xmin, xmax])
            self.yt_plot_ui.canvas.ax.set_ylim([ymin, ymax])

        self.yt_plot_ui.canvas.draw_idle()

    def displayTOFrange(self, tmin, tmax, units):
        parent = self.parent

        _tmin = float(tmin)
        _tmax = float(tmax)

        stmin = str("%.2f" % _tmin)
        stmax = str("%.2f" % _tmax)

        parent.ui.TOFmanualFromValue.setText(stmin)
        parent.ui.TOFmanualToValue.setText(stmax)

    def workWithNorm(self, update_reduction_table=True):
        parent = self.parent
        self.yt_plot_ui = parent.ui.norm_yt_plot
        self.yi_plot_ui = parent.ui.norm_yi_plot
        self.it_plot_ui = parent.ui.norm_it_plot
        self.ix_plot_ui = parent.ui.norm_ix_plot

        if update_reduction_table:
            # parent.ui.useNormalizationFlag.setChecked(self.useItFlag)

            [peak1, peak2] = self.peak
            parent.ui.normPeakFromValue.setValue(peak1)
            parent.ui.normPeakToValue.setValue(peak2)

            [back1, back2] = self.back
            parent.ui.normBackFromValue.setValue(back1)
            parent.ui.normBackToValue.setValue(back2)
            parent.ui.normBackgroundFlag.setChecked(self.backFlag)

            [lowRes1, lowRes2] = self.lowRes
            parent.ui.normLowResFromValue.setValue(lowRes1)
            parent.ui.normLowResToValue.setValue(lowRes2)
            parent.ui.normLowResFlag.setChecked(self.lowResFlag)

    def workWithData(self, update_reduction_table=True):
        parent = self.parent
        self.yt_plot_ui = parent.ui.data_yt_plot
        self.yi_plot_ui = parent.ui.data_yi_plot
        self.it_plot_ui = parent.ui.data_it_plot
        self.ix_plot_ui = parent.ui.data_ix_plot

        if update_reduction_table:

            [peak1, peak2] = self.peak
            parent.ui.dataPeakFromValue.setValue(peak1)
            parent.ui.dataPeakToValue.setValue(peak2)

            [back1, back2] = self.back
            parent.ui.dataBackFromValue.setValue(back1)
            parent.ui.dataBackToValue.setValue(back2)
            parent.ui.dataBackgroundFlag.setChecked(self.backFlag)

            [lowRes1, lowRes2] = self.lowRes
            parent.ui.dataLowResFromValue.setValue(lowRes1)
            parent.ui.dataLowResToValue.setValue(lowRes2)
            parent.ui.dataLowResFlag.setChecked(self.lowResFlag)

            [clocking1, clocking2] = self.clocking
            parent.ui.dataPrimFromValue.setValue(clocking1)
            parent.ui.dataPrimToValue.setValue(clocking2)

    def isDataSelected(self):
        if self.parent.ui.dataNormTabWidget.currentIndex() == 0:
            return True
        else:
            return False

    def sortIntArray(self, _array):
        [_element1, _element2] = _array
        _element1 = int(_element1)
        _element2 = int(_element2)
        _element_min = min([_element1, _element2])
        _element_max = max([_element1, _element2])
        return [_element_min, _element_max]

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
