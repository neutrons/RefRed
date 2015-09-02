class ExtractLConfigDataSetRuns(object):
    ''' This class get an array of LConfigDataSet and extract the data sets
    and append them in a list that is returned
    '''
    
    def __init__(self, lconfigdataset = None):
        self.lconfigdataset = lconfigdataset
    
    def list_runs(self):
        _data_set = self.lconfigdataset
        full_list_runs = []
        i=0
        
        for _lconfig in _data_set:
            if _lconfig is not None:
                _list_run = _lconfig.data_sets
                if _list_run is not ['']:
                    for _run in _list_run:
                        int_run = int(_run)
                        full_list_runs.append(int_run)
                
        return full_list_runs