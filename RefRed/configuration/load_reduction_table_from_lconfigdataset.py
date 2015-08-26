from RefRed.calculations.add_list_nexus import AddListNexus
from RefRed.calculations.lr_data import LRData
from RefRed.calculations.update_reduction_table_metadata import UpdateReductionTableMetadata
from PyQt4 import QtGui


class LoadReductionTableFromLConfigDataSet(object):
    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent
        
        big_table_data = self.parent.big_table_data
        
        for index_row, lconfig in enumerate(big_table_data[:,2]):
            if lconfig is None:
                return
            
            list_data_nexus = lconfig.data_full_file_name
            list_data_run = lconfig.data_sets
            _add_data_nexus = AddListNexus(list_nexus = list_data_nexus,
                                     list_run = list_data_run,
                                     metadata_only = False,
                                     check_nexus_compatibility = False,
                                     prefix = 'data')
            data_lrdata = LRData(_add_data_nexus.wks)
            self.update_lrdata(lrdata = data_lrdata, 
                               lconfig = lconfig, 
                               type = 'data',
                               row = index_row)

            list_norm_nexus = lconfig.norm_full_file_name
            list_norm_run = lconfig.norm_sets
            _add_norm_nexus = AddListNexus(list_nexus = list_norm_nexus,
                                     list_run = list_norm_run,
                                     metadata_only = False,
                                     check_nexus_compatibility = False,
                                     prefix = 'norm')
            norm_lrdata = LRData(_add_norm_nexus.wks)
            self.update_lrdata(lrdata = norm_lrdata, 
                               lconfig = lconfig, 
                               type = 'norm',
                               row = index_row)
            
    def update_lrdata(self, lrdata=None, lconfig=None, type='data', row=0):
        big_table_data = self.parent.big_table_data
        
        if type == 'data':
            peak1 = int(lconfig.data_peak[0])
            peak2 = int(lconfig.data_peak[1])
            back1 = int(lconfig.data_back[0])
            back2 = int(lconfig.data_back[1])
            back_flag = lconfig.data_back_flag
            low_res1 = int(lconfig.data_low_res[0])
            low_res2 = int(lconfig.data_low_res[1])
            low_res_flag = lconfig.data_low_res_flag
            
        else:
            peak1 = int(lconfig.norm_peak[0])
            peak2 = int(lconfig.norm_peak[1])
            back1 = int(lconfig.norm_back[0])
            back2 = int(lconfig.norm_back[1])
            back_flag = lconfig.norm_back_flag
            low_res1 = int(lconfig.norm_low_res[0])
            low_res2 = int(lconfig.norm_low_res[1])
            low_res_flag = lconfig.norm_low_res_flag
            
        tof_auto_flag = lconfig.tof_auto_flag
        tof_range = lconfig.tof_range
        
        # using lconfig values
        lrdata.peak = [peak1, peak2]
        lrdata.back = [back1, back2]
        lrdata.back_flag = back_flag
        lrdata.low_res = [low_res1, low_res2]
        lrdata.low_res_flag = low_res_flag
        lrdata.tof_range = tof_range
        lrdata.tof_auto_flag = tof_auto_flag
        
        index_col = 0 if type == 'data' else 1
        big_table_data[row, index_col] = lrdata
        self.parent.big_table_data = big_table_data
        
        if type == 'data':
            UpdateReductionTableMetadata(parent = self.parent,
                                         lrdata = lrdata, 
                                         row = row)
            QtGui.QApplication.processEvents()                                             
        
        
        
        