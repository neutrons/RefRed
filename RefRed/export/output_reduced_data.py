import os
from pathlib import Path
from qtpy.QtGui import QPalette
from qtpy.QtWidgets import QDialog, QFileDialog
from qtpy.QtCore import Qt
from mantid.api import mtd
from mantid.simpleapi import (
    ConvertToHistogram,
    CreateWorkspace,
    LRReflectivityOutput,
    Rebin,
    Scale,
)
import numpy as np
import time

from RefRed.interfaces import load_ui
from RefRed.load_reduced_data_set.stitching_ascii_widget import StitchingAsciiWidget
from RefRed.configuration.export_stitching_ascii_settings import (
    ExportStitchingAsciiSettings,
)
from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.reduction.reduced_data_handler import ReducedDataHandler
import RefRed.utilities


class OutputReducedData(QDialog):

    _open_instances = []
    o_stitching_ascii_widget = None
    parent = None
    filename = ""
    folder = ""

    q_axis = None
    y_axis = None
    e_axis = None

    R_THRESHOLD = 1e-15

    metadata = None
    text_data = None
    is_with_4th_column_flag = False
    dq0 = None
    dq_over_q = None
    use_lowest_error_value_flag = True

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.setWindowModality(False)
        self._open_instances.append(self)
        self.ui = load_ui("output_reduced_data_dialog.ui", self)
        self.parent = parent

        self.ui.folder_error.setVisible(False)
        palette = QPalette()
        palette.setColor(QPalette.Foreground, Qt.red)
        self.ui.folder_error.setPalette(palette)

        o_loaded_ascii = ReducedAsciiLoader(
            parent=parent, ascii_file_name="", is_live_reduction=True
        )
        if parent.o_stitching_ascii_widget is None:
            o_stitching_ascii_widget = StitchingAsciiWidget(
                parent=self.parent, loaded_ascii=o_loaded_ascii
            )
            parent.o_stitching_ascii_widget = o_stitching_ascii_widget

        # retrieve gui parameters
        _export_stitching_ascii_settings = ExportStitchingAsciiSettings()
        self.dq0 = str(_export_stitching_ascii_settings.fourth_column_dq0)
        self.dq_over_q = str(_export_stitching_ascii_settings.fourth_column_dq_over_q)
        self.is_with_4th_column_flag = bool(
            _export_stitching_ascii_settings.fourth_column_flag
        )
        # self.use_lowest_error_value_flag = bool(_export_stitching_ascii_settings.use_lowest_error_value_flag)

        self.ui.dq0Value.setText(self.dq0)
        self.ui.dQoverQvalue.setText(self.dq_over_q)
        self.ui.output4thColumnFlag.setChecked(self.is_with_4th_column_flag)

        _gui_metadata = self.parent.gui_metadata
        _q_min = str(_gui_metadata["q_min"])
        self.ui.manual_qmin_value.setText(_q_min)

    def auto_qmin_button_clicked(self, state):
        self.ui.manual_qmin_frame.setEnabled(not state)

    def output_format_radio_buttons_event(self):
        if self.ui.one_ascii_format.isChecked():
            status = False
        else:
            status = True

        self.ui.base_name_label.setEnabled(status)
        self.ui.prefix_name_value.setEnabled(status)
        self.ui.run_name_label.setEnabled(status)
        self.ui.suffix_name_value.setEnabled(status)
        self.ui.ext_name_label.setEnabled(status)

    def create_reduce_ascii_button_event(self):
        self.ui.folder_error.setVisible(False)
        if self.parent.o_stitching_ascii_widget is None:
            return

        if self.ui.one_ascii_format.isChecked():
            self.create_1_common_file()
        else:
            self.create_n_files()
        self.close()

    def create_n_files(self):
        path = self.parent.path_ascii
        folder = str(
            QFileDialog.getExistingDirectory(self, "Select Location", directory=path)
        )
        if folder == "":
            return

        self.folder = folder
        self.parent.path_ascii = folder
        self.write_n_ascii()
        self.save_back_widget_parameters_used()

    def create_1_common_file(self):

        run_number = self.parent.ui.reductionTable.item(0, 1).text()
        default_filename = "REFL_" + run_number + "_reduced_data.txt"
        path = Path(self.parent.path_ascii)
        default_filename = path + default_filename
        # directory = path
        _filter = "Reduced Ascii (*.txt);; All (*.*)"
        rst = QFileDialog.getSaveFileName(
            self,
            "Select Location and Name",
            directory=default_filename,
            filter=(_filter),
        )

        if isinstance(rst, tuple):
            filename, _ = rst
        else:
            filename = rst

        if filename.strip() == "":
            return

        folder = os.path.dirname(filename)
        if not self.is_folder_access_granted(folder):
            self.ui.folder_error.setVisible(True)
            return

        self.filename = filename
        self.parent.path_ascii = os.path.dirname(filename)
        self.write_1_common_ascii()

    def save_back_widget_parameters_used(self):
        _is_with_4th_column_flag = self.ui.output4thColumnFlag.isChecked()
        _dq0 = self.ui.dq0Value.text()
        _dq_over_q = self.ui.dQoverQvalue.text()
        # _use_lowest_error_value_flag = self.ui.usingLessErrorValueFlag.isChecked()

        _export_stitching_ascii_settings = ExportStitchingAsciiSettings()
        _export_stitching_ascii_settings.fourth_column_dq0 = _dq0
        _export_stitching_ascii_settings.fourth_column_dq_over_q = _dq_over_q
        _export_stitching_ascii_settings.fourth_column_flag = _is_with_4th_column_flag
        self.parent.exportStitchingAsciiSettings = _export_stitching_ascii_settings

    def is_folder_access_granted(self, filename):
        return os.access(filename, os.W_OK)

    def write_n_ascii(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        nbr_row = o_gui_utility.reductionTable_nbr_row()

        self.is_with_4th_column_flag = self.ui.output4thColumnFlag.isChecked()
        dq_over_q = self.ui.dQoverQvalue.text()
        self.dq_over_q = float(dq_over_q)

        for _row in range(nbr_row):
            self.filename = self.format_n_filename(row=_row)
            text = self.retrieve_individual_metadata(row=_row)

            if self.is_with_4th_column_flag:
                dq0 = self.ui.dq0Value.text()
                self.dq0 = float(dq0)
                line1 = "# dQ0[1/Angstroms]= " + dq0
                line2 = "# dQ1/Q= " + dq_over_q
                line3 = "# Q[1/Angstroms] R delta_R Precision"
                text.append(line1)
                text.append(line2)
                text.append("#")
                text.append(line3)
            else:
                text.append("# Q[1/Angstroms] R delta_R")

            self.text_data = text
            self.produce_data_without_common_q_axis(row=_row)
            self.format_data()
            self.create_file()

    def format_n_filename(self, row=-1):
        folder = self.folder
        prefix = self.ui.prefix_name_value.text()
        suffix = self.ui.suffix_name_value.text()
        ext = "txt"
        run_number = self.parent.ui.reductionTable.item(row, 1).text()
        filename = "%s/%s_%s_%s.%s" % (folder, prefix, run_number, suffix, ext)
        return filename

    def write_1_common_ascii(self):
        text = self.retrieve_metadata()
        self.is_with_4th_column_flag = self.ui.output4thColumnFlag.isChecked()
        dq_over_q = self.ui.dQoverQvalue.text()
        self.dq_over_q = float(dq_over_q)
        if self.is_with_4th_column_flag:
            dq0 = self.ui.dq0Value.text()
            self.dq0 = float(dq0)
            line1 = "# dQ0[1/Angstroms]= " + dq0
            line2 = "# dQ1/Q= " + dq_over_q
            line3 = "# Q[1/Angstroms] R delta_R Precision"
            text.append(line1)
            text.append(line2)
            text.append("#")
            text.append(line3)
        else:
            text.append("# Q[1/Angstroms] R delta_R")

        self.text_data = text

        # using new outputScript from Mantid
        self.apply_scaling_factor()
        self.create_output_file()

    def generate_selected_sf(self, lconfig=None):
        o_gui = GuiUtility(parent=self.parent)
        stitching_type = o_gui.getStitchingType()
        if stitching_type == "absolute":
            return lconfig.sf_abs_normalization
        elif stitching_type == "auto":
            return lconfig.sf_auto
        else:
            return lconfig.sf_manual

    def apply_sf(self, list_wks):
        big_table_data = self.parent.big_table_data
        for _index, _wks in enumerate(list_wks):
            _lconfig = big_table_data[_index, 2]
            _sf = self.generate_selected_sf(_lconfig)
            Scale(InputWorkspace=_wks, OutputWorkspace=_wks, Factor=_sf)
            list_wks[_index] = _wks
        return list_wks

    def create_output_file(self):
        # o_gui_utility = GuiUtility(parent=self.parent)
        # nbr_row = o_gui_utility.reductionTable_nbr_row()
        # _dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
        # _big_table_data = _dataObject.big_table_data

        # q min, q max
        [_q_min, _q_max] = self.get_q_range()
        # q bin
        _q_bin = -1.0 * float(self.parent.ui.qStep.text())
        _q_range = [_q_min, _q_bin, _q_max]

        # collect list of workspaces
        _list_wks = self.collect_list_wks()

        _list_wks = self.apply_sf(_list_wks)

        _text_data = self.format_metadata()

        print("Creating output file")
        print("====================")
        print("OutputBinning: %r" % _q_range)
        print("DQConstant: %r" % (float(self.ui.dq0Value.text())))
        print("DQSlope: %r" % (float(self.ui.dQoverQvalue.text())))

        LRReflectivityOutput(
            ReducedWorkspaces=_list_wks,
            OutputBinning=_q_range,
            DQConstant=float(self.ui.dq0Value.text()),
            DQSlope=float(self.ui.dQoverQvalue.text()),
            OutputFilename=self.filename,
            ScaleToUnity=False,
            Metadata=_text_data,
        )

    def format_metadata(self):
        _text_data = self.text_data
        _text_data_str = [str(txt) for txt in _text_data]
        sep = " \n"
        _new_text_data = sep.join(_text_data_str)
        return _new_text_data

    def collect_list_wks(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        nbr_row = o_gui_utility.reductionTable_nbr_row()
        _dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
        _big_table_data = _dataObject.big_table_data

        _list_wks = []
        for _row in range(nbr_row):
            _data = _big_table_data[_row, 2]
            _list_wks.append(_data.wks)

        return _list_wks

    def get_q_range(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        nbr_row = o_gui_utility.reductionTable_nbr_row()

        _auto_qmin_flag = self.ui.auto_qmin_button.isChecked()
        if _auto_qmin_flag:
            minQ = 100
        else:
            minQ = float(self.ui.manual_qmin_value.text())

        maxQ = 0

        _dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
        _big_table_data = _dataObject.big_table_data

        for i in range(nbr_row):
            _data = _big_table_data[i, 2]
            _q_axis = _data.reduce_q_axis
            if _auto_qmin_flag:
                minQ = min([_q_axis[0], minQ])
            maxQ = max([_q_axis[-1], maxQ])

        return [minQ, maxQ]

    def apply_scaling_factor(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        nbr_row = o_gui_utility.reductionTable_nbr_row()
        _dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
        _big_table_data = _dataObject.big_table_data

        for _row in range(nbr_row):
            _data = _big_table_data[_row, 2]
            _wks = _data.wks
            _sf = self.retrieve_sf(_data)
            _wks_scaled = Scale(_wks, _sf, "Multiply")
            _data.wks_scaled = _wks_scaled
            _big_table_data[_row, 2]

        _dataObject.big_table_data = _big_table_data

    def retrieve_sf(self, lconfigdataset):
        o_gui = GuiUtility(parent=self.parent)
        stitching_type = o_gui.getStitchingType()
        if stitching_type == "absolute":
            return lconfigdataset.sf_abs_normalization
        elif stitching_type == "auto":
            return lconfigdataset.sf_auto
        else:
            return lconfigdataset.sf_manual

    def retrieve_individual_metadata(self, row=-1):
        reduction_table = self.parent.ui.reductionTable
        text = []

        o_gui_utility = GuiUtility(parent=self.parent)
        _date = time.strftime("# Date: %d_%m_%Y")
        _reduction_method = "# Reduction method: manual"
        _reduction_engine = "# Reduction engine: RefRed"
        _reduction_date = "# %s" % _date
        # _ipts = o_gui_utility.get_ipts(row=0)
        for _entry in [_date, _reduction_method, _reduction_engine, _reduction_date]:
            text.append(_entry)
        text.append("#")

        _legend = (
            "# DataRun\tNormRun\t2theta(degrees)\tLambdaMin(A)\tLambdaMax(A)\tQmin(1/A)"
            "\tQmax(1/A)\tScalingFactor\tTotal Counts\tpcCharge(mC)"
        )
        text.append(_legend)
        _data_run = str(reduction_table.item(row, 1).text())
        _norm_run = str(reduction_table.item(row, 2).text())
        _2_theta = str(reduction_table.item(row, 3).text())
        _lambda_min = str(reduction_table.item(row, 4).text())
        _lambda_max = str(reduction_table.item(row, 5).text())
        _q_min = str(reduction_table.item(row, 6).text())
        _q_max = str(reduction_table.item(row, 7).text())
        _scaling_factor = self.retrieve_scaling_factor(row=row)
        _total_counts = self.retrieve_total_counts(row)
        _pcCharge = self.retrieve_pcCharge(row)
        _value = "# %s\t%s\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%f\t\t%f" % (
            _data_run,
            _norm_run,
            _2_theta,
            _lambda_min,
            _lambda_max,
            _q_min,
            _q_max,
            _scaling_factor,
            _total_counts,
            _pcCharge,
        )
        text.append(_value)

        # clocking settings
        text.append("#")
        text.append("# Clocking Correction used")
        o_gui_utility = GuiUtility(parent=self.parent)
        last_row = o_gui_utility.get_row_with_highest_q()
        big_table_data = self.parent.big_table_data
        clocking = big_table_data[last_row, 0].clocking
        text.append("# clock1: %s" % clocking[0])
        text.append("# clock2: %s" % clocking[1])

        return text

    def retrieve_metadata(self):
        reduction_table = self.parent.ui.reductionTable
        text = []

        o_gui_utility = GuiUtility(parent=self.parent)
        _date = time.strftime("# Date: %d_%m_%Y")
        _reduction_method = "# Reduction method: manual"
        _reduction_engine = "# Reduction engine: RefRed"
        _reduction_date = "# %s" % _date
        # _ipts = o_gui_utility.get_ipts(row=0)
        for _entry in [_date, _reduction_method, _reduction_engine, _reduction_date]:
            text.append(_entry)
        text.append("#")

        nbr_row = o_gui_utility.reductionTable_nbr_row()
        _legend = "\t".join(
            [
                "# DataRun",
                "NormRun",
                "2theta(degrees)",
                "LambdaMin(A)",
                "LambdaMax(A)",
                "Qmin(1/A)",
                "Qmax(1/A)",
                "ScalingFactor",
                "Total Counts",
                "pcCharge(mC)",
            ]
        )
        text.append(_legend)
        for _row in range(nbr_row):
            _data_run = str(reduction_table.item(_row, 1).text())
            _norm_run = str(reduction_table.item(_row, 2).text())
            _2_theta = str(reduction_table.item(_row, 3).text())
            _lambda_min = str(reduction_table.item(_row, 4).text())
            _lambda_max = str(reduction_table.item(_row, 5).text())
            _q_min = str(reduction_table.item(_row, 6).text())
            _q_max = str(reduction_table.item(_row, 7).text())
            _scaling_factor = self.retrieve_scaling_factor(row=_row)
            _total_counts = self.retrieve_total_counts(_row)
            _pcCharge = self.retrieve_pcCharge(_row)
            _value = "# %s\t%s\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%f\t\t%f" % (
                _data_run,
                _norm_run,
                _2_theta,
                _lambda_min,
                _lambda_max,
                _q_min,
                _q_max,
                _scaling_factor,
                _total_counts,
                _pcCharge,
            )
            text.append(_value)

        # clocking settings
        text.append("#")
        text.append("# Clocking Correction used")
        o_gui_utility = GuiUtility(parent=self.parent)
        last_row = o_gui_utility.get_row_with_highest_q()
        big_table_data = self.parent.big_table_data
        clocking = big_table_data[last_row, 0].clocking
        text.append("# clock1: %s" % clocking[0])
        text.append("# clock2: %s" % clocking[1])

        return text

    def retrieve_total_counts(self, row):
        _big_table_data = self.parent.big_table_data
        _lrdata = _big_table_data[row, 0]
        total_counts = _lrdata.total_counts
        return total_counts

    def retrieve_pcCharge(self, row):
        _big_table_data = self.parent.big_table_data
        _lrdata = _big_table_data[row, 0]
        pcCharge = _lrdata.proton_charge
        return pcCharge

    def retrieve_scaling_factor(self, row=-1):
        o_reduced_data_hanlder = ReducedDataHandler(parent=self.parent)
        big_table_data = self.parent.big_table_data
        _lconfig = big_table_data[row, 2]
        sf = o_reduced_data_hanlder.generate_selected_sf(lconfig=_lconfig)
        return str(sf)

    def create_file(self):
        RefRed.utilities.write_ascii_file(self.filename, self.text_data)

    def produce_data_without_common_q_axis(self, row=-1):
        _dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
        _big_table_data = _dataObject.big_table_data
        _data = _big_table_data[row, 2]
        _q_axis = _data.reduce_q_axis
        _y_axis = _data.reduce_y_axis[:-1]
        _e_axis = _data.reduce_e_axis[:-1]
        [_y_axis, _e_axis] = self.applySF(_data, _y_axis, _e_axis)

        self.q_axis = _q_axis
        self.y_axis = _y_axis
        self.e_axis = _e_axis

    def produce_data_with_common_q_axis(self):
        o_gui_utility = GuiUtility(parent=self.parent)
        nbr_row = o_gui_utility.reductionTable_nbr_row()

        _dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
        _big_table_data = _dataObject.big_table_data

        _auto_qmin_flag = self.ui.auto_qmin_button.isChecked()
        if _auto_qmin_flag:
            minQ = 100
        else:
            minQ = float(self.ui.manual_qmin_value.text())

        maxQ = 0

        for i in range(nbr_row):
            _data = _big_table_data[i, 2]

            tmp_wks_name = "wks_" + str(i)

            _q_axis = _data.reduce_q_axis
            _y_axis = _data.reduce_y_axis[:-1]
            _e_axis = _data.reduce_e_axis[:-1]

            [_y_axis, _e_axis] = self.applySF(_data, _y_axis, _e_axis)

            if _auto_qmin_flag:
                minQ = min([_q_axis[0], minQ])
            maxQ = max([_q_axis[-1], maxQ])

            tmp_wks_name = CreateWorkspace(
                DataX=_q_axis,
                DataY=_y_axis,
                DataE=_e_axis,
                Nspec=1,
                UnitX="Wavelength",
                OutputWorkspace=tmp_wks_name,
            )
            tmp_wks_name.setDistribution(True)

            # rebin everyting using the same Q binning parameters
        binQ = self.parent.ui.qStep.text()
        bin_parameters = str(minQ) + ",-" + str(binQ) + "," + str(maxQ)
        for i in range(nbr_row):

            tmp_wks_name = "wks_" + str(i)
            ConvertToHistogram(
                InputWorkspace=tmp_wks_name, OutputWorkspace=tmp_wks_name
            )

            Rebin(
                InputWorkspace=tmp_wks_name,
                Params=bin_parameters,
                OutputWorkspace=tmp_wks_name,
            )

        # we use the first histo as output reference
        data_y = mtd["wks_0"].dataY(0).copy()
        data_e = mtd["wks_0"].dataE(0).copy()

        skip_index = 0
        point_to_skip = 2

        for k in range(1, nbr_row):

            skip_point = True
            can_skip_last_point = False

            data_y_k = mtd["wks_" + str(k)].dataY(0)
            data_e_k = mtd["wks_" + str(k)].dataE(0)
            for j in range(len(data_y_k) - 1):

                if data_y_k[j] > 0:

                    can_skip_last_point = True
                    if skip_point:
                        skip_index += 1
                        if skip_index == point_to_skip:
                            skip_point = False
                            skip_index = 0
                        else:
                            continue

                if can_skip_last_point and (data_y_k[j + 1] == 0):
                    break

                if data_y[j] > 0 and data_y_k[j] > 0:

                    if self.use_lowest_error_value_flag:
                        if data_e[j] > data_e_k[j]:
                            data_y[j] = data_y_k[j]
                            data_e[j] = data_e_k[j]

                    else:
                        [data_y[j], data_e[j]] = RefRed.utilities.weighted_mean(
                            [data_y[j], data_y_k[j]], [data_e[j], data_e_k[j]]
                        )

                elif (data_y[j] == 0) and (data_y_k[j] > 0):
                    data_y[j] = data_y_k[j]
                    data_e[j] = data_e_k[j]

        data_x = mtd["wks_1"].dataX(0)

        self.q_axis = data_x
        self.y_axis = data_y
        self.e_axis = data_e

    def applySF(self, _data, y_array, e_array):
        if self.parent.ui.absolute_normalization_button.isChecked():
            _sf = _data.sf_abs_normalization
        elif self.parent.ui.auto_switching_button.isChecked():
            _sf = _data.sf_auto
        else:
            _sf = _data.sf_manual

        y_array = np.array(y_array, dtype=np.float)
        e_array = np.array(e_array, dtype=np.float)
        y_array *= _sf
        e_array *= _sf

        return [y_array, e_array]

    def format_data(self):
        self.cleanup_data()
        self.centering_q_axis()

        _q_axis = self.q_axis
        _y_axis = self.y_axis
        _e_axis = self.e_axis
        text = self.text_data

        if self.is_with_4th_column_flag:
            dq0 = self.dq0
            dq_over_q = self.dq_over_q

        sz = len(_q_axis)
        for i in range(sz):
            if _y_axis[i] > self.R_THRESHOLD:
                _line = str(_q_axis[i])
                _line += " " + str(_y_axis[i])
                _line += " " + str(_e_axis[i])
                if self.is_with_4th_column_flag:
                    _precision = str(dq0 + dq_over_q * _q_axis[i])
                    _line += " " + _precision
                text.append(_line)

        self.text_data = text

    def centering_q_axis(self):
        _q_axis = self.q_axis

        new_q_axis = []
        sz = len(_q_axis)
        for index in range(1, sz):
            _value = (_q_axis[index - 1] + _q_axis[index]) / 2.0
            new_q_axis.append(_value)

        self.q_axis = new_q_axis

    def cleanup_data(self):
        """Remove data where error bar is bigger than value"""
        _q_axis = self.q_axis
        _y_axis = self.y_axis
        _e_axis = self.e_axis

        new_q_axis = []
        new_y_axis = []
        new_e_axis = []

        for i in range(len(_y_axis)):

            q = _q_axis[i]
            y = _y_axis[i]
            e = _e_axis[i]

            if abs(e) > abs(y):
                continue

            if y < 0:
                continue

            new_q_axis.append(q)
            new_y_axis.append(y)
            new_e_axis.append(e)

        self.q_axis = new_q_axis
        self.y_axis = new_y_axis
        self.e_axis = new_e_axis

    def closeEvent(self, event=None):
        _gui_metadata = self.parent.gui_metadata
        _q_min = str(self.ui.manual_qmin_value.text())
        _gui_metadata["q_min"] = _q_min
        self.parent.gui_metadata = _gui_metadata
