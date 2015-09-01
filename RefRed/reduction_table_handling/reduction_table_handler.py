import numpy as np
from RefRed.plot.clear_plots import ClearPlots
from RefRed.gui_handling.gui_utility import GuiUtility


class ReductionTableHandler(object):

    from_row = -1
    to_row = -1
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def full_clear(self):
        self.__clear_big_table_data()
        self.__clear_reduction_table()
        self.__clear_metadata()
        self.__clear_plots()
        
    def clear_rows_selected(self):
        self.__get_range_row_selected()
        if self.__is_row_displayed_in_range_selected:
            self.__clear_metadata()
            self.__clear_plots()

    def __is_row_displayed_in_range_selected(self):
        _range_selected = range(self.from_row, self.to_row + 1)
        o_gui_utility = GuiUtility(parent = self.parent)
        _row_displayed = o_gui_utility.get_current_table_reduction_check_box_checked()
        if _row_displayed == -1:
            return False
        if _row_displayed in _range_selected:
            return True
        return False
        
    def __get_range_row_selected(self):
        selected_range = self.parent.ui.reductionTable.selectedRanges()
        self.to_row = selected_range[0].bottomRow()
        self.from_row = selected_range[0].topRow()

    def __clear_metadata(self):
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
    
    def __clear_plots(self):
        ClearPlots(self.parent, 
                   is_data = True,
                   is_norm = True,
                   plot_yt = True,
                   plot_yi = True,
                   plot_it = True,
                   plot_ix = True)

    def __clear_reduction_table(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")
        
    def __clear_big_table_data(self):
        self.parent.big_table_data = np.empty((self.parent.nbr_row_table_reduction,
                                               3), dtype = object)
        