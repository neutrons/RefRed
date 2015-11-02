from RefRed.reduction_table_handling.update_reduction_table import UpdateReductionTable

class UpdateDataNormTab(object):
    
    parent = None
    tab_index = 0
    
    def __init__(self, parent=None, tab_index=0):
        self.parent = parent
        self.tab_index = tab_index
        
        if tab_index == 0:
            col = 1
        else:
            col = 2
            
        row = parent.prev_table_reduction_row_selected
        item = parent.ui.reductionTable.item(row, col)
        if item is None:
            return
        if (item.text() == ''):
            UpdateReductionTable(parent = parent, 
                                 row = row, 
                                 col = col, 
                                 clear_cell = True)
        else:
            UpdateReductionTable(parent = parent, 
                                 runs = item.text(), 
                                 row = row, 
                                 col = col)


        
        
        