from RefRed.plot.clear_plots import ClearPlots
from RefRed.plot.display_plots import DisplayPlots
from RefRed.calculations.add_list_nexus import AddListNexus
from RefRed.calculations.lr_data import LRData


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
        lconfig = big_table_data[row, 2]
        if lconfig is None:
            return

        if is_data_displayed:
            runs_compatible = lconfig.data_runs_compatible
        else:
            runs_compatible = lconfig.norm_runs_compatible
        if runs_compatible is False:
            ClearPlots(self.parent,
                       is_data = is_data_displayed,
                       is_norm = not is_data_displayed,
                       all_plots = True)
            return

        big_table_data_col_index = 0 if is_data_displayed else 1

        # check that the data or norm lr_data object is there (data already loaded)
        lr_data = big_table_data[row, big_table_data_col_index]
        if lr_data is None:
            # we need to load the data first
            if is_data_displayed:
                list_nexus = lconfig.data_full_file_name
                list_run = lconfig.data_sets
            else:
                list_nexus = lconfig.norm_full_file_name
                list_run = lconfig.norm_sets

            if list_nexus == ['']:
                return

            nexus_loader = AddListNexus(list_nexus = list_nexus,
                                        list_run = list_run,
                                        metadata_only = False,
                                        check_nexus_compatibility = False)
            wks = nexus_loader.wks
            lrdata = LRData(wks)
            col_index = 0 if is_data_displayed else 1
            big_table_data[row, col_index] = lrdata
            self.big_table_data = big_table_data
            
        DisplayPlots(parent = self.parent, 
                     row = self.row,
                     is_data = self.is_data_displayed)
            
        
        
        
        return



        lconfig = big_table_data[row, 2]
        if is_data_displayed: #data
            _data = lconfig.data_wks
        else: #norm
            _data = lconfig.norm_wks
        
        if _data is None:
            self.retrieve_list_nexus_run()
            if (self.list_nexus is None) or (self.list_run is None):
                return
            
            loader = AddListNexus(list_nexus = self.list_nexus, 
                                   list_run = self.list_run, 
                                   metadata_only = False,
                                   check_nexus_compatibility = False)
            self.wks = loader.wks
            if is_data_displayed:
                lconfig.data_wks = self.wks
            else:
                lconfig.norm_wks = self.wks
            big_table_data[row, 2] = lconfig
            self.parent.big_table_data = big_table_data
        else:
            self.wks = _data
        
        
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
        
            
        
        