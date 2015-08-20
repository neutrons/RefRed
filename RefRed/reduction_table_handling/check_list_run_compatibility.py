from RefRed.calculations.locate_list_run import LocateListRun
from RefRed.calculations.load_list_nexus import LoadListNexus
from RefRed.calculations.check_if_same_nxs_property import CheckIfSameNxsProperty

class CheckListRunCompatibility(object):
    
    list_wks = None
    
    runs_compatible = False
    no_nexus_found = True
    
    def __init__(self, list_nexus=None, list_run=None):
        if list_run is None:
            return

        list_run_found = list_run
        list_nexus_found = list_nexus
        
        load_object = LoadListNexus(list_nexus = list_nexus_found, 
                                 list_run = list_run_found, 
                                 metadata_only = True)
        self.list_wks = load_object.list_wks_loaded
        
        same_property_object = CheckIfSameNxsProperty(list_wks = self.list_wks,
                                                      property_name = 'LambdaRequest')
        if same_property_object.is_same_property:
            self.runs_compatible = True
        else:
            self.runs_compatible = False
                    
        self.no_nexus_found = False