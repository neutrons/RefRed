from PyQt4 import QtGui

from RefRed.calculations.run_sequence_breaker import RunSequenceBreaker
from RefRed.reduction_table_handling.check_list_run_compatibility import CheckListRunCompatibility
from RefRed.plot.display_reduction_table import DisplayReductionTable
import RefRed.colors 
from RefRed.lconfigdataset import LConfigDataset

class UpdateReductionTable(object):
    
    raw_runs = None
    
    def __init__(self, parent=None, runs=None, row=0, col=1, clear_cell=False):
        self.parent= parent
        self.row = row
        self.col = col
        
        if clear_cell:
            self.clear_cell()
            return
        
        self.raw_runs = str(runs)
        run_breaker = RunSequenceBreaker(run_sequence=self.raw_runs)
        _list_run = run_breaker.final_list
        nxs_loader = CheckListRunCompatibility(list_run=_list_run)
        
        self.update_lconfigdataset(nxs_loader)

        if nxs_loader.runs_compatible:
            _color = QtGui.QColor(RefRed.colors.VALUE_OK)
        else:
            _color = QtGui.QColor(RefRed.colors.VALUE_BAD)
        self.parent.ui.reductionTable.item(row, 8).setBackground(_color)
    
        if self.display_of_this_row_checked():
            is_data_displayed = True if (col == 1) else False
            DisplayReductionTable(parent=self.parent, 
                                  row=self.row,
                                  is_data_displayed=_is_data_displayed)
    
    def update_lconfigdataset(self, nxs_loaded):
        list_nexus_found = nxs_loaded.list_nexus_found
        list_run_found = nxs_loaded.list_run_found
        
        _row = self.row
        big_table_data = self.parent.big_table_data
        
        if big_table_data[_row, 2] is None:
            _lconfig = LConfigDataset()
        else:
            _lconfig = big_table_data[_row, 2]
            
        if self.col == 1: #data
            _lconfig.data_full_file_name = list_nexus_found
            _lconfig_data_sets = list_run_found
        else: #norm
            _lconfig.norm_full_file_name = list_nexus_found
            _lconfig.norm_sets = list_run_found
            
        big_table_data[_row, 2] = _lconfig
        self.parent.big_table_data = big_table_data

    def clear_cell(self):
        print('in clear cell')
        
    def display_of_this_row_checked(self):
        _button_status = self.parent.ui.reductionTable.cellWidget(self.row, 0).checkState()
        if _button_status == 2:
            return True
        return False
    