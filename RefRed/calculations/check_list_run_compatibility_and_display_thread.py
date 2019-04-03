import RefRed.colors
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication

from RefRed.reduction_table_handling.check_list_run_compatibility import CheckListRunCompatibility
from RefRed.calculations.add_list_nexus import AddListNexus
from RefRed.lconfigdataset import LConfigDataset
from RefRed.calculations.lr_data import LRData
from RefRed.plot.display_plots import DisplayPlots
from RefRed.calculations.update_reduction_table_metadata import UpdateReductionTableMetadata


class CheckListRunCompatibilityAndDisplayThread(QtCore.QThread):
    
    runs_are_compatible = False
    wks = None
    lrdata = None
    
    def setup(self, parent=None,
              list_run=None,
              list_nexus=None,
              row=-1,
              is_working_with_data_column=True,
              is_display_requested=False):
 
        self.parent = parent
        self.list_run = list_run
        self.list_nexus = list_nexus
        self.row = row
        self.col = 1 if is_working_with_data_column else 2
        self.is_working_with_data_column = is_working_with_data_column
        self.is_display_requested = is_display_requested
        self.runs_are_compatible = False
        self.lrdata = None
        
    def run(self):
        runs_are_compatible = False
        wks = []
    
        if (len(self.list_run) > 1):
            o_check_runs = CheckListRunCompatibility(list_nexus = self.list_nexus,
                                                     list_run = self.list_run)
            runs_are_compatible = o_check_runs.runs_compatible
            if runs_are_compatible:
                _color = QtGui.QColor(RefRed.colors.VALUE_OK)
            else:
                _color = QtGui.QColor(RefRed.colors.VALUE_BAD)
        else:
            _color = QtGui.QColor(RefRed.colors.VALUE_OK)
        
        self.parent.ui.reductionTable.item(self.row, 
                                           self.col).setForeground(_color)
        
        #if runs_are_compatible:
        o_add_list_nexus = AddListNexus(list_nexus = self.list_nexus,
                                        list_run = self.list_run,
                                        metadata_only = False,
                                        check_nexus_compatibility = False)
        wks = o_add_list_nexus.wks

        self.wks = wks
        self.runs_are_compatible = runs_are_compatible
        self.update_lconfigdataset()
        
#        if runs_are_compatible:
        self.loading_lr_data()
        self.updating_reductionTable_metadata()
        if self.is_display_requested:
            self.display_plots()

        self.parent.file_loaded_signal.emit()
        QApplication.processEvents()
            
    def updating_reductionTable_metadata(self):
        is_working_with_data_column = self.is_working_with_data_column
        if is_working_with_data_column is False:
            return

        row = self.row
        lrdata = self.lrdata 
        UpdateReductionTableMetadata(parent = self.parent, 
                                     lrdata = lrdata,
                                     row = row)

    def update_lconfigdataset(self):
        runs_are_compatible = self.runs_are_compatible
        big_table_data = self.parent.big_table_data
        _lconfig = big_table_data[self.row, 2]
        if _lconfig is None:
            _lconfig = LConfigDataset()
        
        if self.is_working_with_data_column:
            _lconfig.data_full_file_anme = self.list_nexus
            _lconfig.data_sets = self.list_run
            _lconfig.data_wks = self.wks
            _lconfig.data_runs_compatible = runs_are_compatible
        else:
            _lconfig.norm_full_file_anme = self.list_nexus
            _lconfig.norm_sets = self.list_run
            _lconfig.norm_wks = self.wks
            _lconfig.norm_runs_compatible = runs_are_compatible
            
        big_table_data[self.row, 2] = _lconfig
        self.parent.big_table_data = big_table_data

    def loading_lr_data(self):
        wks = self.wks
        lrdata = LRData(wks, parent = self.parent)
        self.lrdata = lrdata
        big_table_data = self.parent.big_table_data
        col_index = 0 if self.is_working_with_data_column else 1
        big_table_data[self.row, col_index] = lrdata
        self.parent.big_table_data = big_table_data
        
    def display_plots(self):
        DisplayPlots(parent = self.parent,
                     row = self.row,
                     is_data = self.is_working_with_data_column)