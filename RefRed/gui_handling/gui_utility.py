class GuiUtility(object):
    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def data_norm_tab_widget_row_to_display(self):
        return self.parent.current_table_reduction_row_selected

        
        