class ExtractLConfigDataSetRuns(object):
    ''' This class get an array of LConfigDataSet and extract the data sets
    and append them in a list that is returned
    '''
    
    def __init__(self, lconfigdataset = None, data_type='data'):
        self.lconfigdataset = lconfigdataset
        self.data_type = data_type
    
    def list_runs(self):
        _data_set = self.lconfigdataset
        full_list_runs = []
        i=0
        
        for _lconfig in _data_set:
            if _lconfig is not None:
                if self.data_type is 'data':
                    _list_run = _lconfig.data_sets
                else:
                    _list_run = _lconfig.norm_sets
                    
                if _list_run is not ['']:
                    for _run in _list_run:
                        if _run is not '':
                            int_run = int(_run)
                            full_list_runs.append(int_run)
                
        return full_list_runs