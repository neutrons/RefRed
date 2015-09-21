import time
import os


class ExportDataReductionScript(object):
    
    script = []
    export_filename = ''
    
    def __init__(self, parent=None):
        self.parent = parent
        self.script = []
        
    def define_export_filename(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        _data = big_table_data[0, 0]
        run_number = _data.run_number
        default_filename = 'REFL_' + run_number + '_data_reduction_script.py'
        path = parent.path_ascii
        default_filename = path + '/' + default_filename
        filename = str(QtGui.QFileDialog.getSaveFileName(parent, 
                                                         'Python Script',
                                                         default_filename))
        if filename.strip() == '':
            return
        self.parent.path_ascii = os.path.dirname(filename)
        
    def make_script(self):
        if self.export_filename == '':
            return
        self.make_header_script()
        self.make_reduction_script()
        
    def make_header_script(self):
        scrit = self.script
        script.append('# RefRed Reduction script')
        _date = time.strftime("%d_%m_%Y")
        script.append('# Script automatically generated on ' + _date + '\n')
        script.appned('\n')
        script.append('import os\n')
        script.append('import mantid\n')
        script.append('from mantid.simpleapi import *\n')
        script.append('import LiquidsReflectometryReduction')
        self.script = script
        
    def make_reduction_script(self):
        

        
        
        
        