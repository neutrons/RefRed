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
            
            o_loaded_ascii = ReducedAsciiLoader(parent=self.parent,
                                                ascii_file_name = filename)
            if self.parent.o_stitched_ascii is None:
                self.parent.o_stitched_ascii = StitchedAsciiHandler(parent = self.parent,
                                                                    loaded_ascii = o_loaded_ascii)
            else:
                self.parent.o_stitched_ascii.addData(o_loaded_ascii)
                
                
            
        