from RefRed.calculations.locate_list_run import LocateListRun
from RefRed.calculations.load_list_nexus import LoadListNexus
from RefRed.calculations.check_if_same_nxs_property import CheckIfSameNxsProperty

class CheckListRunCompatibility(object):
    
    list_run = None
    list_wks = None
    
    list_run_found = None
    list_nexus_found = None
    
    runs_compatible = False
    no_nexus_found = True
    
    def __init__(self, list_run=None):
        if list_run is None:
            return
        
        list_run_object = LocateListRun(list_run=list_run)
        if list_run_object.list_nexus_found == []:
            return
        list_nexus_found = list_run_object.list_nexus_found
        list_run_found = list_run_object.list_run_found
        
        self.list_nexus_found = list_nexus_found
        self.list_run_found = list_run_found
        
        load_object = LoadListNexus(list_nexus=list_nexus_found, 
                                 list_run=list_run_found, 
                                 metadata_only=True)
        self.list_wks = load_object.list_wks_loaded
        
        same_property_object = CheckIfSameNxsProperty(list_wks = self.list_wks,
                                                      property_name = 'LambdaRequest')
        if same_property_object.is_same_property:
            self.runs_compatible = True
        else:
            self.runs_compatible = False
                    
        self.no_nexus_found = False