from RefRed.calculations.locate_list_run import LocateListRun
from RefRed.calculations.load_list_nexus import LoadListNexus
from mantid.simpleapi import *

class CheckListRunCompatibility(object):
    
    list_run = None
    list_wks = None
    
    runs_compatible = False
    
    def __init__(self, list_run=None):
        if list_run is None:
            return
        
        list_run_object = LocateListRun(list_run=list_run)
        list_nexus_found = list_run_object.list_nexus_found
        list_run_found = list_run_object.list_run_found
        
        load_object = LoadListNexus(list_nexus=list_nexus_found, 
                                 list_run=list_run_found, 
                                 metadata_only=True)
        self.list_wks = load_object.list_wks_loaded
        
        if self.wks_have_same_lambda_requested():
            self.runs_compatible = True
        else:
            self.runs_compatible = False
                    
    def wks_have_same_lambda_requested(self):
        if len(self.list_wks) < 2:
            return True
        
        list_wks = self.list_wks
        _lambda_source = self.get_lambda_requested(list_wks[0])
        for index in range(1, len(list_wks)):
            _lambda_target = self.get_lambda_requested(list_wks[index])
            if (_lambda_target != _lambda_source):
                return False
        return True
        
    def get_lambda_requested(self, wks):
        mt_run = wks.getRun()
        lambda_requested = float(mt_run.getProperty('LambdaRequest').value[0])
        return lambda_requested
            