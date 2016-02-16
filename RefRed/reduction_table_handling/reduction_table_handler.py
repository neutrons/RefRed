from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import numpy as np
from RefRed.plot.clear_plots import ClearPlots
from RefRed.gui_handling.gui_utility import GuiUtility
import RefRed.colors
from RefRed.version import window_title


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
        self.__reset_default_config_file_name()
        
    def __reset_default_config_file_name(self):
        str_new_window_title = (u"%s%s" %(window_title, self.parent.default_loaded_file))
        self.parent.setWindowTitle(str_new_window_title)
        self.parent.ui.previewLive.setEnabled(False)
        
    def clear_rows_selected(self):
        self.__get_range_row_selected()
        if self.__is_row_displayed_in_range_selected():
            self.__clear_metadata()
            self.__clear_plots()
        self.__clear_rows_big_table_data()
        self.__clear_rows_reduction_table()
        self.__shifs_none_empty_rows_reduction_table()
        self.__to_do_if_table_empty()
        
    def __to_do_if_table_empty(self):
        """If the table is now empty, various reset algos"""
        _cell_value = str(self.parent.ui.reductionTable.item(0, 1).text())
        if _cell_value == '':
            self.__reset_default_config_file_name()

    def __clear_rows_reduction_table(self):
        _from_row = self.from_row
        _to_row = self.to_row
        _nbr_col = self.parent.ui.reductionTable.columnCount()
        for row_index in range(_from_row, _to_row + 1):
            for col_index in range(_nbr_col):
                if col_index == 0:
                    _widget = QtGui.QCheckBox()
                    _widget.setChecked(False)
                    _widget.setEnabled(True)
#                    signal_function = self.__get_checkbox_signal_function(row_index)
                    QtCore.QObject.connect(_widget, QtCore.SIGNAL("stateChanged(int)"), 
                                           lambda state=0, row=row_index: self.parent.reduction_table_visibility_changed_test(state, row))
#                                           eval(signal_function))
                    self.parent.ui.reductionTable.setCellWidget(row_index, col_index, _widget)
    
                elif (col_index == 1) or (col_index == 2):
                    _item = QtGui.QTableWidgetItem()
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                    #if (col_index == 1):
                        #_color = QtGui.QColor(RefRed.colors.DATA_TABLE_BACKGROUND)
                        #_item.setBackground(_color)
                    #else:
                        #_color = QtGui.QColor(RefRed.colors.NORM_TABLE_BACKGROUND)
                        #_item.setBackground(_color)
                    self.parent.ui.reductionTable.setItem(row_index, col_index, _item)
    
                else:
                    _item = QtGui.QTableWidgetItem()
                    _item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.parent.ui.reductionTable.setItem(row_index, col_index, _item)
              
    def __shifs_none_empty_rows_reduction_table(self):
        _nbr_row = self.parent.nbr_row_table_reduction
        _to_row = self.to_row
        if _to_row == (_nbr_row - 1):
            return
        
        _from_row = self.from_row
        _row_offset = 0
        _nbr_col = self.parent.ui.reductionTable.columnCount()
        for row_index in range(_to_row + 1, _nbr_row):
            _target_row_index = _from_row + _row_offset
            for col_index in range(_nbr_col):
                if col_index == 0:
                    _widget = self.parent.ui.reductionTable.cellWidget(_target_row_index, col_index)
                    _widget.setChecked(self.__is_row_selected_checked(row_index))
                else:
                    _cell_value = self.parent.ui.reductionTable.item(row_index, col_index).text()
                    self.parent.ui.reductionTable.item(_target_row_index, col_index).setText(_cell_value)
            _row_offset += 1
                    
    def __is_row_selected_checked(self, row_selected):
        _widget = self.parent.ui.reductionTable.cellWidget(row_selected, 0)
        current_state = _widget.checkState()
        if current_state == Qt.Unchecked:
            return False
        else:
            return True
            
    def __get_checkbox_signal_function(self, row_index):
        root_function_name = 'self.parent.reduction_table_visibility_changed_' + str(row_index)
        return root_function_name
        
    def __clear_rows_big_table_data(self):
        big_table_data = self.parent.big_table_data
        for row in range(self.from_row, self.to_row + 1):
            big_table_data = np.delete(big_table_data, (self.from_row), axis=0)
            big_table_data = np.append(big_table_data, [[None, None, None]], axis=0)
        self.parent.big_table_data = big_table_data

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
        