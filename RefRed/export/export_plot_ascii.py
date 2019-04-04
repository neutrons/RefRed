import os
from PyQt4 import QtGui
import RefRed.utilities
from RefRed.export.output_reduced_data import OutputReducedData
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.utilities import makeSureFileHasExtension


class ExportPlotAscii(object):

    parent = None
    data_type = 'yt'

    def __init__(self, parent=None, data_type='yt'):
        self.parent = parent
        self.data_type = data_type

    def export(self):
        _data_type = self.data_type
        if _data_type == 'yt':
            self.export_yt()
        elif _data_type == 'ix':
            self.export_ix()
        elif _data_type == 'it':
            self.export_it()
        elif _data_type == 'yi':
            self.export_yi()
        elif _data_type == 'stitched':
            self.export_stitched()

    def export_yt(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row, col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        run_number = _data.run_number
        default_filename = 'REFL_' + run_number + '_2dPxVsTof.txt'
        path = parent.path_ascii
        default_filename = path + '/' + default_filename
        filename = str(QtGui.QFileDialog.getSaveFileName(parent, 
                                                         'Create 2D Pixel VS TOF', 
                                                         default_filename))

        if filename.strip() == '':
            return

        parent.path_ascii = os.path.dirname(filename)
        filename = makeSureFileHasExtension(filename, default_ext=".txt")
        image = _data.ytofdata
        RefRed.utilities.output_2d_ascii_file(filename, image)

    def export_ix(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row,col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        run_number = _data.run_number
        default_filename = 'REFL_' + run_number + '_ix.txt'
        path = parent.path_ascii
        default_filename = path + '/' + default_filename
        filename = str(QtGui.QFileDialog.getSaveFileName(parent, 
                                                         'Create Counts vs Pixel (low resolution range) ASCII File', 
                                                         default_filename))

        if filename.strip() == '':
            return

        parent.path_ascii = os.path.dirname(filename)
        filename = makeSureFileHasExtension(filename, default_ext=".txt")
        countsxdata = _data.countsxdata
        pixelaxis = range(len(countsxdata))

        text = ['#Counts vs Pixels (low resolution range)','#Pixel - Counts']
        sz = len(pixelaxis)
        for i in range(sz):
            _line = str(pixelaxis[i]) + ' ' + str(countsxdata[i])
            text.append(_line)
        RefRed.utilities.write_ascii_file(filename, text)

    def export_it(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row,col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        run_number = _data.run_number
        default_filename = 'REFL_' + run_number + '_yt.txt'
        path = parent.path_ascii
        default_filename = path + '/' + default_filename
        filename = str(QtGui.QFileDialog.getSaveFileName(parent, 
                                                         'Create Counts vs TOF ASCII File', 
                                                         default_filename))

        if filename.strip() == '':
            return

        parent.path_ascii = os.path.dirname(filename)
        countstofdata = _data.countstofdata
        filename = makeSureFileHasExtension(filename, default_ext=".txt")
        tof = _data.tof_axis_auto_with_margin
        if tof[-1] > 1000:
            tof /= 1000.

        text = ['#Counts vs  TOF','#TOF(ms) - Counts']
        sz = len(tof)-1
        for i in range(sz):
            _line = str(tof[i]) + ' ' + str(countstofdata[i])
            text.append(_line)
        text.append(str(tof[-1]))
        RefRed.utilities.write_ascii_file(filename, text)
        
    def export_yi(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        [row,col] = self.get_current_row_col_displayed()
        _data = big_table_data[row, col]
        run_number = _data.run_number
        default_filename = 'REFL_' + run_number + '_rpx.txt'
        path = parent.path_ascii
        default_filename = path + '/' + default_filename
        filename = str(QtGui.QFileDialog.getSaveFileName(parent, 
                                                         'Create Counts vs Pixel ASCII File', 
                                                         default_filename))

        if filename.strip() == '':
            return

        parent.path_ascii = os.path.dirname(filename)
        filename = makeSureFileHasExtension(filename, default_ext=".txt")
        ycountsdata = _data.ycountsdata
        pixelaxis = range(len(ycountsdata))

        text = ['#Counts vs Pixels','#Pixel - Counts']
        sz = len(pixelaxis)
        for i in range(sz):
            _line = str(pixelaxis[i]) + ' ' + str(ycountsdata[i])
            text.append(_line)
        RefRed.utilities.write_ascii_file(filename, text)

    def export_stitched(self):
        _tmp = OutputReducedData(parent = self.parent)
        _tmp.show()

    def get_current_row_col_displayed(self):
        o_gui_utility = GuiUtility(parent = self.parent)
        row = o_gui_utility.get_current_table_reduction_check_box_checked()
        col = o_gui_utility.get_data_norm_tab_selected()
        return [row, col]
