class SFCalculatorTableHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def full_clear(self):
        self.__clear_variables()
        self.__clear_sf_calculator_table()
        self.__clear_plots()
        
    def __clear_variables(self):
        self.parent.data_list = []
        self.parent.big_table_nxdata = []
        self.parent.loaded_list_of_runs = []
        self.parent.list_nxsdata_sorted = []
        
    def __clear_sf_calculator_table(self):
        parent = self.parent
        nbr_row = parent.tableWidget.rowCount()
        for i in range(nbr_row):
            parent.tableWidget.removeRow(0)
            
    def __clear_plots(self):
        parent = self.parent

        parent.yt_plot.clear()
        parent.yt_plot.draw()
        
        parent.yi_plot.clear()
        parent.yi_plot.draw()
        
        