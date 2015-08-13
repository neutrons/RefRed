from mantid.simpleapi import *

INSTRUMENT_SHORT_NAME = "REF_L"

class LocateListRun(object):
   
    list_run = None
    list_nexus_found = []
    list_run_found = []
    list_run_not_found = []
    
    def __init__(self, list_run=None):
        if list_run is None:
            return
        self.list_run = list_run
        
        for run in list_run:
            try:
                nexus_file_name = FileFinder.findRuns("%s_%d" %(INSTRUMENT_SHORT_NAME, 
                                                                int(run)))[0]
                self.list_nexus_found.append(nexus_file_name)
                self.list_run_found.append(run)
            except:
                self.list_run_not_found.append(run)
                
            