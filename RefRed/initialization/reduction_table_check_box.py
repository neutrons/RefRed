import numpy as np
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

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
        if row_selected == self.prev_row_selected:
            return
        
        self.row_selected = row_selected
        self.parent = parent
        _reduction_table_check_box_state = parent.reduction_table_check_box_state

        self.size_check_box_state_table = len(_reduction_table_check_box_state)
        old_check_box_state = _reduction_table_check_box_state[row_selected]
        _reduction_table_check_box_state = np.zeros((self.size_check_box_state_table), dtype=bool)
        
        _reduction_table_check_box_state[row_selected] = not old_check_box_state
        self._reduction_table_check_box_state = _reduction_table_check_box_state
        
        self.update_state_of_all_checkboxes()
        parent.reduction_table_check_box_state = _reduction_table_check_box_state
        
        parent.prev_table_reduction_row_selected = row_selected
        
        
    def update_state_of_all_checkboxes(self):
        for row in range(self.size_check_box_state_table):
            _state = self._reduction_table_check_box_state[row]
            _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
            _widget.setChecked(_state)
            
    def change_state_of_given_checkbox(self, row):
        _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
        _current_state = _widget.checkState()
        if _current_state == Qt.Unchecked():
            _widget.setChecked(True)
        else:
            _widget_setChecked(False)
