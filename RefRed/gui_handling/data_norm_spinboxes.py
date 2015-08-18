from RefRed.plot.display_plots import DisplayPlots

class DataSpinbox(object):
    
    parent = None
    
    def __init__(self, parent=None, is_peak=True, value_min=-1, value_max=-1):
        self.parent = parent
        big_table_data = parent.big_table_data
        row = parent.current_table_reduction_row_selected
        
        if row == -1:
            return
        
        data = big_table_data[row,0]
        
        if is_peak:
            val1 = self.parent.ui.dataPeakFromValue.value()
            val2 = self.parent.ui.dataPeakToValue.value()
        else:
            val1 = self.parent.ui.dataBackFromValue.value()
            val2 = self.parent.ui.dataBackToValue.value()

        if (val1 > val2):
            val_min = val2
            val_max = val1
        else:
            val_min = val1
            val_max = val2
        
        if is_peak:
            data.peak = [str(val_min), str(val_max)]
        else:
            data.back = [str(val_min), str(val_max)]
            
        big_table_data[row, 0] = data
        self.parent.big_table_data = big_table_data
        
        DisplayPlots(parent = self.parent,
                     row = row,
                     is_data = True,
                     plot_yt = True,
                     plot_yi = True,
                     plot_it = False,
                     plot_ix = False,
                     refresh_reduction_table = False)
        

class DataPeakSpinbox(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        peak1 = self.parent.ui.dataPeakFromValue.value()
        peak2 = self.parent.ui.dataPeakToValue.value()

        DataSpinbox(parent = parent,
                    is_peak = True,
                    value_min = peak1,
                    value_max = peak2)
       
class DataBackSpinbox(object):
    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent
        back1 = self.parent.ui.dataBackFromValue.value()
        back2 = self.parent.ui.dataBackToValue.value()
        
        DataSpinbox(parent = parent,
                    is_peak = False,
                    value_min = back1,
                    value_max = back2)
