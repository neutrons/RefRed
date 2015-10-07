from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QApplication
from RefRed.gui_handling.gui_utility import GuiUtility
from distutils.util import strtobool
import RefRed.colors
import numpy as np


class LiveReducedDataHandler(object):
    
    big_table_data = None
    colors = None
    row_index = 0
    
    def __init__(self, parent=None, row_index = 0):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data
        self.colors = RefRed.colors.COLOR_LIST
        self.row_index = row_index

    def populate_table(self):
        self.clear_stiching_table()
        self.fill_cell()
        if self.row_index == 0:
            self.activate_stitching_tab()        
        
    def activate_stitching_tab(self):
        self.parent.ui.plotTab.setCurrentIndex(1)
        
    def fill_cell(self):
        big_table_data = self.big_table_data
        row_index = self.row_index
        
        _lconfig = big_table_data[row_index, 2]
        if _lconfig is None:
            return
            
        #run number
        _run_number = self.parent.ui.reductionTable.item(row_index, 1).text()
        _run_item = QtGui.QTableWidgetItem(_run_number)
        _run_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.parent.ui.dataStitchingTable.setItem(row_index, 0, _run_item)
        
        #auto SF
        _brush = QtGui.QBrush()
        if strtobool(_lconfig.sf_auto_found_match):
            _brush.setColor(QtCore.Qt.green)
        else:
            _brush.setColor(QtCore.Qt.red)

        sf_auto = "%.4f" %_lconfig.sf_auto
        _auto_item = QtGui.QTableWidgetItem(sf_auto)
        _auto_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        _auto_item.setForeground(_brush)
        self.parent.ui.dataStitchingTable.setItem(row_index, 1, _auto_item)
        
        #manual SF
        _widget_manual = QtGui.QDoubleSpinBox()
        _widget_manual.setMinimum(0)
        _widget_manual.setValue(_lconfig.sf_manual)
        _widget_manual.setSingleStep(0.01)
        _widget_manual.valueChanged.connect(self.parent.data_stitching_table_manual_spin_box)
        self.parent.ui.dataStitchingTable.setCellWidget(row_index, 2, _widget_manual)
        
        #1 SF
        _item_1 = QtGui.QTableWidgetItem(str(1))
        _item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.parent.ui.dataStitchingTable.setItem(row_index, 3, _item_1)

    def clear_stiching_table(self):
        if self.row_index == 0:
            o_gui_utility = GuiUtility(parent = self.parent)
            o_gui_utility.clear_table(self.parent.ui.dataStitchingTable)
        
    def plot(self):
        
        self.parent.ui.data_stitching_plot.clear()
        self.parent.ui.data_stitching_plot.draw()
        
        big_table_data = self.big_table_data

        for index_row in range(self.row_index + 1):
            _lconfig = big_table_data[index_row, 2]
            if _lconfig is None:
                return        
        
            _q_axis = _lconfig.q_axis_for_display.copy()
            _y_axis = _lconfig.y_axis_for_display.copy()
            _e_axis = _lconfig.e_axis_for_display.copy()
            sf = self.generate_selected_sf(lconfig = _lconfig)
            
            _y_axis = np.array(_y_axis, dtype = np.float)
            _e_axis = np.array(_e_axis, dtype = np.float)
            
            _y_axis = _y_axis * sf
            _e_axis = _e_axis *sf

            o_produce_output = ProducedSelectedOutputScaled(parent = self.parent, 
                                                            q_axis = _q_axis,
                                                            y_axis = _y_axis,
                                                            e_axis = _e_axis)
            o_produce_output.calculate()
            y_axis = o_produce_output.output_y_axis
            e_axis = o_produce_output.output_e_axis

            self.parent.ui.data_stitching_plot.errorbar(_q_axis,
                                                        y_axis,
                                                        yerr = e_axis, 
                                                        color = self.get_current_color_plot(index_row))
            self.parent.ui.data_stitching_plot.set_yscale('log')
            self.parent.ui.data_stitching_plot.draw()
            QApplication.processEvents()
        
    def live_plot(self):
        
        if self.row_index == 0:
            self.parent.ui.data_stitching_plot.clear()
            self.parent.ui.data_stitching_plot.draw()
        
        big_table_data = self.big_table_data

        _lconfig = big_table_data[self.row_index, 2]
        if _lconfig is None:
            return        
        
        _q_axis = _lconfig.q_axis_for_display.copy()
        _y_axis = _lconfig.y_axis_for_display.copy()
        _e_axis = _lconfig.e_axis_for_display.copy()
        sf = self.generate_selected_sf(lconfig = _lconfig)
        
        _y_axis = np.array(_y_axis, dtype = np.float)
        _e_axis = np.array(_e_axis, dtype = np.float)
        
        _y_axis = _y_axis * sf
        _e_axis = _e_axis *sf

        o_produce_output = ProducedSelectedOutputScaled(parent = self.parent, 
                                                        q_axis = _q_axis,
                                                        y_axis = _y_axis,
                                                        e_axis = _e_axis)
        o_produce_output.calculate()
        y_axis = o_produce_output.output_y_axis
        e_axis = o_produce_output.output_e_axis

        self.parent.ui.data_stitching_plot.errorbar(_q_axis,
                                                    y_axis,
                                                    yerr = e_axis, 
                                                    color = self.get_current_color_plot(self.row_index))
        self.parent.ui.data_stitching_plot.set_yscale('log')
        self.parent.ui.data_stitching_plot.draw()
        QApplication.processEvents()

    def generate_selected_sf(self, lconfig=None):
        if self.parent.ui.autoSF.isChecked():
            return lconfig.sf_auto
        elif self.parent.ui.manualSF.isChecked():
            return lconfig.sf_manual
        else:
            return 1
            
    def get_current_color_plot(self, index_color):
        _color_list = self.colors
        _modulo_index = index_color % len(_color_list)
        return _color_list[_modulo_index]
        
class ProducedSelectedOutputScaled(object):

    parent = None
    axis_type = 'RvsQ'
    
    def __init__(self, parent=None, q_axis=None, y_axis=None, e_axis=None):
        self.parent = parent
        self.input_q_axis = q_axis
        self.input_y_axis = y_axis
        self.input_e_axis = e_axis
    
        self.init_output()
        
    def init_output(self):
        self.output_y_axis = None
        self.output_e_axis = None
        
    def calculate(self):
        self.get_selected_scale_type()
        
        input_q_axis = self.input_q_axis
        input_y_axis = self.input_y_axis
        input_e_axis = self.input_e_axis
        
        # R vs Q selected
        if self.axis_type == 'RvsQ':
            self.output_y_axis = input_y_axis
            self.output_e_axis = input_e_axis
            return
    
        # RQ4 vs Q selected
        if self.axis_type == 'RQ4vsQ':
            _q_axis_4 = input_q_axis ** 4
            self.output_y_axis = input_y_axis * _q_axis_4
            self.output_e_axis = input_e_axis * _q_axis_4
            return
    
        # Log(R) vs Q
        # make sure there is no <= 0 values of _y_axis
        input_y_axis[input_y_axis <=0] = np.nan
        self.output_y_axis = np.log(input_y_axis)
    #    _final_e_axis = np.log(_e_axis)
        self.output_e_axis = input_e_axis  ## FIXME
        
    def get_selected_scale_type(self):
        self.axis_type = 'RvsQ'
        if self.parent.ui.RQ4vsQ.isChecked():
            self.axis_type = 'RQ4vsQ'
        elif self.parent.ui.LogRvsQ.isChecked():
            self.axis_type = 'LogRvsQ'
        