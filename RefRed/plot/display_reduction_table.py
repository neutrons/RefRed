from RefRed.plot.clear_plots import ClearPlots

class DisplayReductionTable(object):
    
    parent = None
    row = 0
    is_data_displayed = True
    
    def __init__(self, parent=None, row=0, is_data_displayed=True):
        self.parent = parent
        self.row = row
        self.is_data_displayed = is_data_displayed
        
        big_table_data = self.parent.big_table_data
        if is_data_displayed:
            _data = big_table_data[row, 0]
        else:
            _data = big_table_data[row, 1]
        
        if _data is None:
            
            print("Load it")
        else:
            print("retrieve data")
        
        print("display data")
        

        
        