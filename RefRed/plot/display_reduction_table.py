from RefRed.plot.clear_plots import ClearPlots
from RefRed.calculations.add_list_nexus import AddListNexus

class DisplayReductionTable(object):
    
    parent = None
    row = 0
    is_data_displayed = True # data or norm

    list_nexus = None
    list_run = None
    
    wks = None
    
    def __init__(self, parent=None, row=0, is_data_displayed=True):
        self.parent = parent
        self.row = row
        self.is_data_displayed = is_data_displayed
        
        big_table_data = self.parent.big_table_data
        if is_data_displayed: #data
            col_index = 0
        else: #norm
            col_index = 1
        _data = big_table_data[row, col_index]
        
        if _data is None:
            self.retrieve_list_nexus_run()
            if (self.list_nexus is None) or (self.list_run is None):
                return
            
            loader = AddListNexus(list_nexus = self.list_nexus, 
                                   list_run = self.list_run, 
                                   metadata_only = False,
                                   check_nexus_compatibility = False)
            self.wks = loader.wks
            big_table_data[row, col_index] = self.wks
            self.parent.big_table_data = big_table_data
        else:
            print("retrieve data")
        
        print("display data")
        
    def retrieve_list_nexus_run(self):
        print('in retrieve list nexus')
        parent = self.parent
        big_table_data = parent.big_table_data
        _lconfig = big_table_data[self.row, 2]
        if _lconfig is None:
            return
        
        if self.is_data_displayed:
            self.list_nexus = _lconfig.data_full_file_name
            self.list_run = _lconfig.data_sets
        else:
            self.list_nexus = _lconfig.norm_full_file_name
            self.list_run = _lconfig.norm_sets
        
            
        
        