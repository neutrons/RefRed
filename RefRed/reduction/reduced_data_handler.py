from PyQt4 import QtGui, QtCore
from RefRed.gui_handling.gui_utility import GuiUtility
from distutils.util import strtobool
import RefRed.colors
import numpy as np

class ReducedDataHandler(object):
    
    big_table_data = None
    colors = None
    
    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data
        self.colors = RefRed.colors.COLOR_LIST

    def populate_table(self):
        self.clear_stiching_table()
        self.fill_all_cells()
        self.activate_stitching_tab()        
        
    def activate_stitching_tab(self):
        self.parent.ui.plotTab.setCurrentIndex(1)
        
    def fill_all_cells(self):
        big_table_data = self.big_table_data
        for index_row, _lconfig in enumerate(big_table_data[:,2]):
            if _lconfig is None:
                return
            
            #run number
            _run_number = self.parent.ui.reductionTable.item(index_row, 1).text()
            _run_item = QtGui.QTableWidgetItem(_run_number)
            _run_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.parent.ui.dataStitchingTable.setItem(index_row, 0, _run_item)
            
            #auto SF
            #_brush = QtGui.QBrush()
            #if strtobool(_lconfig.sf_auto_found_match):
            #_brush.setColor(QtCore.Qt.green)
            #else:
            #_brush.setColor(QtCore.Qt.red)

            sf_auto = "%.4f" %_lconfig.sf_auto
            _auto_item = QtGui.QTableWidgetItem(sf_auto)
            _auto_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            #_auto_item.setForeground(_brush)
            self.parent.ui.dataStitchingTable.setItem(index_row, 1, _auto_item)
            
            #manual SF
            _widget_manual = QtGui.QDoubleSpinBox()
            _widget_manual.setMinimum(0)
            _widget_manual.setValue(_lconfig.sf_manual)
            _widget_manual.setSingleStep(0.01)
            _widget_manual.valueChanged.connect(self.parent.data_stitching_table_manual_spin_box)
            self.parent.ui.dataStitchingTable.setCellWidget(index_row, 2, _widget_manual)
            
            # FIXME
            #1 SF
            _item_1 = QtGui.QTableWidgetItem(str(1))
            _item_1.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.parent.ui.dataStitchingTable.setItem(index_row, 3, _item_1)

    def save_manual_sf(self):
        big_table_data = self.big_table_data
        for index_row, _lconfig in enumerate(big_table_data[:,2]):
            if _lconfig is None:
                break
            
            sf_manual_value = self.parent.ui.dataStitchingTable.cellWidget(index_row, 2).value()
            _lconfig.sf_manual = sf_manual_value
            big_table_data[index_row, 2] = _lconfig
        
        self.big_table_data = big_table_data
        self.parent.big_table_data = big_table_data

    def clear_stiching_table(self):
        o_gui_utility = GuiUtility(parent = self.parent)
        o_gui_utility.clear_table(self.parent.ui.dataStitchingTable)
        
    def plot(self):
        #try:
        self.plot_live_reduced_data()
#            self.plot_reduced_ascii_files()
        #except:
        #    pass
        
    def plot_live_reduced_data(self):
        
        self.parent.ui.data_stitching_plot.clear()
        self.parent.ui.data_stitching_plot.draw()
        
        big_table_data = self.big_table_data
        _data = big_table_data[0, 0]

        for index_row, _lconfig in enumerate(big_table_data[:,2]):
            if _lconfig is None:
                break       
        
            _q_axis = _lconfig.q_axis_for_display
            _y_axis = _lconfig.y_axis_for_display
            _e_axis = _lconfig.e_axis_for_display
            sf = self.generate_selected_sf(lconfig = _lconfig)
            
            _y_axis = np.array(_y_axis, dtype = np.float)
            _e_axis = np.array(_e_axis, dtype = np.float)
            
            _y_axis = _y_axis * sf
            _e_axis = _e_axis * sf

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
            
            #if _data.all_plot_axis.reduced_plot_stitching_tab_view_interval is None:
##                self.parent.ui.data_stitching_plot.canvas.ax.set_ylim(0, self.ylim)
                #self.parent.ui.data_stitching_plot.canvas.draw()
                #[xmin,xmax] = self.parent.ui.data_stitching_plot.canvas.ax.xaxis.get_view_interval()
                #[ymin,ymax] = self.parent.ui.data_stitching_plot.canvas.ax.yaxis.get_view_interval()
                #_data.all_plot_axis.reduced_plot_stitching_tab_view_interval = [xmin, xmax, ymin, ymax]
                #_data.all_plot_axis.reduced_plot_stitching_tab_view_interval = [xmin, xmax, ymin, ymax]
                #self.parent.ui.data_stitching_plot.toolbar.home_settings = [xmin, xmax, ymin, ymax]
            #else:
                #[xmin,xmax,ymin,ymax] = _data.all_plot_axis.reduced_plot_stitching_tab_view_interval
                #self.parent.ui.data_stitching_plot.canvas.ax.set_xlim([xmin,xmax])
                #self.parent.ui.data_stitching_plot.canvas.ax.set_ylim([ymin,ymax])
                #self.parent.ui.data_stitching_plot.canvas.draw()
            
            self.parent.ui.data_stitching_plot.set_yscale('log')
            self.parent.ui.data_stitching_plot.draw()
            
        o_gui_utility = GuiUtility(parent = self.parent)
        yaxis_type = o_gui_utility.get_reduced_yaxis_type()
        if yaxis_type == 'RvsQ':
            if _data.all_plot_axis.reduced_plot_RQuserView is None:
                self.parent.ui.data_stitching_plot.canvas.draw()
                [xmin,xmax] = self.parent.ui.data_stitching_plot.canvas.ax.xaxis.get_view_interval()
                [ymin,ymax] = self.parent.ui.data_stitching_plot.canvas.ax.yaxis.get_view_interval()
                _data.all_plot_axis.reduced_plot_RQuserView = [xmin, xmax, ymin, ymax]
                _data.all_plot_axis.reduced_plot_RQautoView = [xmin, xmax, ymin, ymax]
            else:
                [xmin, xmax, ymin, ymax] = _data.all_plot_axis.reduced_plot_RQuserView
                self.parent.ui.data_stitching_plot.canvas.ax.set_xlim([xmin,xmax])
                self.parent.ui.data_stitching_plot.canvas.ax.set_ylim([ymin,ymax])
                self.parent.ui.data_stitching_plot.canvas.draw()
        else:            
            if _data.all_plot_axis.reduced_plot_RQ4QuserView is None:
                self.parent.ui.data_stitching_plot.canvas.draw()
                [xmin,xmax] = self.parent.ui.data_stitching_plot.canvas.ax.xaxis.get_view_interval()
                [ymin,ymax] = self.parent.ui.data_stitching_plot.canvas.ax.yaxis.get_view_interval()
                _data.all_plot_axis.reduced_plot_RQ4QuserView = [xmin, xmax, ymin, ymax]
                _data.all_plot_axis.reduced_plot_RQ4QautoView = [xmin, xmax, ymin, ymax]
            else:
                [xmin, xmax, ymin, ymax] = _data.all_plot_axis.reduced_plot_RQ4QuserView
                self.parent.ui.data_stitching_plot.canvas.ax.set_xlim([xmin,xmax])
                self.parent.ui.data_stitching_plot.canvas.ax.set_ylim([ymin,ymax])
                self.parent.ui.data_stitching_plot.canvas.draw()

        big_table_data[0, 0] = _data
        self.parent.big_table_data = big_table_data

    def plot_reduced_ascii_files(self):
        big_table_data = self.parent.big_table_data
        data = big_table_data[0,0]
        if data is None:
            o_user_configuration = self.parent.o_user_configuration
            _isylog = o_user_configuration.is_reduced_plot_stitching_tab_ylog
            _isxlog = o_user_configuration.is_reduced_plot_stitching_tab_xlog
        else:
            _isylog = data.all_plot_axis.is_reduced_plot_stitching_tab_ylog
            _isxlog = data.all_plot_axis.is_reduced_plot_stitching_tab_xlog
        
        if self.parent.o_stitching_ascii_widget is None:
            return
        
        self.parent.o_stitching_ascii_widget.update_display(isxlog = _isxlog,
                                                            isylog = _isylog,
                                                            display_live_reduced_flag = False)
            
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
        o_gui_utility = GuiUtility(parent = self.parent)
        self.axis_type = o_gui_utility.get_reduced_yaxis_type()
        
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
        
        