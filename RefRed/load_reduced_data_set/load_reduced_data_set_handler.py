from PyQt4 import QtGui
import os
from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader
from RefRed.load_reduced_data_set.stitched_ascii_handler import StitchedAsciiHandler

class LoadReducedDataSetHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def run(self):
        _path = self.parent.path_ascii
        _filter = u"Ascii File (*.txt);; All (*.*)"
        filename = str(QtGui.QFileDialog.getOpenFileName(self.parent, 'Open Reduced Data Set', 
                                                     directory = _path,
                                                     filter = _filter))
        
        QtGui.QApplication.processEvents()
        if not (filename== ""):
            
            _new_path = os.path.dirname(filename)
            self.parent.path_ascii = _new_path
            
            o_loaded_ascii = ReducedAsciiLoader(parent = self.parent,
                                                ascii_file_name = filename)
            if self.parent.o_stitched_ascii is None:
                self.parent.o_stitched_ascii = StitchedAsciiHandler(parent = self.parent,
                                                                    loaded_ascii = o_loaded_ascii)
            else:
                self.parent.o_stitched_ascii.addData(o_loaded_ascii)
                
            self.plot()
            
    def plot(self):
        big_table_data = self.parent.big_table_data
        data = big_table_data[0,0]
        if data is None:
            o_user_configuration = self.parent.o_user_configuration
            _isylog = o_user_configuration.is_reduced_plot_stitching_tab_ylog
            _isxlog = o_user_configuration.is_reduced_plot_stitching_tab_xlog
        else:
            _isylog = data.all_plot_axis.is_reduced_plot_stitching_tab_ylog
            _isxlog = data.all_plot_axis.is_reduced_plot_stitching_tab_xlog
        
        self.parent.o_stitched_ascii.updateDisplay(isxlog = _isxlog,
                                                   isylog = _isylog)
        
            
        