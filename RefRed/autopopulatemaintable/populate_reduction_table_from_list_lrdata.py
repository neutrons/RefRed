import numpy as np

class PopulateReductionTableFromListLRData(object):
    
    def __init__(self, parent=None,
                 list_lrdata = None,
                 list_wks = None,
                 list_run = None,
                 is_data = True):
        
        self.parent = parent
        self.list_run = list_run
        self.list_lrdata = list_lrdata
        self.list_wks = list_wks
        self.is_data = is_data

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