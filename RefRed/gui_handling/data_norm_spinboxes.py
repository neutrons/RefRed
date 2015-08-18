from RefRed.plot.display_plots import DisplayPlots

class DataPeakSpinbox(object):
    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent
        
        big_table_data = parent.big_table_data
        row = parent.current_table_reduction_row_selected
        
        if row == -1:
            return
        
        data = big_table_data[row,0]
        
        peak1 = self.parent.ui.dataPeakFromValue.value()
        peak2 = self.parent.ui.dataPeakToValue.value()
        
        if (peak1 > peak2):
            peak_min = peak2
            peak_max = peak1
        else:
            peak_min = peak1
            peak_max = peak2
        
        data.peak = [str(peak_min), str(peak_max)]
        big_table_data[row, 0] = data
        self.parent.big_table_data = big_table_data
        
        #self.parent.ui.dataPeakFromValue.setValue(peak_min)
        #self.parent.ui.dataPeakToValue.setValue(peak_max)
        
        DisplayPlots(parent = self.parent,
                     row = row,
                     is_data = True,
                     plot_yt = True,
                     plot_yi = True,
                     plot_it = False,
                     plot_ix = False,
                     refresh_reduction_table = False)