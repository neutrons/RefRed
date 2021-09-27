from qtpy import QtWidgets
from RefRed import nexus_utilities
import os


class BrowsingRuns(object):
    
    list_files = None
    list_runs = None
    
    def __init__(self, parent=None, data_type='data'):
        self.parent = parent
        self.data_type = data_type
        
        self._select_files()
        self._populate_line_edit()
        
    def _select_files(self):
        _path = self.parent.path_config
        _filter = ("NeXus (*.nxs);;All (*.*)")
        _title = "Select %s NeXus files" % self.data_type
        filenames = QtWidgets.QFileDialog.getOpenFileNames(self.parent,
                                                       _title,
                                                       _path,
                                                       _filter)
        
        QtWidgets.QApplication.processEvents()
        if filenames == "":
            self.parent.browsed_files[self.data_type] = None
            return
        
        # format list of full file name to string
        _list_files = [str(_file) for _file in filenames]
        self.list_files = _list_files
        self.parent.browsed_files[self.data_type] = _list_files
        self.parent.path_config = os.path.dirname(_list_files[0])

    def _populate_line_edit(self):
        _list_runs = []
        for _run in self.list_files:
            _run_number = nexus_utilities.get_run_number(_run)
            _list_runs.append(_run_number)
            
        _unique_list_runs = set(_list_runs) 
        str_list = ",".join(_unique_list_runs)

        if self.data_type is 'data':
            self.parent.ui.data_sequence_lineEdit.setText(str_list)
        else:
            self.parent.ui.norm_sequence_lineEdit.setText(str_list)
