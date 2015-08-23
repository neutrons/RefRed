import sys
import time
import numpy as np

from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker
from RefRed.autopopulatemaintable.extract_lconfigdataset_runs import ExtractLConfigDataSetRuns
from RefRed.thread.locate_run import LocateRunThread
from RefRed.calculations.load_list_nexus import LoadListNexus
from RefRed.calculations.sort_lrdata_list import SortLRDataList
from RefRed.calculations.lr_data import LRData
from RefRed.autopopulatemaintable.populate_reduction_table_from_list_lrdata import PopulateReductionTableFromListLRData

class ReductionTableAutoFill(object):

    list_full_file_name = []
    list_nxs = []
    list_lradata = []

    list_lrdata_sorted = []
    list_runs_sorted = []
    list_wks_sorted = []

    def __init__(self, main_gui=None, 
                 list_of_run_from_input='',
                 data_type_selected='data', 
                 reset_table=False):

        if list_of_run_from_input == '':
            return

        if data_type_selected != 'data':
            self.data_type_selected = 'norm'
        else:
            self.data_type_selected = 'data'
        if list_of_run_from_input == '':
            self.sorted_list_of_runs = []
            return

        self.raw_run_from_input = list_of_run_from_input
        self.list_of_run_from_input = None
        self.main_gui = main_gui
        self.list_of_run_from_lconfig = None
        self.full_list_of_runs = None
        self.list_lrdata_sorted = None

        self.runs_found = 0

        self.number_of_runs = None
        self.filename_thread_array = None
        self.number_of_runs = None
        self.list_nxs_sorted = None

        self.calculate_discrete_list_of_runs() # step1 -> list_new_runs

        self.big_table_data = None
        if not reset_table:
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
        
    def run(self):
        self.locate_runs()
        self.loading_runs()
        self.loading_lrdata()
        self.sorting_runs()
        self.updating_reductionTable()

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

    def loading_runs(self):
        _list_full_file_name = self.list_nxs
        _list_run = self.full_list_of_runs
        
        o_load_list = LoadListNexus(list_nexus = _list_full_file_name,
                                    list_run = _list_run,
                                    metadata_only = False)
        self.list_wks_loaded = o_load_list.list_wks_loaded

    def loading_lrdata(self):
        _list_wks_loaded = self.list_wks_loaded
        _list_lrdata = []
        for index in range(len(_list_wks_loaded)):
            _lrdata = LRData(_list_wks_loaded[index])
            _list_lrdata.append(_lrdata)
        self.list_lrdata = _list_lrdata

    def sorting_runs(self):
        o_wks_sorted = SortLRDataList(parent = self.main_gui,
                                   list_lrdata = np.array(self.list_lrdata),
                                   list_runs = np.array(self.full_list_of_runs),
                                   list_wks = np.array(self.list_wks_loaded),
                                   data_type_selected = self.data_type_selected)

        o_wks_sorted.run()
        self.list_lrdata_sorted = o_wks_sorted.list_lrdata_sorted
        self.list_runs_sorted = o_wks_sorted.list_runs_sorted
        self.list_wks_sorted = o_wks_sorted.list_wks_sorted
        
    def updating_reductionTable(self):
        list_lrdata_sorted = self.list_lrdata_sorted
        list_runs_sorted = self.list_runs_sorted
        list_wks_sorted = self.list_wks_sorted
        o_pop_reduction_table = PopulateReductionTableFromListLRData(parent=self.main_gui,
                                                                     list_lrdata = list_lrdata_sorted,
                                                                     list_wks = list_wks_sorted,
                                                                     list_run = list_runs_sorted,
                                                                     is_data = True)

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
        main_gui = self.main_gui
        if main_gui is None:
            return
        _big_table_data = main_gui.big_table_data
        self.big_table_data = _big_table_data
        _extract_runs = ExtractLConfigDataSetRuns(_big_table_data[:, 2])
        self.list_of_run_from_lconfig = _extract_runs.list_runs()

    def remove_duplicate_runs(self):
        full_list_of_runs = self.full_list_of_runs
        full_list_without_duplicate = list(set(full_list_of_runs))
        self.full_list_of_runs = full_list_without_duplicate


if __name__ == "__main__":
    maintable = MainTableAutoFill('1, 2, 3, 5-10, 15, 16', reset_table=True)

