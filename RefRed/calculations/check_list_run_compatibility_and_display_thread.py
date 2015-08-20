import RefRed.colors
from PyQt4 import QtCore, QtGui

from RefRed.reduction_table_handling.check_list_run_compatibility import CheckListRunCompatibility

class CheckListRunCompatibilityAndDisplayThread(QtCore.QThread):
    
    def setup(self, parent=None,
                 list_run=None,
                 list_nexus=None,
                 row=-1,
                 col=-1,
                 is_working_with_data_column=True,
                 is_display_requested=False):
        self.parent = parent
        self.list_run = list_run
        self.list_nexus = list_nexus
        self.row = row
        self.col = col
        self.is_working_with_data_column = is_working_with_data_column
        self.is_display_requested = is_display_requested
        
    def run(self):
        if len(self.list_run) > 1:
            o_check_runs = CheckListRunCompatibility(list_nexus = self.list_nexus,
                                                     list_run = self.list_run)
            if o_check_runs.runs_compatible:
                _color = QtGui.QColor(RefRed.colors.VALUE_OK)
            else:
                _color = QtGui.QColor(RefRed.colors.VALUE_BAD)
        else:
            _color = QtGui.QColor(RefRed.colors.VALUE_OK)
        
        self.parent.ui.reductionTable.item(self.row, 
                                           self.col).setForeground(_color)
            