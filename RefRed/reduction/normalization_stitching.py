import numpy as np

from RefRed.reduction.calculate_sf_overlap_range import CalculateSFoverlapRange


class ParentHandler(object):
    def __init__(self, parent=None, row_index=0, n_runs=1):
        self.parent = parent
        self.row_index = row_index
        self.n_runs = n_runs

    def _calculateSFCE(self, data_type="absolute"):
        '''
        Scaling factor calculation of Ctritical Edge (CE)
        '''
        _q_min = float(str(self.parent.ui.sf_qmin_value.text()))
        _q_max = float(str(self.parent.ui.sf_qmax_value.text()))

        values = np.zeros(0)
        errors = np.zeros(0)

        for row_index in range(self.n_runs):
            reduction_config = self.parent.big_table_data.reduction_config(row_index)
            low_bound = reduction_config.reduce_q_axis >= _q_min
            high_bound = reduction_config.reduce_q_axis <= _q_max
            indices = np.argwhere(low_bound & high_bound).T[0]

            _values_i = reduction_config.reduce_y_axis[indices]
            values = np.concatenate((values, _values_i))

            _errors_i = reduction_config.reduce_e_axis[indices]
            errors = np.concatenate((errors, _errors_i))

        if len(values) > 1:
            _sf = 1 / np.average(values, weights=1 / errors**2)
        else:
            _sf = 1

        # Save the SF in first run
        self.saveSFinLConfig(self.parent.big_table_data[0, 2], _sf, data_type=data_type)

    def saveSFinLConfig(self, lconfig, sf, data_type='absolute'):
        if data_type == 'absolute':
            lconfig.sf_abs_normalization = sf
        elif data_type == 'auto':
            lconfig.sf_auto = sf
        else:
            lconfig.sf_manual = sf

        return lconfig

    def getLConfig(self, row_index):
        big_table_data = self.parent.big_table_data
        data_set = big_table_data[row_index, 2]
        return data_set


class AbsoluteNormalization(ParentHandler):
    '''
    this class performs the absolute normalization of reduced data
    '''

    def __init__(self, parent=None, row_index=0, n_runs=1):
        super(AbsoluteNormalization, self).__init__(parent=parent, row_index=row_index, n_runs=n_runs)

    def run(self):
        if self.row_index == 0:
            if self.parent.ui.sf_button.isChecked():
                self.useManuallyDefineSF()
            else:
                self._calculateSFCE()
        else:
            self.copySFtoOtherAngles()

    def useManuallyDefineSF(self):
        _sf = float(str(self.parent.ui.sf_value.text()))
        data_set = self.getLConfig(0)
        data_set.sf_abs_normalization = _sf

    def copySFtoOtherAngles(self):
        ce_lconfig = self.getLConfig(0)
        _sf = ce_lconfig.sf_abs_normalization
        lconfig = self.getLConfig(self.row_index)
        lconfig = self.saveSFinLConfig(lconfig, _sf, data_type='absolute')


class AutomaticStitching(ParentHandler):
    '''
    automatic stiching of the reduced data using the Q range to calculate the CE
    '''

    def __init__(self, parent=None, row_index=0, n_runs=1):
        super(AutomaticStitching, self).__init__(parent=parent, row_index=row_index, n_runs=n_runs)

    def run(self):
        self.use_first_angle_range()

    def use_first_angle_range(self):
        if self.row_index == 0:
            self._calculateSFCE(data_type='auto')
        else:
            self._calculateSFOtherAngles()

    def _calculateSFOtherAngles(self):
        '''
        Scaling factor calculation of other angles
        '''
        _row_index = self.row_index
        left_lconfig = self.getLConfig(_row_index - 1)
        right_lconfig = self.getLConfig(_row_index)

        calculate_sf = CalculateSFoverlapRange(left_lconfig, right_lconfig)
        _sf = 1.0 / calculate_sf.getSF()
        right_lconfig.sf_auto = _sf


class ManualStitching(ParentHandler):
    '''
    manual stitching of the data. The program will simply used the data defined
    in the main table to scaled the data
    '''

    def __init__(self, parent=None, row_index=0, n_runs=1):
        super(ManualStitching, self).__init__(parent=parent, row_index=row_index, n_runs=n_runs)

    def run(self):
        ce_lconfig = self.getLConfig(self.row_index)
        _sf = ce_lconfig.sf_manual
        lconfig = self.getLConfig(self.row_index)
        lconfig = self.saveSFinLConfig(lconfig, _sf, data_type='manual')
