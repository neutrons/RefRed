class DisplayReductionTable(object):
    
    parent = None
    row = 0
    is_data_displayed = True
    
    def __init__(self, parent=None, row=0, is_data_displayed=True):
        self.parent = parent
        self.row = row
        self.is_data_displayed = is_data_displayed
        
        
        