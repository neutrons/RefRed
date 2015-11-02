from PyQt4 import QtGui
import time
import os
from mantid.simpleapi import *

import numpy as np
from RefRed.utilities import convertTOF

def createAsciiFile(filename, str_list):
    if os.path.isfile(filename):
        os.remove(filename)
    f = open(filename,'w')
    for _line in str_list:
        f.write(str(_line))
    f.close()

class ReductionSfCalculator(object):
    
    sf_gui = None
    export_script_flag = False
    export_script_file = ''
    export_script = []
    table_settings = []
    index_col = [0,1,5,10,11,12,13,14,15]
    nbr_row = -1
    nbr_scripts = 0
    new_sfcalculator_script = True
    
    def __init__(self, parent=None, export_script_flag=False):
        self.sf_gui = parent
        self.export_script_flag = export_script_flag
        
        if export_script_flag:
            #TODO: get last path from QSettings
            _path = os.path.expanduser('~')
            #_path = self.sf_gui.main_gui.path_config
            _filter = u'python (*.py);;All (*.*)'
            filename = QtGui.QFileDialog.getSaveFileName(self.sf_gui, 'Export Script File', _path, filter=_filter)
            if not(filename == ''):
                self.export_script_file = filename
                self.prepareExportScript()
            else:
                return
        self.collectTableSettings()
        self.createAndLaunchScripts()
                
    def collectTableSettings(self):
        nbr_row = self.sf_gui.tableWidget.rowCount()
        self.nbr_row = nbr_row
        nbr_column = len(self.index_col)
        _table_settings = np.zeros((nbr_row, nbr_column))
        
        for _row in range(nbr_row):
            for _col in range(nbr_column):
                if _col == 1:
                    _value = str(self.sf_gui.tableWidget.cellWidget(_row, self.index_col[_col]).value())
                else:
                    _value = str(self.sf_gui.tableWidget.item(_row, self.index_col[_col]).text())
                _table_settings[_row, _col] = _value
                
        self.table_settings = _table_settings
        
    def createAndLaunchScripts(self):
        from_to_index_same_lambda = self.generateIndexSameLambda()
        nbr_scripts = self.nbr_scripts
        
        incident_medium = self.getIncidentMedium()
        output_file_name = self.getOutputFileName()
        self.sf_gui.updateProgressBar(0.1)
        
        for i in range(nbr_scripts):
            from_index = int(from_to_index_same_lambda[i,0])
            to_index = int(from_to_index_same_lambda[i,1])

            if (to_index - from_index) <= 1:
                continue

            string_runs = self.getStringRuns(from_index, to_index)
            list_peak_back = self.getListPeakBack(from_index, to_index)
            tof_range = self.getTofRange(from_index)
            
            if not self.export_script:
                self.launchScript(string_runs = string_runs,
                             list_peak_back = list_peak_back,
                             incident_medium = incident_medium,
                             output_file_name = output_file_name,
                             tof_range = tof_range)
            
                self.refreshOutputFileContainPreview(output_file_name)
            else:
                self.exportScript(string_runs = string_runs,
                             list_peak_back = list_peak_back,
                             incident_medium = incident_medium,
                             output_file_name = output_file_name,
                             tof_range = tof_range)
    
            self.sf_gui.updateProgressBar(float(i+1)/float(nbr_scripts))
            QtGui.QApplication.processEvents()
        
        if self.export_script_flag:
            createAsciiFile(self.export_script_file, self.export_script)

    def launchScript(self, string_runs = '', list_peak_back=[], incident_medium = '', output_file_name = '', tof_range = []):
        peak_ranges = []
        bck_ranges = []
        for item in list_peak_back:
            peak_ranges.append(int(item[0]))
            peak_ranges.append(int(item[1]))
            bck_ranges.append(int(item[2]))
            bck_ranges.append(int(item[3]))
        
        run_list = []
        att_list = []
        toks = string_runs.strip().split(',')
        for item in toks:
            pair = item.strip().split(':')
            run_list.append(int(pair[0]))
            att_list.append(int(pair[1]))
            
        LRScalingFactors(DirectBeamRuns = run_list,
                         Attenuators = att_list,
                         IncidentMedium = str(incident_medium),
                         TOFRange = tof_range, TOFSteps = 200,
                         SignalPeakPixelRange = peak_ranges, 
                         SignalBackgroundPixelRange = bck_ranges,
                         ScalingFactorFile= str(output_file_name))


    def prepareExportScript(self):
        script = []
        script.append('# quicksNXS LRScalingFactors scaling factor calculation script\n')
        _date = time.strftime("%d_%m_%Y")
        script.append('# Script  automatically generated on ' + _date + '\n')
        script.append('\n')
        script.append('import os\n')
        script.append('import mantid\n')
        script.append('from mantid.simpleapi import *\n')
        self.export_script = script

    def exportScript(self, string_runs = '', list_peak_back=[], incident_medium = '', output_file_name = '', tof_range = []):
        self.export_script.append('\n')

        peak_ranges = []
        bck_ranges = []
        for item in list_peak_back:
            peak_ranges.append(int(item[0]))
            peak_ranges.append(int(item[1]))
            bck_ranges.append(int(item[2]))
            bck_ranges.append(int(item[3]))
    
        run_list = []
        att_list = []
        toks = string_runs.strip().split(',')
        for item in toks:
            pair = item.strip().split(':')
            run_list.append(int(pair[0]))
            att_list.append(int(pair[1]))
    
        _script_exe = 'LRScalingFactors(DirectBeamRuns = ['
        str_run_list = ', '.join(map(lambda x: str(x), run_list))
        _script_exe += str_run_list + '], Attenuators = ['
        str_att_list = ', '.join(map(lambda x: str(x), att_list))
        _script_exe += str_att_list + '], IncidentMedium = '
        _script_exe += '"' + incident_medium + '", TOFRange = ['
        str_tof_list = ', '.join(map(lambda x: str(x), tof_range))
        _script_exe += str_tof_list + '], TOFSteps=200, '
        _script_exe += 'SignalPeakPixelRange=['
        str_peak_range = ', '.join(map(lambda x: str(x), peak_ranges))
        _script_exe += str_peak_range + '], SignalBackgroundPixelRange = ['
        str_back_range = ', '.join(map(lambda x: str(x), bck_ranges))
        _script_exe += str_back_range + '], ScalingFactorFile = "'
        _script_exe += output_file_name + '")'
        
        self.export_script.append(_script_exe)

    def refreshOutputFileContainPreview(self, output_file_name):
        self.sf_gui.displayConfigFile(output_file_name)

    def getStringRuns(self, from_index, to_index):
        data = self.table_settings
        string_list = []
        for i in range(from_index, to_index+1):
            string_list.append(str(int(data[i,0])) + ":" + str(int(data[i,1])))
        return ",".join(string_list)

    def getListPeakBack(self, from_index, to_index):
        data = self.table_settings
        return data[from_index:to_index+1, 3:7]
    
    def getIncidentMedium(self):
        return self.sf_gui.incidentMediumComboBox.currentText()
    
    def getOutputFileName(self):
        output_file_name = self.sf_gui.sfFileNameLabel.text()
        return output_file_name
    
    def getTofRange(self, from_index):
        data = self.table_settings
        from_tof_ms = data[from_index, 7]
        to_tof_ms = data[from_index, 8 ]
        tof_from_to_micros = convertTOF([from_tof_ms, to_tof_ms], from_units='ms', to_units='micros')
        return tof_from_to_micros

    def generateIndexSameLambda(self):
        _data = self.table_settings

        lambda_list = _data[:,2]        
        nbr_scripts = len(set(lambda_list))
        self.nbr_scripts = nbr_scripts
        
        from_to_index_same_lambda = np.zeros((nbr_scripts, 2))
        
        first_index_lambda = 0
        ref_lambda = lambda_list[0]
        index_script = 0
        for i in range(1,self.nbr_row):
            live_lambda = lambda_list[i]
            if (live_lambda != ref_lambda):
                from_to_index_same_lambda[index_script,:] = [first_index_lambda, i-1]
                first_index_lambda = i
                ref_lambda = live_lambda
                index_script+= 1
            if  i == (self.nbr_row-1):
                from_to_index_same_lambda[index_script,:] = [ first_index_lambda, i]

        return from_to_index_same_lambda

