# import sys
import time
from itertools import chain

import numpy as np
from qtpy.QtWidgets import QApplication

from refred.autopopulatemaintable.auto_fill_widgets_handler import AutoFillWidgetsHandler
from refred.autopopulatemaintable.extract_lconfigdataset_runs import ExtractLConfigDataSetRuns
from refred.autopopulatemaintable.populate_reduction_table_from_list_lrdata import PopulateReductionTableFromListLRData
from refred.background_tasks.locate_run import LocateRunThread
from refred.calculations.check_list_run_compatibility_and_display import CheckListRunCompatibilityAndDisplay
from refred.calculations.load_list_nexus import LoadListNexus
from refred.calculations.lr_data import LRData
from refred.calculations.run_sequence_breaker import RunSequenceBreaker
from refred.calculations.sort_lrdata_list import SortLRDataList
from refred.mantid_utility import MantidUtility
from refred.nexus_utilities import get_run_number
from refred.utilities import format_to_list


class ReductionTableAutoFill(object):
    list_full_file_name = []
    list_nxs = []
    list_lrdata = []

    list_lrdata_sorted = []
    list_runs_sorted = []
    list_wks_sorted = []
    list_nexus_sorted = []

    data_type_selected = "data"
    o_auto_fill_widgets_handler = None

    def __init__(self, parent=None, list_of_run_from_input="", data_type_selected="data", reset_table=False):
        self.parent = parent

        if data_type_selected == "data":
            # add to norm box, previous loaded norm
            _str_old_runs = self.retrieve_list_norm_previously_loaded()
            if not _str_old_runs == "":
                _live_norm_edit = str(self.parent.ui.norm_sequence_lineEdit.text())
                if not (_live_norm_edit == ""):
                    new_str = _live_norm_edit + "," + _str_old_runs
                else:
                    new_str = _str_old_runs
                self.parent.ui.norm_sequence_lineEdit.setText(new_str)

        self.browsing_files_flag = False
        if self.parent.browsed_files[data_type_selected] is not None:
            self.browsing_files_flag = True

        if list_of_run_from_input == "":
            self.sorted_list_of_runs = []
            if not self.browsing_files_flag:
                return

        if data_type_selected != "data":
            data_type_selected = "norm"
        self.data_type_selected = data_type_selected

        self.init_variable()

        self.reset_table = reset_table

        is_minimum_requirements = self.check_minimum_requirements()
        if is_minimum_requirements is False:
            return

        self.o_auto_fill_widgets_handler = AutoFillWidgetsHandler(parent=self.parent)
        self.o_auto_fill_widgets_handler.setup()

        if self.browsing_files_flag:
            _full_list_of_runs = []
            if self.list_of_run_from_lconfig is not None:
                for _run in self.list_of_run_from_lconfig:
                    _full_list_of_runs.append(int(_run))
            self.full_list_of_runs = _full_list_of_runs

        else:
            self.merge_list_of_runs(new_runs=list_of_run_from_input)

        # start calculation
        self.run()

    def merge_list_of_runs(self, new_runs=None):
        # manual entry of the runs
        self.raw_run_from_input = new_runs
        self.calculate_discrete_list_of_runs()  # step1 -> list_of_runs_from_input

        self.big_table_data = None
        if (not self.reset_table) and (self.data_type_selected == "data"):
            self.retrieve_bigtable_list_data_loaded()  # step2 -> list_of_runs_from_lconfig

        _full_list_of_runs = []
        if self.list_of_run_from_input is not None:
            for _run in self.list_of_run_from_input:
                _full_list_of_runs.append(int(_run))

        if self.list_of_run_from_lconfig is not None:
            for _run in self.list_of_run_from_lconfig:
                _full_list_of_runs.append(int(_run))
        self.full_list_of_runs = _full_list_of_runs

        self.remove_duplicate_runs()

    def init_variable(self):
        self.list_full_file_name = []
        self.list_nxs = []
        self.lrdata = []
        self.list_lrdata_sorted = []
        self.list_runs_sorted = []
        self.list_wks_sorted = []
        self.list_nexus_sorted = []
        self.full_list_of_runs = None
        self.list_of_run_from_input = None
        self.list_of_run_from_lconfig = None
        self.list_lrdata_sorted = None
        self.runs_found = 0
        self.number_of_runs = None
        self.filename_thread_array = None
        self.number_of_runs = None
        self.list_nexus_sorted = None
        self.list_nexus_loaded = None

    def run(self):
        self.cleanup_workspaces()
        self.locate_runs()
        self.add_browsed_runs()
        self.retrieve_list_of_runs_from_nexus_metadata()
        if self.runs_found == 0:
            return
        self.loading_runs()
        self.loading_lrdata()
        self.sorting_runs()
        self.updating_reductionTable()
        self.loading_full_reductionTable()
        self.o_auto_fill_widgets_handler.end()
        self.cleanup()

    def cleanup(self):
        self.parent.browsed_files[self.data_type_selected] = None

    def cleanup_workspaces(self):
        o_mantid_utility = MantidUtility(parent=self.parent)
        o_mantid_utility.cleanup_workspaces()

    def loading_full_reductionTable(self):
        _list_nexus_sorted = self.list_nexus_sorted
        _list_runs_sorted = self.list_runs_sorted
        # _data_type_selected = self.data_type_selected
        _is_working_with_data_column = True if self.data_type_selected == "data" else False

        self.parent.ui.progressBar_check5.setMinimum(0)
        self.parent.ui.progressBar_check5.setValue(0)
        self.parent.ui.progressBar_check5.setMaximum(len(_list_nexus_sorted))
        self.parent.ui.progressBar_check5.setVisible(True)
        QApplication.processEvents()

        for index, nexus in enumerate(_list_nexus_sorted):
            _is_display_requested = self.display_of_this_row_checked(index)
            _list_run = format_to_list(_list_runs_sorted[index])
            _nexus = format_to_list(nexus)
            o_check_and_load = CheckListRunCompatibilityAndDisplay(
                parent=self.parent,
                list_run=_list_run,
                list_nexus=_nexus,
                row=index,
                is_working_with_data_column=_is_working_with_data_column,
                is_display_requested=_is_display_requested,
            )
            o_check_and_load.run()
            self.parent.ui.progressBar_check5.setValue(index + 1)
            QApplication.processEvents()

        self.o_auto_fill_widgets_handler.step5()

    def display_of_this_row_checked(self, row):
        _button_status = self.parent.ui.reductionTable.cellWidget(row, 0).checkState()
        if _button_status == 2:
            return True
        return False

    def locate_runs(self):
        _list_of_runs = self.full_list_of_runs
        self.number_of_runs = len(_list_of_runs)
        self.runs_found = 0
        self.init_filename_thread_array(len(_list_of_runs))
        for index, _run in enumerate(_list_of_runs):
            _thread = self.filename_thread_array[index]
            _thread.setup(self, _run, index)
            _thread.start()

        while self.runs_found < self.number_of_runs:
            time.sleep(0.5)

        if (self.runs_found > 0) or (self.browsing_files_flag):
            self.o_auto_fill_widgets_handler.step1()
        else:
            self.o_auto_fill_widgets_handler.error_step1()

    def add_browsed_runs(self):
        if self.parent.browsed_files[self.data_type_selected] is None:
            return

        list_nxs_browsed = self.parent.browsed_files[self.data_type_selected]
        list_nxs = self.list_nxs

        new_list_nxs = list(chain(list_nxs, list_nxs_browsed))
        self.list_nxs = new_list_nxs

        _nbr_files = len(list_nxs_browsed)
        self.runs_found += _nbr_files

    def retrieve_list_of_runs_from_nexus_metadata(self):
        _list_nxs = self.list_nxs
        _list_runs = []
        for _nxs in _list_nxs:
            _run = get_run_number(_nxs)
            if _run is not None:
                _list_runs.append(_run)

        self.full_list_of_runs = _list_runs

    def loading_runs(self):
        _list_full_file_name = self.list_nxs
        _list_run = self.full_list_of_runs
        _prefix = self.data_type_selected
        o_load_list = LoadListNexus(
            list_nexus=_list_full_file_name, list_run=_list_run, metadata_only=False, prefix=_prefix
        )
        self.list_wks_loaded = o_load_list.list_wks_loaded
        self.list_nexus_loaded = o_load_list.list_nexus_loaded

    def loading_lrdata(self):
        _list_wks_loaded = self.list_wks_loaded
        _list_lrdata = []

        self.parent.ui.progressBar_check2.setMinimum(0)
        self.parent.ui.progressBar_check2.setValue(0)
        self.parent.ui.progressBar_check2.setMaximum(len(_list_wks_loaded))
        self.parent.ui.progressBar_check2.setVisible(True)
        QApplication.processEvents()

        for index in range(len(_list_wks_loaded)):
            _lrdata = LRData(_list_wks_loaded[index], parent=self.parent)
            _list_lrdata.append(_lrdata)
            self.parent.ui.progressBar_check2.setValue(index + 1)
            QApplication.processEvents()
        self.list_lrdata = _list_lrdata

        self.o_auto_fill_widgets_handler.step2()

    def sorting_runs(self):
        o_wks_sorted = SortLRDataList(
            parent=self.parent,
            list_lrdata=np.array(self.list_lrdata),
            list_runs=np.array(self.full_list_of_runs),
            list_wks=np.array(self.list_wks_loaded),
            list_nexus=np.array(self.list_nexus_loaded),
            data_type_selected=self.data_type_selected,
        )

        o_wks_sorted.run()
        self.list_lrdata_sorted = o_wks_sorted.list_lrdata_sorted
        self.list_runs_sorted = o_wks_sorted.list_runs_sorted
        self.list_wks_sorted = o_wks_sorted.list_wks_sorted
        self.list_nexus_sorted = o_wks_sorted.list_nexus_sorted
        self.o_auto_fill_widgets_handler.step3()

    def updating_reductionTable(self):
        list_lrdata_sorted = self.list_lrdata_sorted
        list_runs_sorted = self.list_runs_sorted
        list_wks_sorted = self.list_wks_sorted
        list_nexus_sorted = self.list_nexus_sorted
        is_data = True if self.data_type_selected == "data" else False
        o_pop_reduction_table = PopulateReductionTableFromListLRData(
            parent=self.parent,
            list_lrdata=list_lrdata_sorted,
            list_wks=list_wks_sorted,
            list_run=list_runs_sorted,
            list_nexus=list_nexus_sorted,
            is_data=is_data,
        )
        if not is_data:
            self.list_runs_sorted = o_pop_reduction_table.list_runs_sorted
            self.list_lrdata_sorted = o_pop_reduction_table.list_lrdata_sorted
            self.list_wks_sorted = o_pop_reduction_table.list_wks_sorted
            self.list_nexus_sorted = o_pop_reduction_table.list_nexus_sorted

        self.o_auto_fill_widgets_handler.step4()

    def init_filename_thread_array(self, sz):
        _filename_thread_array = []
        _list_full_file_name = []
        for i in range(sz):
            _filename_thread_array.append(LocateRunThread())
            _list_full_file_name.append("")
        self.filename_thread_array = _filename_thread_array
        self.list_nxs = _list_full_file_name

    def calculate_discrete_list_of_runs(self):
        _raw_run_from_input = self.raw_run_from_input
        sequence_breaker = RunSequenceBreaker(_raw_run_from_input)
        self.list_of_run_from_input = sequence_breaker.final_list

    def retrieve_bigtable_list_data_loaded(self):
        parent = self.parent
        if parent is None:
            return
        _big_table_data = parent.big_table_data
        self.big_table_data = _big_table_data
        _extract_runs = ExtractLConfigDataSetRuns(_big_table_data[:, 2])
        self.list_of_run_from_lconfig = _extract_runs.list_runs()

    def retrieve_list_norm_previously_loaded(self):
        parent = self.parent
        if parent is None:
            return
        _big_table_data = parent.big_table_data
        _extract_runs = ExtractLConfigDataSetRuns(_big_table_data[:, 2], data_type="norm")
        _runs = _extract_runs.list_runs()
        _str_runs = ",".join([str(run) for run in _runs])
        return _str_runs

    def remove_duplicate_runs(self):
        full_list_of_runs = self.full_list_of_runs
        full_list_without_duplicate = list(set(full_list_of_runs))
        self.full_list_of_runs = full_list_without_duplicate

    def check_minimum_requirements(self):
        _data_type_selected = self.data_type_selected
        if _data_type_selected == "data":
            return True

        big_table_data = self.parent.big_table_data
        if big_table_data[0, 0] is None:
            return False
