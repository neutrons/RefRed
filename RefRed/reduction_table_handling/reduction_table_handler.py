import numpy as np
from RefRed.plot.clear_plots import ClearPlots


class ReductionTableHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def full_clear(self):
        self.clear_big_table_data()
        self.clear_reduction_table()
        self.clear_metadata()
        self.clear_plots()
        
    def clear_metadata(self):
        parent = self.parent
        parent.ui.metadataProtonChargeValue.setText('N/A')
        parent.ui.metadataProtonChargeUnits.setText('units')
        parent.ui.metadataLambdaRequestedValue.setText('N/A')
        parent.ui.metadataLambdaRequestedUnits.setText('units')
        parent.ui.metadatathiValue.setText('N/A')
        parent.ui.metadatathiUnits.setText('units')
        parent.ui.metadatatthdValue.setText('N/A')
        parent.ui.metadatatthdUnits.setText('units')
        parent.ui.metadataS1WValue.setText('N/A')
        parent.ui.metadataS1HValue.setText('N/A')
        parent.ui.metadataS2WValue.setText('N/A')
        parent.ui.metadataS2HValue.setText('N/A')
    
    def clear_plots(self):
        ClearPlots(self.parent, 
                   is_data = True,
                   is_norm = True,
                   plot_yt = True,
                   plot_yi = True,
                   plot_it = True,
                   plot_ix = True)

    def clear_reduction_table(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")
        
    def clear_big_table_data(self):
        self.parent.big_table_data = np.empty((self.parent.nbr_row_table_reduction,
                                               3), dtype = object)
        