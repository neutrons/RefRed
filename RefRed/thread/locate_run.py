from PyQt4 import QtCore
import time
import mantid
import sys
from mantid.simpleapi import *
import RefRed.nexus_utilities

class LocateRunThread(QtCore.QThread):

    def setup(self, parent, run_number, index):   
        self.parent = parent
        self.run_number = run_number
        self.index = index
    
    def run(self):
        full_file_name = RefRed.nexus_utilities.findNeXusFullPath(self.run_number)
        if full_file_name == '':
            self.parent.number_of_runs = self.parent.number_of_runs - 1
            self.parent.list_full_file_name.pop()
        else:
            self.parent.list_full_file_name[self.index] = full_file_name
            self.parent.runs_found += 1
            
    def stop(self):
        pass
        
    def pause(self):
        pass
        

class LoadRunThread(QtCore.QThread):
    
    def setup(self, parent, file_name, output_wks, index):
        self.parent = parent
        self.file_name = file_name
        self.output_wks = output_wks
        self.index = index
        
    def run(self):
        _workspace = LoadEventNexus(Filename = self.file_name,
                                    OutputWorkspace = self.output_wks,
                                    MetadataOnly = True)
        self.parent.list_nxs[self.index] = self.output_wks
        self.parent.runs_loaded += 1
