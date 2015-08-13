from PyQt4 import QtCore
from mantid.simpleapi import *

class LoadNexus(QtCore.QThread):
    
    def setup(self, parent, filename, output_wks, metadata_only=False):
        self.parent = parent
        self.filename = filename
        self.output_wks = output_wks
        self.metadata_only = metadata_only
        
    def run(self):
        _workspace = LoadEventNexus(Filename=self.filename,
                                    OutputWorkspace=self.output_wks,
                                    MetadataOnly=self.metadata_only)
    
    