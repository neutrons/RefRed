import numpy as np

class PopulateReductionTableFromListLRData(object):

    list_lrdata_sorted = None
    list_wks_sorted = None
    list_runs_sorted = None
    list_nexus_sorted = None
    
    def __init__(self, parent=None,
                 list_lrdata = None,
                 list_wks = None,
                 list_run = None,
                 list_nexus = None,
                 is_data = True):
        
        self.parent = parent
        self.list_run = list_run
        self.list_lrdata = list_lrdata
        self.list_wks = list_wks
        self.list_nexus = list_nexus
        self.is_data = is_data

        if not is_data:
            self.list_lrdata_sorted = None
            self.list_wks_sorted = None
            self.list_runs_sorted = None
            self.list_nexus_sorted = None

        self.big_table_data = self.parent.big_table_data

        if self.is_data:
            self.reductionTable_col = 1
            self.big_table_data_col = 0
        else:
            self.reductionTable_col = 2
            self.big_table_data_col = 1

        if is_data:
            self.clear_reductionTable()
            
        self.insert_runs_into_table()    
        
        if is_data:
            self.clear_big_table_data()
            self.update_big_table_data()
                
        self.parent.big_table_data = self.big_table_data
                
    def update_big_table_data(self):
        list_lrdata = self.list_lrdata
        big_table_data = self.big_table_data
        for _index, _wks in enumerate(self.list_wks):
            if type(_wks) == type([]):
                pass
            else:
                _lrdata = list_lrdata[_index]

            big_table_data[_index, self.big_table_data_col] = _lrdata
        self.big_table_data = big_table_data
                                
    def insert_runs_into_table(self):
        if self.is_data:
            self.insert_data_runs_into_table()
        else:
            self.insert_norm_runs_into_table()

    def insert_norm_runs_into_table(self):
        _list_lrdata = self.list_lrdata
        _list_run = self.list_run
        _list_wks = self.list_wks
        _list_nexus = self.list_nexus
        
        _list_norm_lrdata_sorted = []
        _list_norm_runs_sorted = []
        _list_norm_wks_sorted = []
        _list_norm_nexus_sorted = []
        
        _big_table_data = self.big_table_data

        # retrive data column lrdata
        _list_data_lrdata = _big_table_data[:,0]
        _data_index = 0
        _data_lrdata = _list_data_lrdata[_data_index]
        while (_data_lrdata is not None):
            _data_lambda_value = _data_lrdata.lambda_requested
            for _norm_index, _norm_lrdata in enumerate(_list_lrdata):
                _norm_lambda_value = _norm_lrdata.lambda_requested
                if (_norm_lambda_value == _data_lambda_value):
                    _run = _list_run[_norm_index]
                    _list_norm_lrdata_sorted.append(_norm_lrdata)
                    _list_norm_runs_sorted.append(_run)
                    _list_norm_wks_sorted.append(_list_wks[_norm_index])
                    _list_norm_nexus_sorted.append(_list_nexus[_norm_index])
                    if type(_run) == type([]):
                        str_run = ",".join(_run)
                    else:
                        str_run = str(_run)
                    self.parent.ui.reductionTable.item(_data_index, 
                                                       self.reductionTable_col).setText(str_run)
                    break
            _data_index += 1
            _data_lrdata = _list_data_lrdata[_data_index]

        self.list_lrdata_sorted = _list_norm_lrdata_sorted
        self.list_runs_sorted = _list_norm_runs_sorted
        self.list_wks_sorted = _list_norm_wks_sorted
        self.list_nexus_sorted = _list_norm_nexus_sorted
            
    def insert_data_runs_into_table(self):
        for _index, _run in enumerate(self.list_run):
            if type(_run) == type([]):
                str_run = ",".join(_run)
            else:
                str_run = str(_run)
            self.parent.ui.reductionTable.item(_index, self.reductionTable_col).setText(str_run)
            
    def clear_reductionTable(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")
                
    def clear_big_table_data(self):
        self.big_table_data = np.empty((self.parent.nbr_row_table_reduction, 3), dtype=object)