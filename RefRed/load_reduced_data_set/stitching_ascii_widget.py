from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import numpy as np

from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader
from RefRed.gui_handling.gui_utility import GuiUtility
import RefRed.colors

class StitchingAsciiWidget(object):

    loaded_ascii_array = []
    tableUi = None
    stitchingPlot = None
    parent = None
    isylog = True
    isxlog = True
    yaxistype = 'RvsQ'
    row_of_this_file = 0

    def __init__(self, parent=None, loaded_ascii=None):

        self.parent = parent
        self.loaded_ascii_array.append(loaded_ascii)
        self.tableUi = parent.ui.reducedAsciiDataSetTable
        self.stitchingPlot = parent.ui.data_stitching_plot

    def add_data(self, newloaded_ascii):

        row_of_this_file = self.get_row_of_this_file(newloaded_ascii)
        if row_of_this_file == -1:
            #add row
            row_of_this_file = len(self.loaded_ascii_array)
            self.loaded_ascii_array.append(newloaded_ascii)
        else:
            # replace
            self.loaded_ascii_array[row_of_this_file] = newloaded_ascii
        self.row_of_this_file = row_of_this_file
        
    def remove_data(self, list_file_to_remove = None):
        if list_file_to_remove is None:
            return
        _loaded_ascii_array = self.loaded_ascii_array
        _new_loaded_ascii_array = []
        for _loaded_ascii in _loaded_ascii_array:
            _name = _loaded_ascii.short_ascii_file_name
            if _name in list_file_to_remove:
                continue
            _new_loaded_ascii_array.append(_loaded_ascii)
        
        self.loaded_ascii_array = _new_loaded_ascii_array
    
    def remove_all_data(self):
        self.loaded_ascii_array = []

    def get_row_of_this_file(self, loaded_ascii):

        newFilename = loaded_ascii.ascii_file_name

        nbrRow = len(self.loaded_ascii_array)
        for i in range(nbrRow):
            _tmpObject = self.loaded_ascii_array[i]
            _name = _tmpObject.ascii_file_name

            if _name == newFilename:
                return i
        return -1

    def update_status(self):

        nbrRow = len(self.loaded_ascii_Array)
        for i in range(nbrRow):

            _data_object = self.loaded_ascii_array[i]

            _item_state = self.parent.ui.reducedAsciiDataSetTable.cellWidget(i,1).checkState()
            if _item_state == 2:
                _data_object.isEnabled = True
            else:
                _data_object.isEnabled = False

            self.loaded_ascii_array[i] = _data_object

    def update_display(self, isylog=True, 
                       isxlog=True, 
                       force_row=-1, 
                       display_live_reduced_flag=True):

        if self.loaded_ascii_array == []:
            return
        
        self.isylog = isylog
        self.isxlog = isxlog
        self.yaxistype = self.get_selected_reduced_output()

        if display_live_reduced_flag:
            self.stitchingPlot.clear()
            self.stitchingPlot.draw()

        nbrRow = len(self.loaded_ascii_array)
        for i in range(nbrRow):

            _data_object = self.loaded_ascii_array[i]

            _item = QtGui.QTableWidgetItem(str(_data_object.short_ascii_file_name))
            self.tableUi.setItem(i,0,_item)

            _widget = self.tableUi.cellWidget(i, 1)
            if _data_object.is_live_reduction:
                _widget.setCheckState(Qt.Checked)
                _widget.setEnabled(False)
                _status = True
            elif (force_row == i):
                _widget.setCheckState(Qt.Checked)
                _status = True				
            else:
                _status = _widget.checkState()
                _widget.setEnabled(True)

            if _status:

                if _data_object.is_live_reduction and display_live_reduced_flag:
                    self.__display_live_data(_data_object)
                else:
                    _q_axis = _data_object.col1
                    _y_axis = _data_object.col2
                    _e_axis = _data_object.col3

                    [_y_axis_red, _e_axis_red] = self.format_data_from_ymode_selected(_q_axis, 
                                                                                      _y_axis,
                                                                                      _e_axis)

                    self.stitchingPlot.errorbar(_q_axis, _y_axis_red, yerr=_e_axis_red)
                    if isylog:
                        self.stitchingPlot.set_yscale('log')
                    else:
                        self.stitchingPlot.set_yscale('linear')

                    if isxlog:
                        self.stitchingPlot.set_xscale('log')
                    else:
                        self.stitchingPlot.set_xscale('linear')
                    self.stitchingPlot.draw()

    def __display_live_data(self, _data_object):
        '''
        plot last reduced data set
        '''

        #big_table_data = _data_object.big_table_data
        big_table_data = self.parent.big_table_data

        _colors = RefRed.colors.COLOR_LIST
        _colors.append(_colors)

        #_data0 = big_table_data[0,0]

        i = 0
        while (big_table_data[i,2] is not None):

            _data = big_table_data[i,2]
            _q_axis = _data.q_axis_for_display
            _y_axis = _data.y_axis_for_display
            _e_axis = _data.e_axis_for_display

            sf = _data.sf

            _y_axis = _y_axis / sf
            _e_axis = _e_axis / sf

            [y_axis_red, e_axis_red] = self.format_data_from_ymode_selected(_q_axis, 
                                                                            _y_axis,
                                                                            _e_axis)

            self.stitchingPlot.errorbar(_q_axis, y_axis_red, yerr=e_axis_red, color=_colors[i])
            if self.isylog:
                self.stitchingPlot.set_yscale('log')
            else:
                self.stitchingPlot.set_yscale('linear')
            if self.isxlog:
                self.stitchingPlot.set_xscale('log')
            else:
                self.stitchingPlot.set_xscale('linear')

            self.stitchingPlot.draw()

            i += 1

        #if _data0.all_plot_axis.reduced_plot_stitching_tab_data_interval is None:
            #[xmin,xmax] = self.stitchingPlot.canvas.ax.xaxis.get_view_interval()
            #[ymin,ymax] = self.stitchingPlot.canvas.ax.yaxis.get_view_interval()
            #_data0.all_plot_axis.reduced_plot_stitching_tab_data_interval = [xmin,xmax,ymin,ymax]
            #_data0.all_plot_axis.reduced_plot_stitching_tab_view_interval = [xmin,xmax,ymin,ymax]
            #self.stitchingPlot.toolbar.home_settings = [xmin,xmax,ymin,ymax]
        #else:
            #[xmin,xmax,ymin,ymax] = _data0.all_plot_axis.reduced_plot_stitching_tab_view_interval
            #self.stitchingPlot.canvas.ax.set_xlim([xmin,xmax])
            #self.stitchingPlot.canvas.ax.set_ylim([ymin,ymax])
            #self.stitchingPlot.draw()

        #big_table_data[0,0] = _data0
        #self.parent.big_table_data = big_table_data

        self.stitchingPlot.set_xlabel(u'Q (1/Angstroms)')
        type = self.get_selected_reduced_output()
        if type == 'RvsQ':
            self.stitchingPlot.set_ylabel(u'R')
        elif type == 'RQ4vsQ':
            self.stitchingPlot.set_ylabel(u'RQ4')
        else:
            self.stitchingPlot.set_ylabel(u'Log(Q))')
        self.stitchingPlot.draw()

    def format_data_from_ymode_selected(self, q_axis, y_axis, e_axis):

        data_type = self.get_selected_reduced_output()
        [final_y_axis, final_e_axis] = self.get_formated_output(data_type, q_axis, y_axis, e_axis)
        return [final_y_axis, final_e_axis]

    def get_formated_output(self, data_type, _q_axis, _y_axis, _e_axis):

        try:
            # R vs Q selected
            if data_type == 'RvsQ':
                return [_y_axis, _e_axis]
    
            # RQ4 vs Q selected
            if data_type == 'RQ4vsQ':
                _q_axis_4 = _q_axis ** 4
                _final_y_axis = _y_axis * _q_axis_4
                _final_e_axis = _e_axis * _q_axis_4
                return [_final_y_axis, _final_e_axis]
    
            # Log(R) vs Q
            _final_y_axis = np.log(_y_axis)
            # _final_e_axis = np.log(_e_axis)
            _final_e_axis = _e_axis  ## FIXME
        except:
            _final_e_axis = _e_axis
            _final_y_axis = _y_axis
            
        return [_final_y_axis, _final_e_axis]

    def get_selected_reduced_output(self):
        o_gui_utility = GuiUtility(parent = self.parent)
        return o_gui_utility.get_reduced_yaxis_type()

    def display_loaded_ascii(self, _data_object):
        '''
        plot data coming from ascii file loaded
        '''
        _q_axis = _data_object.col1
        _y_axis = _data_object.col2
        _e_axis = _data_object.col3

        self.stitchingPlot.errorbar(_q_axis, _y_axis, yerr=_e_axis)
        self.stitchingPlot.draw()
