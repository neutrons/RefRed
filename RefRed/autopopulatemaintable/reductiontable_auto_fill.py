import sys
import time
import numpy as np
from PyQt4.QtGui import QApplication

from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker
from RefRed.autopopulatemaintable.extract_lconfigdataset_runs import ExtractLConfigDataSetRuns
from RefRed.thread.locate_run import LocateRunThread
from RefRed.calculations.load_list_nexus import LoadListNexus
from RefRed.calculations.sort_lrdata_list import SortLRDataList
from RefRed.calculations.lr_data import LRData
from RefRed.autopopulatemaintable.populate_reduction_table_from_list_lrdata import PopulateReductionTableFromListLRData
from RefRed.calculations.check_list_run_compatibility_and_display_thread import CheckListRunCompatibilityAndDisplayThread
from RefRed.calculations.check_list_run_compatibility_and_display import CheckListRunCompatibilityAndDisplay
from RefRed.utilities import format_to_list
from RefRed.autopopulatemaintable.auto_fill_widgets_handler import AutoFillWidgetsHandler


class ReductionTableAutoFill(object):

    list_full_file_name = []
    list_nxs = []
    list_lrdata = []

    list_lrdata_sorted = []
    list_runs_sorted = []
    list_wks_sorted = []
    list_nexus_sorted = []

    data_type_selected = 'data'
    o_auto_fill_widgets_handler = None

    def __init__(self, parent=None, 
                 list_of_run_from_input='',
                 data_type_selected='data', 
                 reset_table=False):

        if list_of_run_from_input == '':
            return

        if data_type_selected != 'data':
            data_type_selected = 'norm'
        self.data_type_selected = data_type_selected

        if list_of_run_from_input == '':
            self.sorted_list_of_runs = []
            return

        self.init_variable()

        self.parent = parent
        is_minimum_requirements = self.check_minimum_requirements()
        if is_minimum_requirements is False:
            return
        
        self.o_auto_fill_widgets_handler = AutoFillWidgetsHandler(parent=self.parent)
        self.o_auto_fill_widgets_handler.setup()

        self.raw_run_from_input = list_of_run_from_input

        self.calculate_discrete_list_of_runs() # step1 -> list_new_runs

        self.big_table_data = None
        if (not reset_table) and (data_type_selected == 'data'):
            self.retrieve_bigtable_list_data_loaded() # step2 -> list_old_runs

        _full_list_of_runs = []
        if self.list_of_run_from_input is not None:
            for _run in self.list_of_run_from_input:
                _full_list_of_runs.append(int(_run))
        if self.list_of_run_from_lconfig is not None:
            for _run in self.list_of_run_from_lconfig:
                _full_list_of_runs.append(int(_run))
        self.full_list_of_runs = _full_list_of_runs

        self.remove_duplicate_runs()
        
        # start calculation
        self.run()

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

    def check_minimum_requirements(self):
        _data_type_selected = self.data_type_selected
        if _data_type_selected == 'data':
            return True
            
        big_table_data = self.parent.big_table_data
        if big_table_data[0,0] is None:
            return False

    def run(self):
        self.locate_runs()
        if self.runs_found == 0:
            return
        self.loading_runs()
        self.loading_lrdata()
        self.sorting_runs()
        self.updating_reductionTable()
        self.loading_full_reductionTable()
        self.o_auto_fill_widgets_handler.end()
        
    def loading_full_reductionTable(self):
        _list_nexus_sorted = self.list_nexus_sorted
        _list_run_sorted = self.list_runs_sorted
        _data_type_selected = self.data_type_selected
        _is_working_with_data_column = True if self.data_type_selected == 'data' else False
        _list_run_sorted = format_to_list(_list_run_sorted)
        _list_nexus_sorted = format_to_list(_list_nexus_sorted)
        
        self.parent.ui.progressBar_check5.setMinimum(0)
        self.parent.ui.progressBar_check5.setValue(0)
        self.parent.ui.progressBar_check5.setMaximum(len(_list_nexus_sorted))
        self.parent.ui.progressBar_check5.setVisible(True)
        QApplication.processEvents()
        
        for index, nexus in enumerate(_list_nexus_sorted):
            _is_display_requested = self.display_of_this_row_checked(index)
            _list_run = format_to_list(_list_run_sorted[index])
            _nexus = format_to_list(nexus)
            o_check_and_load = CheckListRunCompatibilityAndDisplay(parent=self.parent,
                                                                   list_run = _list_run,
                                                                   list_nexus = _nexus,
                                                                   row = index,
                                                                   is_working_with_data_column = _is_working_with_data_column,
                                                                   is_display_requested = _is_display_requested)
            o_check_and_load.run()
            self.parent.ui.progressBar_check5.setValue(index+1)
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
            
        if self.runs_found > 0:
            self.o_auto_fill_widgets_handler.step1()
        else:
            self.o_auto_fill_widgets_handler.error_step1()

    def loading_runs(self):
        _list_full_file_name = self.list_nxs
        _list_run = self.full_list_of_runs
        
        o_load_list = LoadListNexus(list_nexus = _list_full_file_name,
                                    list_run = _list_run,
                                    metadata_only = False)
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
            _lrdata = LRData(_list_wks_loaded[index])
            _list_lrdata.append(_lrdata)
            self.parent.ui.progressBar_check2.setValue(index+1)
            QApplication.processEvents()
        self.list_lrdata = _list_lrdata
        
        self.o_auto_fill_widgets_handler.step2()

    def sorting_runs(self):
        o_wks_sorted = SortLRDataList(parent = self.parent,
                                      list_lrdata = np.array(self.list_lrdata),
                                      list_runs = np.array(self.full_list_of_runs),
                                      list_wks = np.array(self.list_wks_loaded),
                                      list_nexus = np.array(self.list_nexus_loaded),
                                      data_type_selected = self.data_type_selected)

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
        is_data = True if self.data_type_selected == 'data' else False
        o_pop_reduction_table = PopulateReductionTableFromListLRData(parent=self.parent,
                                                                     list_lrdata = list_lrdata_sorted,
                                                                     list_wks = list_wks_sorted,
                                                                     list_run = list_runs_sorted,
                                                                     is_data = is_data)
        
        self.o_auto_fill_widgets_handler.step4()

    def init_filename_thread_array(self, sz):
        _filename_thread_array = []
        _list_full_file_name = []
        for i in range(sz):
            _filename_thread_array.append(LocateRunThread())
            _list_full_file_name.append('')
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

    def remove_duplicate_runs(self):
        full_list_of_runs = self.full_list_of_runs
        full_list_without_duplicate = list(set(full_list_of_runs))
        self.full_list_of_runs = full_list_without_duplicate


if __name__ == "__main__":
    maintable = MainTableAutoFill('1, 2, 3, 5-10, 15, 16', reset_table=True)

