from PyQt4.QtCore import Qt
from PyQt4 import QtGui
import RefRed.version


class GuiUtility(object):
    
    parent = None
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def get_ipts(self, row=-1):
        big_table_data = self.parent.big_table_data
        _data0 = big_table_data[row, 0]
        if _data0 is None:
            return 'N/A'
        if row == -1:
            return 'N/A'
        return _data0.ipts

    def data_norm_tab_widget_row_to_display(self):
        return self.parent.current_table_reduction_row_selected

    #def data_norm_tab_widget_tab_selected(self):
        #return self.parent.ui.dataNormTabWidget.currentIndex()
    
    def get_current_table_reduction_row_selected(self):
        return int(self.parent.ui.reductionTable.currentRow())
    
    def get_current_table_reduction_column_selected(self):
        return int(self.parent.ui.reductionTable.currentColumn())

    def get_current_table_reduction_check_box_checked(self):
        nbr_row_table_reduction = self.parent.nbr_row_table_reduction
        for row in range(nbr_row_table_reduction):
            _widget = self.parent.ui.reductionTable.cellWidget(row, 0)
            _state = _widget.checkState()
            if _state == Qt.Checked:
                return row
        return -1
    
    def get_other_row_with_same_run_number_as_row(self, row=0, is_data=False):
        all_rows = [row]
        if is_data:
            return all_rows
        nbr_row = self.parent.ui.reductionTable.rowCount()
        ref_run_number = str(self.parent.ui.reductionTable.item(row, 2).text())
        for _row in range(nbr_row):
            if _row == row:
                continue
            _item = str(self.parent.ui.reductionTable.item(_row,2).text())
            if _item == ref_run_number:
                all_rows.append(_row)
        all_rows.sort()
        return all_rows
    
    def get_data_norm_tab_selected(self):
        return self.parent.ui.dataNormTabWidget.currentIndex()
    
    def is_data_tab_selected(self):
        if self.get_data_norm_tab_selected() == 0:
            return True
        return False
    
    def is_auto_tof_range_radio_button_selected(self):
        return self.parent.ui.dataTOFautoMode.isChecked()
    
    def set_auto_tof_range_radio_button(self, status = True):
        self.parent.ui.dataTOFautoMode.setChecked(status)
        self.parent.ui.dataTOFmanualMode.setChecked(not status)
        self.set_auto_tof_range_widgets(status = status)
    
    def set_auto_tof_range_widgets(self, status = True):    
        self.parent.ui.TOFmanualFromLabel.setEnabled(not status)
        self.parent.ui.TOFmanualFromValue.setEnabled(not status)
        self.parent.ui.TOFmanualFromUnitsValue.setEnabled(not status)
        self.parent.ui.TOFmanualToValue.setEnabled(not status)
        self.parent.ui.TOFmanualToLabel.setEnabled(not status)
        self.parent.ui.TOFmanualToUnitsValue.setEnabled(not status)
    
    def clear_table(self, table_ui):
        nbr_row = table_ui.rowCount()
        nbr_col = table_ui.columnCount()
        for _row in range(nbr_row):
            table_ui.removeRow(_row)
            table_ui.insertRow(_row)

    def clear_reductionTable(self):
        nbr_row = self.parent.ui.reductionTable.rowCount()
        nbr_col = self.parent.ui.reductionTable.columnCount()
        for _row in range(nbr_row):
            for _col in range(1, nbr_col):
                self.parent.ui.reductionTable.item(_row, _col).setText("")

    def reductionTable_nbr_row(self):
        big_table_data = self.parent.big_table_data
        for _index_row, _ldata in enumerate(big_table_data[:,0]):
            if _ldata is None:
                return _index_row
        return _index_row

    def new_config_file_loaded(self, config_file_name = None):
        self.parent.current_loaded_file = config_file_name
        dialog_title = RefRed.version.window_title + self.parent.current_loaded_file
        self.parent.setWindowTitle(dialog_title)

    def gui_has_been_modified(self):
        dialog_title = RefRed.version.window_title + self.parent.current_loaded_file
        new_dialog_title = dialog_title + '*'
        self.parent.setWindowTitle(new_dialog_title)

    def gui_not_modified(self):
        dialog_title = RefRed.version.window_title + self.parent.current_loaded_file
        new_dialog_title = dialog_title
        self.parent.setWindowTitle(new_dialog_title)



    #def data_peak_and_back_validation(self, with_plot_update = True):
        #self.data_peak_spinbox_validation(with_plot_update = with_plot_update)
        #self.data_back_spinbox_validation(with_plot_update = with_plot_update)
##        CheckErrorWidgets(self)
##	self.fileHasBeenModified()
    
    #def data_peak_spinbox_validation(self, with_plot_update = True):
        #'''
        #This function, reached when the user is done editing the
        #spinboxes (ENTER, leaving the spinbox) 
        #will make sure the min value is < max value    
        #'''

        #bigTableData = self.bigTableData
        ##[row,col] = self.getCurrentRowColumnSelected()
        #row = self._cur_row_selected
        #col = self._cur_column_selected
        #if col != 0:
            #col = 1
        #data = bigTableData[row,col]
        #data = data.active_data

        #peak1 = self.ui.dataPeakFromValue.value()
        #peak2 = self.ui.dataPeakToValue.value()

        #if (peak1 > peak2):
            #peak_min = peak2
            #peak_max = peak1
        #else:
            #peak_min = peak1
            #peak_max = peak2

        #data.peak = [str(peak_min),str(peak_max)]
        #self.active_data = data

        #self.ui.dataPeakFromValue.setValue(peak_min)
        #self.ui.dataPeakToValue.setValue(peak_max)

        ## refresh plots
        #if withPlotUpdate:
            #self.plot_overview_REFL(plot_ix=True, plot_yt=True, plot_yi=True)

        ## save new settings
        #self.save_new_settings()

        #CheckErrorWidgets(self)
        #self.fileHasBeenModified()
        #self.checkRunReductionButton()	

    ## data back spinboxes
    #def data_back_spinbox_validation(self, withPlotUpdate=True):
        #r = self._cur_row_selected
        #c = self._cur_column_selected
        #if c != 0:
            #c = 1
        #_data = self.bigTableData[r,c]
        #if _data is None:
            #return
        #data = _data.active_data

        #back1 = self.ui.dataBackFromValue.value()
        #back2 = self.ui.dataBackToValue.value()

        #if (back1 > back2):
            #back_min = back2
            #back_max = back1
        #else:
            #back_min = back1
            #back_max = back2

        #data.back = [str(back_min),str(back_max)]

        #_data.active_data = data
        #self.bigTableData[r,c] = _data

        #self.ui.dataBackFromValue.setValue(back_min)
        #self.ui.dataBackToValue.setValue(back_max)

        ## save new settings
        #self.save_new_settings()

        ## refresh plots
        #self.plot_overview_REFL(plot_ix=True, plot_yt=True, plot_yi=True)

        #CheckErrorWidgets(self)
        #self.fileHasBeenModified()
        #self.checkRunReductionButton()
    
    #def tofValidation( self, tof_auto_switch_status, tof1, tof2):
        #self.ui.dataTOFautoMode.setChecked(tof_auto_switch_status)
        #self.ui.dataTOFmanualMode.setChecked(not tof_auto_switch_status)
        #bigTableData = self.bigTableData
        #row = self._cur_row_selected
        #col = self._cur_column_selected
        #if col != 0:
            #col = 1
        #data = bigTableData[row, col]
        #_active_data =  data.active_data
        #tof1 = str(float(tof1)*1000)
        #tof2 = str(float(tof2)*1000)
        #if tof_auto_switch_status:
            #_active_data.tof_range_auto = [tof1, tof2]
        #else:
            #_active_data.tof_range = [tof1, tof2]
        #data.active_data = _active_data
        #bigTableData[row, col] = data
        #self.bigTableData = bigTableData
        #self.auto_tof_switch(tof_auto_switch_status)
        #self.fileHasBeenModified()
    