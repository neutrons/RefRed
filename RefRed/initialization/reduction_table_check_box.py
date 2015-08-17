import numpy as np
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from RefRed.plot.display_reduction_table import DisplayReductionTable

class ReductionTableCheckBox(object):

    row_selected = -1
    prev_row_selected = -1
    size_check_box_state_table = None
    parent = None
    _reduction_table_check_box_state = None
    
    def __init__(self, parent=None, row_selected=-1):
        if row_selected == -1:
            return
        if parent == None:
            return
        
        self.prev_row_selected = parent.prev_table_reduction_row_selected
        self.row_selected = row_selected
        self.parent = parent
        if row_selected == self.prev_row_selected:
            pass
        else:
            _reduction_table_check_box_state = parent.reduction_table_check_box_state
    
            self.size_check_box_state_table = len(_reduction_table_check_box_state)
            old_check_box_state = _reduction_table_check_box_state[row_selected]
            _reduction_table_check_box_state = np.zeros((self.size_check_box_state_table), dtype=bool)
            
            _reduction_table_check_box_state[row_selected] = not old_check_box_state
            self._reduction_table_check_box_state = _reduction_table_check_box_state
            
            self.update_state_of_all_checkboxes()
            parent.reduction_table_check_box_state = _reduction_table_check_box_state
            
            parent.prev_table_reduction_row_selected = row_selected
        
        self.launch_update_of_plot()
        
    def launch_update_of_plot(self):
        _row_selected = self.row_selected
        _is_data_selected = self.is_data_tab_selected()
        if self.is_row_selected_checked(_row_selected):
            DisplayReductionTable(parent=self.parent, 
                                  row=_row_selected, 
                                  is_data_displayed=_is_data_selected)
        else:
            print('clear plots')
        
    def is_data_tab_selected(self):
        if self.parent.ui.dataNormTabWidget.currentIndex() == 0:
            return True
        else:
            return False
        
    def is_row_selected_checked(self, row_selected):
        _widget = self.parent.ui.reductionTable.cellWidget(row_selected, 0)
        current_state = _widget.checkState()
        if current_state == Qt.Unchecked:
            return False
        else:
            return True
    
    def update_state_of_all_checkboxes(self):
        for row in range(self.size_check_box_state_table):
            _state = self._reduction_table_check_box_state[row]
            _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
            _widget.setChecked(_state)
            
    def change_state_of_given_checkbox(self, row):
        _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
        _current_state = _widget.checkState()
        if _current_state == Qt.Unchecked:
            _widget.setChecked(True)
        else:
            _widget_setChecked(False)
