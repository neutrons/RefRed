from RefRed.calculations.locate_list_run import LocateListRun
from RefRed.calculations.load_list_nexus import LoadListNexus

class CheckListRunCompatibility(object):
    
    list_run = None
    
    def __init__(self, list_run=None):
        if list_run is None:
            return
        
        list_run_object = LocateListRun(list_run=list_run)
        list_nexus_found = list_run_object.list_nexus_found
        list_run_found = list_run_object.list_run_found
        
        list_wks_object = LoadListNexus(list_nexus=list_nexus_found, 
                                        list_run=list_run_found, 
                                        metadata_only=True)
        
        print(list_wks_object.list_wks_loaded)