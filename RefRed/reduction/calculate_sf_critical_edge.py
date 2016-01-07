from RefRed.utilities import weighted_mean_default


class CalculateSFCE(object):
    
    def __init__(self, q_range, lconfig):
        [self._q_min, self._q_max] = q_range
        self.lconfig = lconfig
        
    def getSF(self):
        _q_axis = self.lconfig.reduce_q_axis
        [q_min_index, q_max_index] = self.get_q_range_index(q_axis = _q_axis, 
                                                            q_min = self._q_min, 
                                                            q_max = self._q_max)
    
    
        _y_axis = data_set.reduce_y_axis[q_min_index : q_max_index].copy()
        _e_axis = data_set.reduce_e_axis[q_min_index : q_max_index].copy()
        _error_0 = 1./ data_set.proton_charge
        [data_mean, error_mean] = weighted_mean_default(_y_axis,
                                                        _e_axis,
                                                        _error_0)
    
        _sf = 1./data_mean
        
    def get_q_range_index(self, q_axis=None, q_min=0, q_max=0.01):
        '''
        return the range of q_axis that are within the q_min and q_max
        values specified
        '''
        min_index = 0
        max_index = len(q_axis)-1
        for _index, _q_value in enumerate(q_axis):
            if _q_value >= q_min:
                min_index = _index
            if _q_value > q_max:
                max_index = _index - 1
            elif _q_value == q_max:
                max_index = _index
        return [min_index, max_index]
        