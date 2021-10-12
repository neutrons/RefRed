from RefRed.utilities import weighted_mean_default


class CalculateSFCE(object):
    def __init__(self, q_range, lconfig):
        [self._q_min, self._q_max] = q_range
        self.lconfig = lconfig

    def getSF(self):
        _q_axis = self.lconfig.reduce_q_axis
        [q_min_index, q_max_index] = self.get_q_range_index(q_axis=_q_axis, q_min=self._q_min, q_max=self._q_max)

        _y_axis = self.lconfig.reduce_y_axis[q_min_index:q_max_index].copy()
        _e_axis = self.lconfig.reduce_e_axis[q_min_index:q_max_index].copy()
        _error_0 = 1.0 / self.lconfig.proton_charge

        [data_mean, _] = weighted_mean_default(_y_axis, _e_axis, _error_0)
        _sf = data_mean
        return _sf

    def get_q_range_index(self, q_axis=None, q_min=0, q_max=0.01):
        '''
        return the range of q_axis that are within the q_min and q_max
        values specified
        '''
        min_index = 0
        max_index = len(q_axis) - 1

        # figure out q_min_index
        for _index, _q_value in enumerate(q_axis):
            if _q_value >= q_min:
                min_index = _index
                break
        # figure out q_max_index
        for _index in range(max_index, 0, -1):
            _q_value = q_axis[_index]
            if _q_value <= q_max:
                max_index = _index
                break

        return [min_index, max_index]
