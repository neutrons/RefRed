from RefRed.utilities import weighted_mean_default
from RefRed.reduction.calculate_sf_overlap_range import CalculateSFoverlapRange
from RefRed.reduction.calculate_sf_critical_edge import CalculateSFCE


class ParentHandler(object):
    
    def __init__(self, parent=None, row_index=0):
        self.parent = parent
        self.row_index = row_index

class AbsoluteNormalization(ParentHandler):
    '''
    this class performs the absolute normalization of reduced data
    '''
    
    def __init__(self, parent=None, row_index=0):
        super(AbsoluteNormalization, self).__init__(parent = parent,
                                                    row_index = row_index)
        
    def run(self):
        if self.parent.ui.sf_button.isChecked():
            self.use_manually_defined_sf()
        else:
            self.use_first_angle_range()
    
    def use_manually_defined_sf(self):
        manual_sf = float(str(self.parent.ui.sf_value.text()))
    
    def use_first_angle_range(self):
        if self.row_index == 0:
            self.calculateSFCE(self)
        else:
            self.calcualteSFOtherAngles(self)
    
    def calculateSFCE(self):
        '''
        Scaling factor calculation of Ctritical Edge (CE)
        '''
        _q_min = float(str(self.parent.ui.sf_qmin_value.text()))
        _q_max = float(str(self.parent.ui.sf_qmax_value.text()))
        big_table_data = self.parent.big_table_data
        data_set = big_table_data[0, 2]
        calculate_sf = CalculateSFCE([_q_min, _q_max], data_set)
        _sf = 1./calculate_sf.run()
        data_set.sf_auto = _sf
        big_table_data[0, 2] = data_set
        self.parent.big_table_data = big_table_data
    
    def calculateSFOtherAngles(self):
        '''
        Scaling factor calculation of other angles
        '''
        _row_index = self.row_index
        left_lconfig = self.big_table_data[ _row_index-1, 2]
        right_lconfig = self.big_table_data[_row_index, 2]
        
        calculate_sf = CalculateSFoverlapRange(left_lconfig, right_lconfig)
        _sf = 1./calculate_sf.getSF()
        right_lconfig.sf_auto = _sf
        self.big_table_data[_row_index, 2] = right_lconfig
        self.parent.big_table_data = big_table_data


class AutomaticStitching(ParentHandler):
    '''
    automatic stiching of the reduced data using the Q range to calculate the CE
    '''
    
    def __init__(self, parent=None, row_index=0):
        super(AutomaticStitching, self).__init__(parent = parent,
                                                 row_index = row_index)
        
    def run(self):
        pass
    
    
class ManualStitching(ParentHandler):
    '''
    manual stitching of the data. The program will simply used the data defined
    in the main table to scaled the data    
    '''
    
    def __init__(self, parent=None, row_index=0):
        super(ManualStitching, self).__init__(parent = parent,
                                              row_index = row_index)
    
    def run(self):
        pass

