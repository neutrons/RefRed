from PyQt4.QtCore import Qt

class GuiUtility(object):
    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def data_norm_tab_widget_row_to_display(self):
        return self.parent.current_table_reduction_row_selected
    
    def data_norm_tab_widget_tab_selected(self):
        return self.parent.ui.dataNormTabWidget.currentIndex()

    def get_current_table_reduction_check_box_checked(self):
        nbr_row_table_reduction = self.parent.nbr_row_table_reduction
        for row in range(nbr_row_table_reduction):
            _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
            _state = _widget.checkState()
            if _state == Qt.Checked:
                return row
        return -1
        
        