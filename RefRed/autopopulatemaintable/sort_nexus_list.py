import numpy as np
import sys




class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SortNexusList(object):
    '''
    Will sort the NXSData list (numpy.ndarray) provided according to the criteria1 and criteria2
    where criteria1 and criteria2 looks like ['name_argumne','sort_order']
    sort_order is either 'increasing' or 'decreasing'
    '''
    
    parent = None
    
    list_nxs_sorted = None
    list_runs_sorted = None
    list_wks_sorted = None
    
    criteria_type = ['increase','decrease']
    list_nxs = None
    list_runs = None
    list_wks = None
    
    criteria1_value = None
    criteria1_type = ''
    
    criteria2_value = None
    criteria2_type = ''
        
    def __init__(self, parent = None, 
                 list_nxs = None, 
                 list_runs = None,
                 list_wks = None,
                 criteria1 = None, 
                 criteria2 = None):

        if list_nxs is None:
            raise MyError("Need a list of nexus")
        if type(list_nxs) is not np.ndarray:
            raise MyError("Need a numpy nexus_list array")
        if criteria1 is None and criteria2 is None:
            raise MyError("Need at least 1 criteria")

        if criteria1 is not None:
            if len(criteria1) != 2:
                raise MyError("Wrong criteria arguments number!")
            if not criteria1[1] in self.criteria_type:
                raise MyError("Wrong criteria1 argument name")
            [self.criteria1_value, self.criteria1_type] = criteria1

        if criteria2 is not None:
            if len(criteria2) != 2:
                raise MyError("Wrong criteria arguments number!")
            if not criteria2[1] in self.criteria_type:
                raise MyError("Wrong criteria2 argument name")
            [self.criteria2_value, self.criteria2_type] = criteria2
            
        self.list_nxs = list_nxs
        self.list_runs = list_runs
        self.list_wks = list_wks
        self.parent = parent
 
    def run(self):
        print('here')
        return
    
        _list_nxs = self.raw_list_nxs
        nbr_nxs = _list_nxs.size
        if nbr_nxs == 1:
            self.list_nxs_sorted = _list_nxs
            return
        
        sortnxs = SortNXSData(parent = self.parent, array_nxsdata_to_sort = _list_nxs)
        list_nxs_sorted = sortnxs.sortedArrayOfNXSData
        
    
        
        
        
