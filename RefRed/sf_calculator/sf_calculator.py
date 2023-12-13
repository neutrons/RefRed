"""
    Scaling factor calculator
    TODO: This need major cleanup
"""
import sys
import os
from pathlib import Path
from qtpy import QtGui, QtCore, QtWidgets
import numpy as np
import logging
import time

from RefRed import ORGANIZATION, APPNAME
import RefRed.colors
from RefRed.interfaces import load_ui
from RefRed.sf_calculator.fill_sf_gui_table import FillSFGuiTable
from RefRed.sf_calculator.incident_medium_list_editor import IncidentMediumListEditor
from RefRed.sf_calculator.load_and_sort_nxsdata_for_sf_calculator import (
    LoadAndSortNXSDataForSFcalculator,
)
from RefRed.sf_calculator.check_sf_run_reduction_button_status import (
    CheckSfRunReductionButtonStatus,
)
from RefRed.sf_calculator.reduction_sf_calculator import ReductionSfCalculator
from RefRed.sf_calculator.sf_calculator_right_click import SFCalculatorRightClick

from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker
from RefRed.utilities import convert_tof_values_unit


def str2bool(v):
    try:
        return v.lower() in ("yes", "true", "t", "1")
    except:
        if float(v) == 0:
            return False
        else:
            return True


class SFCalculator(QtWidgets.QMainWindow):
    window_title = "SF Calculator - "
    user_click_exit = False
    time_click1 = -1
    current_table_row_selected = -1
    event_progressbar = None

    data_list = []
    big_table = None
    big_table_status = None  # only a fully True table will validate the GO_REDUCTION button
    big_table_nxdata = []
    is_using_si_slits = False
    loaded_list_of_runs = []
    list_nxsdata_sorted = []

    def __init__(self, instrument=None, instrument_list=None, parent=None):
        super().__init__(parent)

        # Application settings
        settings = QtCore.QSettings(ORGANIZATION, APPNAME)
        self._save_directory = settings.value("save_directory", os.path.expanduser("~"))
        self._xml_config_dir = settings.value("xml_config_dir", os.path.expanduser("~"))
        self.current_loaded_file = os.path.expanduser("~/new_configuration.xml")

        self.ui = load_ui("sf_calculator_interface.ui", baseinstance=self)
        self.loaded_list_of_runs = []

        # Default options
        self.read_options = {
            "is_auto_tof_finder": True,
            "bins": 40,
            "is_auto_peak_finder": True,
            "back_offset_from_peak": 3,
        }

        self.initGui()
        self.checkGui()
        self.initConnections()

        # Add default medium
        text_list = ["Select or define incident medium...", "air"]
        self.incidentMediumComboBox.clear()
        self.incidentMediumComboBox.addItems(text_list)
        self.incidentMediumComboBox.setCurrentIndex(1)

        # Add default config file
        self.update_config_file(os.path.expanduser("~/scaling_factors.cfg"))

    @property
    def save_directory(self):
        return self._save_directory

    @save_directory.setter
    def save_directory(self, value):
        self._save_directory = value
        settings = QtCore.QSettings(ORGANIZATION, APPNAME)
        settings.setValue("save_directory", value)

    @property
    def xml_config_dir(self):
        return self._xml_config_dir

    @xml_config_dir.setter
    def xml_config_dir(self, value):
        self._xml_config_dir = value
        settings = QtCore.QSettings(ORGANIZATION, APPNAME)
        settings.setValue("xml_config_dir", value)

    def initConnections(self):
        self.yt_plot.toolbar.homeClicked.connect(self.homeYtPlot)
        self.yi_plot.toolbar.homeClicked.connect(self.homeYiPlot)
        self.forceSortByMetaData.clicked.connect(self.forceSrotTableByMetaData)

    def initGui(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, RefRed.colors.VALUE_BAD)
        self.back1_error.setPalette(palette)
        self.back2_error.setPalette(palette)
        self.peak1_error.setPalette(palette)
        self.peak2_error.setPalette(palette)
        self.error_label.setPalette(palette)
        self.event_progressbar = QtWidgets.QProgressBar(self.statusbar)
        self.event_progressbar.setMinimumSize(20, 14)
        self.event_progressbar.setMaximumSize(140, 100)
        self.statusbar.addPermanentWidget(self.event_progressbar)
        self.event_progressbar.setVisible(False)
        # The file menu is not currently used, since we can't load or save
        # configurations. Just remove the menu by giving it an empty title.
        self.menuFile.setTitle("")

    def homeYtPlot(self):
        [xmin, xmax, ymin, ymax] = self.yt_plot.toolbar.home_settings
        self.yt_plot.canvas.ax.set_xlim([xmin, xmax])
        self.yt_plot.canvas.ax.set_ylim([ymin, ymax])
        self.yt_plot.canvas.draw_idle()

    def homeYiPlot(self):
        [xmin, xmax, ymin, ymax] = self.yi_plot.toolbar.home_settings
        self.yi_plot.canvas.ax.set_xlim([xmin, xmax])
        self.yi_plot.canvas.ax.set_ylim([ymin, ymax])
        self.yi_plot.canvas.draw_idle()

    def forceSrotTableByMetaData(self):
        print("Force sorting table by metadata")
        self.is_manual_edit_of_tableWidget = False
        _list_runs = self.loaded_list_of_runs
        o_load_and_sort_nxsdata = LoadAndSortNXSDataForSFcalculator(
            _list_runs,
            parent=self,
            read_options=self.read_options,
            sort_by_metadata=True,
        )
        self.update_table(o_load_and_sort_nxsdata)
        self.is_manual_edit_of_tableWidget = True

    def forceTypeToInt(self, array_value, default_value=-1):
        final_array_value = []
        for _value in array_value:
            if _value == "" or _value == "N/A":
                final_array_value.append(default_value)
            else:
                final_array_value.append(int(_value))
        return final_array_value

    def update_table(self, sorter, finalize=True):
        if len(sorter.big_table) == 0:
            QtWidgets.QMessageBox.information(self, "No Files Loaded!", "Check The list of runs")
            return

        self.big_table = sorter.big_table
        self.list_nxsdata_sorted = sorter.getListNXSDataSorted()
        self.loaded_list_of_runs = sorter.getListOfRunsLoaded()
        self.is_using_si_slits = sorter.is_using_si_slits
        self.fillGuiTable()
        if finalize:
            self.runSequenceLineEdit.setText("")
            self.checkGui()
            self.tableWidgetCellSelected(0, 0)
            self.fileHasBeenModified()

    def runSequenceLineEditEvent(self):
        run_sequence = self.runSequenceLineEdit.text()
        self.is_manual_edit_of_tableWidget = False
        oListRuns = RunSequenceBreaker(run_sequence)
        _new_runs = oListRuns.getFinalList()

        _old_runs = self.loaded_list_of_runs
        _list_runs = np.unique(np.hstack([_old_runs, _new_runs]))
        o_load_and_sort_nxsdata = LoadAndSortNXSDataForSFcalculator(
            _list_runs, parent=self, read_options=self.read_options
        )
        self.update_table(o_load_and_sort_nxsdata)
        self.is_manual_edit_of_tableWidget = True

    def updateProgressBar(self, progress):
        self.event_progressbar.setVisible(True)
        self.event_progressbar.setValue(progress * 100)
        self.event_progressbar.update()
        if progress == 1:
            time.sleep(2)
            self.event_progressbar.setVisible(False)
            self.event_progressbar.setValue(0)
            self.event_progressbar.update()

    def displayConfigFile(self, file_name):
        with open(file_name, "r") as fd:
            data = fd.read()
        if not data:
            data = "EMPTY FILE"
        if data == [""] or data == "\n":
            data = "EMPTY FILE"
        self.sfFileNamePreview.setPlainText(data)
        self.sfFileNamePreview.setEnabled(True)

    def tableWidgetRightClick(self, position):
        o_sf_calculator_table_right_click = SFCalculatorRightClick(parent=self, position=position)
        o_sf_calculator_table_right_click.run()

    def generateSFfile(self):
        ReductionSfCalculator(parent=self)

    def exportScript(self):
        ReductionSfCalculator(parent=self, export_script_flag=True)

    def update_config_file(self, file_name):
        if not file_name.endswith(".cfg"):
            file_name += ".cfg"
        if not os.path.isfile(file_name):
            Path(file_name).touch()
        self.displayConfigFile(file_name)
        self.sfFileNameLabel.setText(file_name)
        self.save_directory = os.path.dirname(file_name)
        self.fileHasBeenModified()

    def browseFile(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,  # parent widget
            "Open Configuration File",  # dialog title
            self.save_directory,  # opening directory
            "SF config (*.cfg);;All (*.*)",  # list of display-file filters
        )
        if file_name:
            self.update_config_file(file_name)

    def selectManualTOF(self):
        self.manualTOFWidgetsEnabled(True)
        self.saveTOFautoFlag(auto_flag=False)
        self.displaySelectedTOFandUpdateTable(mode="manual")
        self.displayPlot(row=self.current_table_row_selected, yi_plot=False)
        self.updateTableWithTOFandLambda()
        self.fileHasBeenModified()

    def updateTableWithTOFandLambda(self):
        tof1 = float(self.TOFmanualFromValue.text())
        tof2 = float(self.TOFmanualToValue.text())
        tof_min = min([tof1, tof2])
        tof_max = max([tof1, tof2])
        self.updateTableWithTOFinfos(tof_min, tof_max)
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxdata = _list_nxsdata_sorted[self.current_table_row_selected]
        _nxdata.calculate_lambda_range([tof_min * 1000.0, tof_max * 1000.0])
        self.updateTableWithLambdaInfos(_nxdata)

    def selectAutoTOF(self):
        self.manualTOFWidgetsEnabled(False)
        self.saveManualTOFmode()
        self.saveTOFautoFlag(auto_flag=True)
        self.displaySelectedTOFandUpdateTable(mode="auto")
        self.displayPlot(row=self.current_table_row_selected, yi_plot=False)
        self.updateTableWithTOFandLambda()
        self.fileHasBeenModified()

    def saveManualTOFmode(self):
        tof1 = float(self.TOFmanualFromValue.text())
        tof2 = float(self.TOFmanualToValue.text())
        tof_min = min([tof1, tof2])
        tof_max = max([tof1, tof2])
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        list_row = self.getListRowWithSameLambda()
        tof1 = 1000.0 * tof_min
        tof2 = 1000.0 * tof_max
        for index, _row in enumerate(list_row):
            _nxdata = _list_nxsdata_sorted[_row]
            _nxdata.tof_range = [tof1, tof2]
            _list_nxsdata_sorted[_row] = _nxdata

        self.list_nxsdata_sorted = _list_nxsdata_sorted

    def saveTOFautoFlag(self, auto_flag=False):
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        # save status for all row from same categorie
        list_row = self.getListRowWithSameLambda()

        auto_flag_value = 1 if auto_flag else 0
        _big_table = self.big_table
        for index, _row in enumerate(list_row):
            _nxdata = _list_nxsdata_sorted[_row]
            _nxdata.tof_auto_flag = auto_flag
            _list_nxsdata_sorted[_row] = _nxdata
            _big_table[_row, 16] = auto_flag_value

        self.list_nxsdata_sorted = _list_nxsdata_sorted
        self.big_table = _big_table

    def displaySelectedTOFandUpdateTable(self, mode="auto"):
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxdata = _list_nxsdata_sorted[self.current_table_row_selected]
        if mode == "auto":
            [tof1, tof2] = _nxdata.tof_range_auto
        else:
            [tof1, tof2] = _nxdata.tof_range
        tof1 = float(tof1) * 1e-3
        tof2 = float(tof2) * 1e-3

        self.updateTableWithTOFinfos(tof1, tof2)
        self.TOFmanualFromValue.setText("%.2f" % tof1)
        self.TOFmanualToValue.setText("%.2f" % tof2)

    def loadingConfiguration(self):
        """
        TODO: this is broken functionality that never worked and is not needed
        This function is a UI slot.
        """
        logging.error("loadingConfiguration not implemented")

    def manualTOFtextFieldValidated(self, with_plot_update=True):
        tof1 = float(self.TOFmanualFromValue.text())
        tof2 = float(self.TOFmanualToValue.text())
        tof_min = min([tof1, tof2]) * 1000
        tof_max = max([tof1, tof2]) * 1000
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxdata = _list_nxsdata_sorted[self.current_table_row_selected]
        _nxdata.tof_range = [tof_min, tof_max]
        _nxdata.calculate_lambda_range()
        _nxdata.tof_auto_flag = False
        _list_nxsdata_sorted[self.current_table_row_selected] = _nxdata
        self.list_nxsdata_sorted = _list_nxsdata_sorted
        if with_plot_update:
            self.displayPlot(row=self.current_table_row_selected, yi_plot=False)
        self.updateTableWithTOFinfos(tof1, tof2)
        self.updateTableWithLambdaInfos(_nxdata)
        self.fileHasBeenModified()

    def updateTableWithLambdaInfos(self, nxdata):
        list_row = self.getListRowWithSameLambda()
        lambda_range = nxdata.lambda_range

        for index, _row in enumerate(list_row):
            if index == 0:
                color = self.tableWidget.item(_row, 0).background()
            _item = QtWidgets.QTableWidgetItem("%s" % lambda_range[0])
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _item.setBackground(color)
            self.tableWidget.setItem(_row, 2, _item)

            _item = QtWidgets.QTableWidgetItem("%s" % lambda_range[1])
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _item.setBackground(color)
            self.tableWidget.setItem(_row, 3, _item)

    def updateTableWithTOFinfos(self, tof1_ms, tof2_ms):
        """update all the rows that have the same lambda requested"""
        list_row = self.getListRowWithSameLambda()
        for index, _row in enumerate(list_row):
            if index == 0:
                color = self.tableWidget.item(_row, 0).background()
            _item = QtWidgets.QTableWidgetItem("%.2f" % tof1_ms)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _brush_OK = QtGui.QBrush()
            _brush_OK.setColor(RefRed.colors.VALUE_OK)
            _item.setForeground(_brush_OK)
            _item.setBackground(color)
            self.tableWidget.setItem(_row, 14, _item)
            _item = QtWidgets.QTableWidgetItem("%.2f" % tof2_ms)
            _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            _brush_OK = QtGui.QBrush()
            _brush_OK.setColor(RefRed.colors.VALUE_OK)
            _item.setForeground(_brush_OK)
            _item.setBackground(color)
            self.tableWidget.setItem(_row, 15, _item)

    def getListRowWithSameLambda(self):
        _row = self.current_table_row_selected
        _lambda_requested = self.tableWidget.item(_row, 5).text()
        nbr_row = self.tableWidget.rowCount()
        list_row = []
        for i in range(nbr_row):
            _lambda_to_compare_with = self.tableWidget.item(i, 5).text()
            if _lambda_to_compare_with == _lambda_requested:
                list_row.append(i)
        return list_row

    def incidentMediumComboBoxChanged(self):
        self.fileHasBeenModified()

    def editIncidentMediumList(self):
        _incident_medium_object = IncidentMediumListEditor(parent=self)
        _incident_medium_object.show()

    def tableWidgetCellEntered(self, row, col):
        if self.user_click_exit:
            return
        try:
            if row == self.current_table_row_selected:
                cell_value = self.tableWidget.item(row, col).text()
                _list_nxsdata_sorted = self.list_nxsdata_sorted
                _nxdata = _list_nxsdata_sorted[row]
                if col in [10, 11]:
                    [peak1, peak2] = _nxdata.peak
                    if col == 10:
                        _nxdata.peak = [cell_value, peak2]
                    else:
                        _nxdata.peak = [peak1, cell_value]
                elif col in [12, 13]:
                    [back1, back2] = _nxdata.back
                    if col == 12:
                        _nxdata.back = [cell_value, back2]
                    else:
                        _nxdata.back = [back1, cell_value]
                _list_nxsdata_sorted[row] = _nxdata
                self.list_nxsdata_sorted = _list_nxsdata_sorted
                self.displaySelectedRow(row)
                self.updateTableWidgetPeakBackTof(row)
                self.displayPlot(row, yt_plot=True, yi_plot=True)
        except:
            logging.error(sys.exc_info()[1])

    def clearSFContentFile(self):
        self.sfFileNamePreview.setPlainText("EMPTY FILE")
        self.sfFileNamePreview.setEnabled(True)

    def peak1SpinBoxValueChanged(self):
        self.peakBackSpinBoxValueChanged("peak1")

    def peak2SpinBoxValueChanged(self):
        self.peakBackSpinBoxValueChanged("peak2")

    def back1SpinBoxValueChanged(self):
        self.peakBackSpinBoxValueChanged("back1")

    def back2SpinBoxValueChanged(self):
        self.peakBackSpinBoxValueChanged("back2")

    def peakBackSpinBoxValueChanged(self, kind, with_plot_update=True):
        if "peak" in kind:
            peak1 = self.dataPeakFromValue.value()
            peak2 = self.dataPeakToValue.value()
            peak_min = min([peak1, peak2])
            peak_max = max([peak1, peak2])

            if peak1 == peak_max:
                if kind == "peak1":
                    self.dataPeakToValue.setFocus()
                else:
                    self.dataPeakFromValue.setFocus()
                self.dataPeakFromValue.setValue(peak_min)
                self.dataPeakToValue.setValue(peak_max)

        if "back" in kind:
            back1 = self.dataBackFromValue.value()
            back2 = self.dataBackToValue.value()
            back_min = min([back1, back2])
            back_max = max([back1, back2])

            if back1 == back_max:
                if kind == "back1":
                    self.dataBackToValue.setFocus()
                else:
                    self.dataBackFromValue.setFocus()
                self.dataBackFromValue.setValue(back_min)
                self.dataBackToValue.setValue(back_max)

        self.testPeakBackErrorWidgets()
        self.updateNXSData(row=self.current_table_row_selected, source="spinbox", kind=kind)
        if with_plot_update:
            self.displayPlot(row=self.current_table_row_selected, yt_plot=True, yi_plot=True)
        self.fileHasBeenModified()
        self.checkGui()

    def updateNXSData(self, row=0, source="spinbox", kind=["peak"]):
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxsdata_row = _list_nxsdata_sorted[row]
        if "peak" in kind:
            if source == "spinbox":
                peak1 = str(self.dataPeakFromValue.value())
                peak2 = str(self.dataPeakToValue.value())
            else:
                peak1 = self.tableWidget.item(row, 10).text()
                peak2 = self.tableWidget.item(row, 11).text()
            _nxsdata_row.peak = [peak1, peak2]
        if "back" in kind:
            if source == "spinbox":
                back1 = str(self.dataBackFromValue.value())
                back2 = str(self.dataBackToValue.value())
            else:
                back1 = self.tableWidget.item(row, 12).text()
                back2 = self.tableWidget.item(row, 13).text()
            _nxsdata_row.back = [back1, back2]
        _list_nxsdata_sorted[row] = _nxsdata_row
        self.list_nxsdata_sorted = _list_nxsdata_sorted
        self.updateTableWidgetPeakBackTof(row, force_spinbox_source=(source == "spinbox"))

    def checkRunReductionButton(self):
        _check_status_object = CheckSfRunReductionButtonStatus(parent=self)
        _is_everything_ok_to_go = _check_status_object.isEverythingReady()
        self.generateSFfileButton.setEnabled(_is_everything_ok_to_go)
        self.exportButton.setEnabled(_is_everything_ok_to_go)

    def attenuatorValueChanged(self, value):
        self.fileHasBeenModified()

    def fillGuiTable(self):
        FillSFGuiTable(parent=self, table=self.big_table, is_using_si_slits=self.is_using_si_slits)

    def fileHasBeenModified(self):
        dialog_title = self.window_title + self.current_loaded_file
        new_dialog_title = dialog_title + "*"
        self.setWindowTitle(new_dialog_title)
        self.checkGui()

    def resetFileHasBeenModified(self):
        dialog_title = self.window_title + self.current_loaded_file
        self.setWindowTitle(dialog_title)

    def updatePeakBackTofWidgets(self, row):
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxsdata_row = _list_nxsdata_sorted[row]
        if _nxsdata_row is None:
            return
        [peak1, peak2] = _nxsdata_row.peak
        if peak1 == "" or peak1 == "N/A":
            peak1 = -1
        self.dataPeakFromValue.setValue(int(peak1))
        if peak2 == "" or peak2 == "N/A":
            peak2 = 255
        self.dataPeakToValue.setValue(int(peak2))

        [back1, back2] = _nxsdata_row.back
        if back1 == "" or back1 == "N/A":
            back1 = -1
        self.dataBackFromValue.setValue(int(back1))
        if back2 == "" or back2 == "N/A":
            back2 = 255
        self.dataBackToValue.setValue(int(back2))

        if _nxsdata_row.tof_auto_flag:
            [tof1, tof2] = _nxsdata_row.tof_range_auto
        else:
            [tof1, tof2] = _nxsdata_row.tof_range
        [tof1ms, tof2ms] = convert_tof_values_unit([tof1, tof2])
        self.TOFmanualFromValue.setText("%.2f" % float(tof1ms))
        self.TOFmanualToValue.setText("%.2f" % float(tof2ms))
        self.manualTOFWidgetsEnabled(not _nxsdata_row.tof_auto_flag)

    def testPeakBackErrorWidgets(self):
        if self.list_nxsdata_sorted == []:
            _show_widgets_1 = False
            _show_widgets_2 = False
        else:
            back_to = int(self.dataBackToValue.text())
            back_from = int(self.dataBackFromValue.text())
            peak_to = int(self.dataPeakToValue.text())
            peak_from = int(self.dataPeakFromValue.text())
            back_flag = self.dataBackgroundFlag.isChecked()

            _show_widgets_1 = False
            _show_widgets_2 = False

            if peak_from == -1:
                self.peak1_error.setVisible(True)
                self.error_label.setVisible(True)

            if peak_to == -1:
                self.peak2_error.setVisible(True)
                self.error_label.setVisible(True)

            if back_from == -1:
                self.back1_error.setVisible(True)
                self.error_label.setVisible(True)

            if back_to == -1:
                self.back2_error.setVisible(True)
                self.error_label.setVisible(True)

            if back_flag:
                if back_from > peak_from:
                    _show_widgets_1 = True
                if back_to < peak_to:
                    _show_widgets_2 = True

        self.back1_error.setVisible(_show_widgets_1)
        self.peak1_error.setVisible(_show_widgets_1)
        self.back2_error.setVisible(_show_widgets_2)
        self.peak2_error.setVisible(_show_widgets_2)
        self.error_label.setVisible(_show_widgets_1 or _show_widgets_2)

    def enabledWidgets(self, is_enabled):
        self.yi_plot.setEnabled(is_enabled)
        self.yt_plot.setEnabled(is_enabled)
        self.dataBackFromLabel.setEnabled(is_enabled)
        self.dataBackToLabel.setEnabled(is_enabled)
        self.dataBackFromValue.setEnabled(is_enabled)
        self.dataBackToValue.setEnabled(is_enabled)
        self.dataPeakFromLabel.setEnabled(is_enabled)
        self.dataPeakToLabel.setEnabled(is_enabled)
        self.dataPeakFromValue.setEnabled(is_enabled)
        self.dataPeakToValue.setEnabled(is_enabled)
        self.dataBackgroundFlag.setEnabled(is_enabled)
        self.tableWidget.setEnabled(is_enabled)
        self.incidentMediumComboBox.setEnabled(is_enabled)
        self.toolButton.setEnabled(is_enabled)
        self.dataTOFautoMode.setEnabled(is_enabled)
        self.dataTOFmanualMode.setEnabled(is_enabled)
        if is_enabled:
            self.manualTOFWidgetsEnabled(self.dataTOFmanualMode.isChecked())
        else:
            self.manualTOFWidgetsEnabled(False)

    def manualTOFWidgetsEnabled(self, status):
        self.TOFmanualFromLabel.setEnabled(status)
        self.TOFmanualFromUnitsValue.setEnabled(status)
        self.TOFmanualFromValue.setEnabled(status)
        self.TOFmanualToLabel.setEnabled(status)
        self.TOFmanualToUnitsValue.setEnabled(status)
        self.TOFmanualToValue.setEnabled(status)

    def checkGui(self):
        if (self.loaded_list_of_runs != []) or (self.big_table is not None):
            wdg_enabled = True
        else:
            wdg_enabled = False
            self.setWindowTitle(self.window_title + self.current_loaded_file)
        self.testPeakBackErrorWidgets()
        self.tableWidget.setEnabled(wdg_enabled)
        self.checkRunReductionButton()
        self.enabledWidgets(wdg_enabled)

    def tableWidgetRowSelected(self):
        col = self.tableWidget.currentColumn()
        row = self.tableWidget.currentRow()
        self.tableWidgetCellSelected(row, col)

    def tableWidgetCellSelected(self, row, col):
        """
        This method is declared in the .ui
        """
        if col != 0:
            return
        self.showWhichRowIsLoading(row)
        QtWidgets.QApplication.processEvents()
        self.current_table_row_selected = row
        rangeSelected = QtWidgets.QTableWidgetSelectionRange(row, 0, row, 15)
        self.tableWidget.setRangeSelected(rangeSelected, True)
        self.displaySelectedRow(row)
        self.savePeakBackTofToBigTable(row)
        self.updatePeakBackTofWidgets(row)
        self.displayPlot(row, yt_plot=True, yi_plot=True)
        self.showWhichRowIsActivated(row)

    def showWhichRowIsLoading(self, row):
        nbr_row = self.tableWidget.rowCount()
        for i in range(nbr_row):
            if row == i:
                _item = QtWidgets.QTableWidgetItem("loading...")
            else:
                _item = QtWidgets.QTableWidgetItem("%d" % i)
            self.tableWidget.setVerticalHeaderItem(i, _item)

    def showWhichRowIsActivated(self, row):
        nbr_row = self.tableWidget.rowCount()
        for i in range(nbr_row):
            if row == i:
                _item = QtWidgets.QTableWidgetItem("ACTIVE")
            else:
                _item = QtWidgets.QTableWidgetItem("%d" % i)
            self.tableWidget.setVerticalHeaderItem(i, _item)

    def displaySelectedRow(self, row):
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        if _list_nxsdata_sorted == []:
            self.clearPlot()
            return
        _nxsdata_row = _list_nxsdata_sorted[row]
        if _nxsdata_row is None:
            self.loadSelectedNxsRuns(row)

    def savePeakBackTofToBigTable(self, row):
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxdata = _list_nxsdata_sorted[row]

        peak1 = self.tableWidget.item(row, 10).text()
        peak2 = self.tableWidget.item(row, 11).text()
        back1 = self.tableWidget.item(row, 12).text()
        back2 = self.tableWidget.item(row, 13).text()
        peak = [peak1, peak2]
        back = [back1, back2]
        _nxdata.peak = peak
        _nxdata.back = back

        if not _nxdata.tof_auto_flag:
            tof1 = self.tableWidget.item(row, 14).text()
            tof2 = self.tableWidget.item(row, 15).text()
            if float(tof1) < 1000:
                tof1 = str(float(tof1) * 1000)
                tof2 = str(float(tof2) * 1000)
                tof = [tof1, tof2]
            _nxdata.tof_range = tof

        _big_table = self.big_table
        tof_auto_flag = str2bool(_big_table[row, 16])
        _nxdata.tof_auto_flag = tof_auto_flag
        self.dataTOFautoMode.setChecked(tof_auto_flag)
        self.dataTOFmanualMode.setChecked(not tof_auto_flag)

        _list_nxsdata_sorted[row] = _nxdata
        self.list_nxsdata_sorted = _list_nxsdata_sorted

    def displayPlot(self, row=-1, yt_plot=True, yi_plot=True):
        if row == -1:
            row = self.current_table_row_selected
            if row == -1:
                self.clearPlot()
                return
        list_nxsdata_sorted = self.list_nxsdata_sorted
        nxsdata = list_nxsdata_sorted[row]
        self.clearPlot(yt_plot=yt_plot, yi_plot=yi_plot)
        if nxsdata is None:
            return
        if nxsdata.data_loaded is False:
            nxsdata.read_data()

        if yt_plot:
            self.plotYT(nxsdata, row)
        if yi_plot:
            self.plotYI(nxsdata, row)

    def plotYT(self, nxsdata, row):
        ytof = nxsdata.ytofdata
        tof_min_ms = float(nxsdata.tof_axis_auto_with_margin[0]) / 1000
        tof_max_ms = float(nxsdata.tof_axis_auto_with_margin[-1]) / 1000
        self.yt_plot.imshow(
            ytof,
            log=True,
            aspect="auto",
            origin="lower",
            extent=[tof_min_ms, tof_max_ms, 0, nxsdata.y.shape[0] - 1],
        )
        self.yt_plot.set_xlabel("t (ms)")
        self.yt_plot.set_ylabel("y (pixel)")

        [peak1, peak2] = nxsdata.peak
        [peak1, peak2] = self.forceTypeToInt([peak1, peak2])
        peak1 = int(peak1)
        peak2 = int(peak2)

        if self.dataTOFautoMode.isChecked():
            [tof1, tof2] = nxsdata.tof_range_auto
        else:
            [tof1, tof2] = nxsdata.tof_range
        tof1 = float(tof1) * 1e-3
        tof2 = float(tof2) * 1e-3

        self.yt_plot.canvas.ax.axvline(tof1, color=RefRed.colors.TOF_SELECTION_COLOR)
        self.yt_plot.canvas.ax.axvline(tof2, color=RefRed.colors.TOF_SELECTION_COLOR)

        if peak1 != -1:
            self.yt_plot.canvas.ax.axhline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        if peak2 != -1:
            self.yt_plot.canvas.ax.axhline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if nxsdata.back_flag:
            [back1, back2] = nxsdata.back
            [back1, back2] = self.forceTypeToInt([back1, back2], default_value=1)
            back1 = int(back1)
            back2 = int(back2)
            if back1 != -1:
                self.yt_plot.canvas.ax.axhline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            if back2 != -1:
                self.yt_plot.canvas.ax.axhline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        if nxsdata.all_plot_axis.is_yt_ylog:
            self.yt_plot.canvas.ax.set_yscale("log")
        else:
            self.yt_plot.canvas.ax.set_yscale("linear")

        if nxsdata.all_plot_axis.yt_data_interval is None:
            if nxsdata.new_detector_geometry_flag:
                ylim = 303
            else:
                ylim = 255
            self.yt_plot.canvas.ax.set_ylim(0, ylim)
            [xmin, xmax] = self.yt_plot.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.yt_plot.canvas.ax.yaxis.get_view_interval()
            nxsdata.all_plot_axis.yt_data_interval = [xmin, xmax, ymin, ymax]
            nxsdata.all_plot_axis.yt_view_interval = [xmin, xmax, ymin, ymax]
            self.yt_plot.toolbar.home_settings = [xmin, xmax, ymin, ymax]
            self.saveNXSdata(nxsdata, row)
        else:
            [xmin, xmax, ymin, ymax] = nxsdata.all_plot_axis.yt_view_interval
            self.yt_plot.canvas.ax.set_ylim([ymin, ymax])

        self.yt_plot.canvas.draw_idle()

    def plotYI(self, nxsdata, row):
        ycountsdata = nxsdata.ycountsdata
        xaxis = list(range(len(ycountsdata)))
        self.yi_plot.canvas.ax.plot(ycountsdata, xaxis)
        self.yi_plot.canvas.ax.set_xlabel("counts")
        self.yi_plot.canvas.ax.set_ylabel("y (pixel)")

        if nxsdata.all_plot_axis.yi_data_interval is None:
            ylim = nxsdata.number_y_pixels - 1
            self.yi_plot.canvas.ax.set_ylim(0, ylim)

        [peak1, peak2] = nxsdata.peak
        [peak1, peak2] = self.forceTypeToInt([peak1, peak2])
        peak1 = int(peak1)
        peak2 = int(peak2)
        if peak1 != -1:
            self.yi_plot.canvas.ax.axhline(peak1, color=RefRed.colors.PEAK_SELECTION_COLOR)
        if peak2 != -1:
            self.yi_plot.canvas.ax.axhline(peak2, color=RefRed.colors.PEAK_SELECTION_COLOR)

        if nxsdata.back_flag:
            [back1, back2] = nxsdata.back
            [back1, back2] = self.forceTypeToInt([back1, back2])
            back1 = int(back1)
            back2 = int(back2)
            if back1 != -1:
                self.yi_plot.canvas.ax.axhline(back1, color=RefRed.colors.BACK_SELECTION_COLOR)
            if back2 != -1:
                self.yi_plot.canvas.ax.axhline(back2, color=RefRed.colors.BACK_SELECTION_COLOR)

        if nxsdata.all_plot_axis.is_yi_xlog:
            self.yi_plot.canvas.ax.set_xscale("log")
        else:
            self.yi_plot.canvas.ax.set_xscale("linear")

        if nxsdata.all_plot_axis.yi_data_interval is None:
            [xmin, xmax] = self.yi_plot.canvas.ax.xaxis.get_view_interval()
            [ymin, ymax] = self.yi_plot.canvas.ax.yaxis.get_view_interval()
            nxsdata.all_plot_axis.yi_data_interval = [xmin, xmax, ymin, ymax]
            nxsdata.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
            self.yi_plot.toolbar.home_settings = [xmin, xmax, ymin, ymax]
            self.saveNXSdata(nxsdata, row)
        else:
            [xmin, xmax, ymin, ymax] = nxsdata.all_plot_axis.yi_view_interval
            self.yi_plot.canvas.ax.set_xlim([xmin, xmax])
            self.yi_plot.canvas.ax.set_ylim([ymin, ymax])

        self.yi_plot.canvas.draw_idle()

    def saveNXSdata(self, nxsdata, row):
        list_nxsdata_sorted = self.list_nxsdata_sorted
        list_nxsdata_sorted[row] = nxsdata
        self.list_nxsdata_sorted = list_nxsdata_sorted

    def clearPlot(self, yt_plot=True, yi_plot=True):
        if yt_plot:
            self.yt_plot.clear()
            self.yt_plot.draw()
        if yi_plot:
            self.yi_plot.clear()
            self.yi_plot.draw()

    def updateTableWidgetPeakBackTof(self, row, force_spinbox_source=False):
        if row == -1:
            return
        is_peak_back_fully_defined = self.isPeakOrBackFullyDefined(row=row)
        _list_nxsdata_sorted = self.list_nxsdata_sorted
        _nxdata = _list_nxsdata_sorted[row]
        if (not is_peak_back_fully_defined) or force_spinbox_source:
            self.updatePeakBackTofWidgets(row)
            _at_least_one_bad = False

            [peak1, peak2] = _nxdata.peak
            [back1, back2] = _nxdata.back

            if peak1 == "-1":
                peak1 = "N/A"
            self.tableWidget.item(row, 10).setText(peak1)
            if back1 > peak1:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_BAD)
                _font = QtGui.QFont()
                _font.setBold(True)
                _font.setItalic(True)
                _at_least_one_bad = True
            else:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_OK)
                _font = QtGui.QFont()
                _font.setBold(False)
                _font.setItalic(False)
            self.tableWidget.item(row, 10).setForeground(_brush)
            self.tableWidget.item(row, 10).setFont(_font)

            if peak2 == "-1":
                peak2 = "N/A"
            self.tableWidget.item(row, 11).setText(peak2)
            if back2 < peak2:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_BAD)
                _font = QtGui.QFont()
                _font.setBold(True)
                _font.setItalic(True)
                _at_least_one_bad = True
            else:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_OK)
                _font = QtGui.QFont()
                _font.setBold(False)
                _font.setItalic(False)
            self.tableWidget.item(row, 11).setFont(_font)
            self.tableWidget.item(row, 11).setForeground(_brush)

            if back1 == "-1":
                back1 = "N/A"
            self.tableWidget.item(row, 12).setText(back1)
            if back1 > peak1:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_BAD)
                _font = QtGui.QFont()
                _font.setBold(True)
                _font.setItalic(True)
                _at_least_one_bad = True
            else:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_OK)
                _font = QtGui.QFont()
                _font.setBold(False)
                _font.setItalic(False)
            self.tableWidget.item(row, 12).setFont(_font)
            self.tableWidget.item(row, 12).setForeground(_brush)

            if back2 == "-1":
                back2 = "N/A"
            self.tableWidget.item(row, 13).setText(back2)
            if back2 < peak2:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_BAD)
                _font = QtGui.QFont()
                _font.setBold(True)
                _font.setItalic(True)
                _at_least_one_bad = True
            else:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_OK)
                _font = QtGui.QFont()
                _font.setBold(False)
                _font.setItalic(False)
            self.tableWidget.item(row, 13).setFont(_font)
            self.tableWidget.item(row, 13).setForeground(_brush)

            tof_auto_flag = _nxdata.tof_auto_flag
            self.dataTOFautoMode.setChecked(tof_auto_flag)
            self.dataTOFmanualMode.setChecked(not tof_auto_flag)
            if tof_auto_flag:
                [tof1, tof2] = _nxdata.tof_range_auto
            else:
                [tof1, tof2] = _nxdata.tof_range

            if float(tof1) > 1000:
                tof1 = "%.2f" % (float(tof1) / 1000)
                tof2 = "%.2f" % (float(tof2) / 1000)

            self.tableWidget.item(row, 14).setText(tof1)
            _brush_OK = QtGui.QBrush()
            _brush_OK.setColor(RefRed.colors.VALUE_OK)
            self.tableWidget.item(row, 14).setForeground(_brush_OK)

            self.tableWidget.item(row, 15).setText(tof2)
            _brush_OK = QtGui.QBrush()
            _brush_OK.setColor(RefRed.colors.VALUE_OK)
            self.tableWidget.item(row, 15).setForeground(_brush_OK)

            if _at_least_one_bad:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_BAD)
                _font = QtGui.QFont()
                _font.setBold(True)
                _font.setItalic(True)
            else:
                _brush = QtGui.QBrush()
                _brush.setColor(RefRed.colors.VALUE_OK)
                _font = QtGui.QFont()
                _font.setBold(False)
                _font.setItalic(False)
            self.tableWidget.item(row, 10).setFont(_font)
            self.tableWidget.item(row, 10).setForeground(_brush)

        else:
            self.savePeakBackTofToBigTable(row)
            self.updatePeakBackTofWidgets(row)

    def isPeakOrBackFullyDefined(self, row=-1):
        if row == -1:
            return False
        for col in range(10, 14):
            _value = self.tableWidget.item(row, col).text()
            if _value == "N/A":
                return False
        return True

    def savingConfiguration(self):
        """
        TODO: this is broken functionality that never worked and is not needed
        This function is a UI slot.
        """
        raise RuntimeError("Method SFCalculator.savingConfiguration is deprecated.")

    def savingAsConfiguration(self):
        """
        TODO: this is broken functionality that never worked and is not needed
        This function is a UI slot.
        """
        raise RuntimeError("Method SFCalculator.savingAsConfiguration is deprecated.")

    def importConfiguration(self, filename):
        """
        TODO: this is broken functionality that never worked and is not needed
        As far as I know this function isn't called anywhere else in the code.
        """
        raise RuntimeError("Method SFCalculator.importConfiguration is deprecated.")

    def tof_validation(self, tof_auto_switch, tof1, tof2, with_plot_update=True):
        self.dataTOFautoMode.setChecked(tof_auto_switch)
        self.dataTOFmanualMode.setChecked(not tof_auto_switch)
        self.manualTOFWidgetsEnabled(not tof_auto_switch)
        self.TOFmanualFromValue.setText("%.2f" % tof1)
        self.TOFmanualToValue.setText("%.2f" % tof2)
        self.manualTOFtextFieldValidated(with_plot_update=with_plot_update)
