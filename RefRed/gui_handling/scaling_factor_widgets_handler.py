from PyQt4 import QtGui
import os
from numpy import shape


class ScalingFactorWidgetsHandler(object):
    
    parent = None
    
    def __init__(self, parent = None):
        self.parent = parent
        
    def checkbox(self, status = True):
        self.parent.ui.scalingFactorConfigFrame.setEnabled(status)
        
    def browse(self):
        _path = self.parent.path_ascii
        filename = str(QtGui.QFileDialog.getOpenFileName(self.parent, 
                                                     'Open scaling factor file', 
                                                     _path,
                                                     "sfConfig (*.cfg)"))
        
        if filename == "":
            return
        
        self.parent.path_ascii = os.path.dirname(filename)
        self.fill_incident_medium_list(filename)
        
    def fill_incident_medium_list(self, filename):
        try:
            _listMedium = self.parse_scaling_factor_file(filename)
            self.parent.ui.selectIncidentMediumList.addItems(_listMedium)
            self.parent.ui.scalingFactorFile.setText(os.path.basename(filename))
            self.parent.full_scaling_factor_file_name = filename
        except:
            _listMedium = 'N/A'
        if self.parent.ui.selectIncidentMediumList.count() > 1:
            index = 1
        else:
            index = 0
        self.parent.ui.selectIncidentMediumList.setCurrentIndex(index)
        
    def parse_scaling_factor_file(self, filename):
        '''
        will parse the scaling factor file
        '''
        f = open(filename,'r')
        _sfFactorTable = []
        for line in f.read().split('\n'):
            if (len(line) > 0) and (line[0] != '#'):
                _sfFactorTable.append(line.split(' '))
        f.close()

        uniqIncidentMedium = self.list_uniq_incident_medium(_sfFactorTable)
        return uniqIncidentMedium
        
    def list_uniq_incident_medium(self, table):

        [nbr_row, nbr_column] = shape(table)
        first_column_only = []
        for i in range(nbr_row):
            _line_split = table[i][0].split('=')
            first_column_only.append(_line_split[1])

        return sorted(set(first_column_only))

        