from RefRed.gui_handling.gui_utility import GuiUtility


class UpdatePlotWidgetStatus(object):
    '''
    This class will check if the plot widgets can be enabled according to
    status of the main table and tab selected
    '''    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent

    def disable_all(self):
        self.data_tab_widgets(status = False)
        self.norm_tab_widgets(status = False)
        
    def disable_data(self):
        self.data_tab_widgets(status = False)

    def enable_data(self):
        self.data_tab_widgets(status = True)
        
    def disable_norm(self):
        self.norm_tab_widgets(status = False)

    def enable_norm(self):
        self.norm_tab_widgets(status = True)
        
    def disable_reduced(self):
        parent = self.parent
        
    def data_tab_widgets(self, status=False):
        parent = self.parent
        parent.ui.dataNormTabWidget.setEnabled(status)
        parent.ui.data_yt_plot.setEnabled(status)
        parent.ui.dataNameOfFile.setEnabled(status)
        parent.ui.data_yi_plot.setEnabled(status)
        parent.ui.data_it_plot.setEnabled(status)
        parent.ui.data_ix_plot.setEnabled(status)
        parent.ui.dataLowResFlag.setEnabled(status)
        parent.ui.dataLowResFromLabel.setEnabled(status)
        parent.ui.dataLowResFromValue.setEnabled(status)
        parent.ui.dataLowResToLabel.setEnabled(status)
        parent.ui.dataLowResToValue.setEnabled(status)
        parent.ui.dataBackToValue.setEnabled(status)
        parent.ui.dataBackFromValue.setEnabled(status)
        parent.ui.dataPeakToValue.setEnabled(status)
        parent.ui.dataPeakFromValue.setEnabled(status)
        parent.ui.dataBackgroundFlag.setEnabled(status)

        
        self.parent.ui.dataTOFmanualLabel.setEnabled(status)
        self.parent.ui.dataTOFautoMode.setEnabled(status)
        self.parent.ui.dataTOFmanualMode.setEnabled(status)
        
    def norm_tab_widgets(self, status=False):
        parent = self.parent
        parent.ui.dataNormTabWidget.setEnabled(status)
        parent.ui.norm_yt_plot.setEnabled(status)
        parent.ui.normNameOfFile.setEnabled(status)
        parent.ui.norm_yi_plot.setEnabled(status)
        parent.ui.norm_it_plot.setEnabled(status)
        parent.ui.norm_ix_plot.setEnabled(status)
        parent.ui.normLowResFlag.setEnabled(status)
        parent.ui.normLowResFromLabel.setEnabled(status)
        parent.ui.normLowResFromValue.setEnabled(status)
        parent.ui.normLowResToLabel.setEnabled(status)
        parent.ui.normLowResToValue.setEnabled(status)
        parent.ui.normBackToValue.setEnabled(status)
        parent.ui.normBackFromValue.setEnabled(status)
        parent.ui.normPeakToValue.setEnabled(status)
        parent.ui.normPeakFromValue.setEnabled(status)
        parent.ui.normBackgroundFlag.setEnabled(status)
            