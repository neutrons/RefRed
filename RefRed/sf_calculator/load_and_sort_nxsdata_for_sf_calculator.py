from qtpy import QtWidgets
import numpy as np
import mantid.simpleapi as api

from RefRed.sf_calculator.sort_nxsdata import SortNXSData
from RefRed.sf_calculator.lr_data import LRData

INSTRUMENT_SHORT_NAME = "REF_L"


class LoadAndSortNXSDataForSFcalculator(object):
    list_runs = []
    loaded_list_runs = []
    list_NXSData = []
    list_NXSData_sorted = []
    list_metadata = [
        'gd_prtn_chrg',
        'S1HWidth',
        'S1VHeight',
        'S2HWidth',
        'S2VHeight',
        'SiHWidth',
        'SiVHeight',
        'LambdaRequest',
        'vATT',
    ]
    big_table = []
    is_using_si_slits = False
    sf_gui = None

    def __init__(self, list_runs, parent=None, read_options=None, sort_by_metadata=False):
        # parse input
        self.list_runs = sorted(set(list_runs))
        self.read_options = read_options
        self.sf_gui = parent
        self._sort_by_metadata = sort_by_metadata
        # local container
        self.list_NXSData = []
        self.big_table = []
        self.loaded_list_runs = []
        # NOTE: sorting is done on the fly with the loading of each run
        self.loadNXSData()

    def loadNXSData(self):
        for _runs in self.list_runs:
            _full_file_name = api.FileFinder.findRuns("%s_%d" % (INSTRUMENT_SHORT_NAME, int(_runs)))[0]
            if _full_file_name != '':
                workspace = api.LoadEventNexus(
                    Filename=_full_file_name, OutputWorkspace="__data_file_%s" % _runs, MetaDataOnly=False
                )
                _data = LRData(workspace, read_options=self.read_options)
                if _data is not None:
                    self.list_NXSData.append(_data)
                    #
                    if _runs not in self.loaded_list_runs:
                        self.loaded_list_runs.append(_runs)
                    #
                    if self._sort_by_metadata:
                        self.sortNXSData()
                    else:
                        self.list_NXSData_sorted = self.list_NXSData
                    #
                    self.fillTable()
                    self.sf_gui.update_table(self, False)
                    QtWidgets.QApplication.processEvents()

    def sortNXSData(self):
        if self.list_NXSData == []:
            return
        oSortNXSDataArray = SortNXSData(self.list_NXSData, parent=self.sf_gui)
        self.list_NXSData_sorted = oSortNXSDataArray.getSortedList()

    def fillTable(self):
        _list_NXSData_sorted = self.list_NXSData_sorted
        if _list_NXSData_sorted == []:
            return
        nbr_row = len(_list_NXSData_sorted)
        nbr_column = len(self.list_metadata) + 8  # +1 for the run number + peak/back/tof/auto_flag
        big_table = np.empty((nbr_row, nbr_column))
        index_row = 0
        for _active_data in _list_NXSData_sorted:
            _run_number = _active_data.run_number
            _nbr_attenuator = _active_data.attenuatorNbr
            _lambda_min = _active_data.lambda_range[0]
            _lambda_max = _active_data.lambda_range[1]
            _proton_charge = _active_data.proton_charge
            _lambda_requested = _active_data.lambda_requested
            _S1W = _active_data.S1W
            _S1H = _active_data.S1H
            self.is_using_si_slits = _active_data.isSiThere
            if _active_data.isSiThere:
                _Si2W = _active_data.SiW
                _Si2H = _active_data.SiH
            else:
                _Si2W = _active_data.S2W
                _Si2H = _active_data.S2H
            _peak1 = _active_data.peak[0]
            _peak2 = _active_data.peak[1]
            _back1 = _active_data.back[0]
            _back2 = _active_data.back[1]
            _tof1 = _active_data.tof_range_auto[0]
            _tof2 = _active_data.tof_range_auto[1]
            if _active_data.tof_auto_flag:
                _tof_auto_flag = 1
            else:
                _tof_auto_flag = 0

            _row = [
                _run_number,
                _nbr_attenuator,
                _lambda_min,
                _lambda_max,
                _proton_charge,
                _lambda_requested,
                _S1W,
                _S1H,
                _Si2W,
                _Si2H,
                _peak1,
                _peak2,
                _back1,
                _back2,
                _tof1,
                _tof2,
                _tof_auto_flag,
            ]
            big_table[index_row, :] = _row
            index_row += 1
        self.big_table = big_table

    def isSiThere(self):
        return self.is_using_Si_slits

    def retrieveMetadataValue(self, _name):
        mt_run = self.mt_run
        _value = mt_run.getProperty(_name).value
        if isinstance(_value, float):
            _value = str(_value)
        elif len(_value) == 1:
            _value = str(_value)
        elif isinstance(_value, str):
            _value = _value
        else:
            _value = '[' + str(_value[0]) + ',...]' + '-> (' + str(len(_value)) + ' entries)'
        return _value

    def getTableData(self):
        return self.big_table

    def getListOfRunsLoaded(self):
        return self.loaded_list_runs

    def getListNXSDataSorted(self):
        return self.list_NXSData_sorted
