from mantid import mtd
from mantid.simpleapi import CreateWorkspace, Fit, ReplaceSpecialValues
import numpy as np


class CalculateSFoverlapRange(object):
    '''
    calculate the scaling factor (SF) to apply to match the average value of the overlap range
    of data between the two lconfig data sets
    '''

    def __init__(self, left_lconfig, right_lconfig):
        self.left_lconfig = left_lconfig
        self.right_lconfig = right_lconfig

    def getSF(self):
        '''
        fit data of the overlaping region between left and right sets
        '''
        left_set = self.applySFtoLconfig(self.left_lconfig)
        right_set = self.right_lconfig

        left_x_axis = left_set.reduce_q_axis
        right_x_axis = right_set.reduce_q_axis
        [min_x, max_x, index_min_in_left, index_max_in_right, no_overlap] = \
            self.calculateOverlapAxis(left_x_axis, right_x_axis)

        if no_overlap:
            _sf = 1

        else:
            [a_left, b_left] = self.fitData(left_set, index_min_in_left, type='left')
            [a_right, b_right] = self.fitData(right_set, index_max_in_right, type='right')

            nbr_points = 10
            fit_range_to_use = self.gitFittingOverlapRange(min_x, max_x, nbr_points)

            _sf = self.scaleToApplyForBestOverlap(fit_range_to_use, a_left, b_left, a_right, b_right)

        return _sf

    def applySFtoLconfig(self, lconfig):
        '''
        use the auto_sf to the data set 
        '''
        y_axis = lconfig.reduce_y_axis
        e_axis = lconfig.reduce_e_axis
        sf = lconfig.sf_auto

        y_axis = y_axis * sf
        e_axis = e_axis * sf

        lconfig.tmp_y_axis = y_axis
        lconfig.tmp_e_axis = e_axis

        return lconfig

    def gitFittingOverlapRange(self, min_x, max_x, nbr_points):

        step = (float(max_x) - float(min_x)) / float(nbr_points)
        _fit_range = np.arange(min_x, max_x + step, step)
        return _fit_range

    def calculateOverlapAxis(self, left_axis, right_axis):
        '''
        calculate the overlap region of the two axis
        '''
        _min_x = -1
        _max_x = -1
        no_overlap = True
        left_min_index = 0
        right_max_index = -1

        if left_axis[-1] <= right_axis[0]: # no overlap
            return [_min_x, _max_x, left_min_index, right_max_index, no_overlap]

        _min_x = right_axis[0]
        _max_x = left_axis[-1]
        no_overlap = False

        left_min_index = self.findNearest(left_axis, _min_x)
        right_max_index = self.findNearest(right_axis, _max_x)

        return [_min_x, _max_x, left_min_index, right_max_index, no_overlap]

    def fitData(self, data_set, threshold_index, type='right'):
        '''
        will fit the data with linear fitting y=ax + b
        '''
        if type == 'left':
            x_axis = data_set.reduce_q_axis[threshold_index:]
            y_axis = data_set.tmp_y_axis[threshold_index:]
            e_axis = data_set.tmp_e_axis[threshold_index:]
        else:
            x_axis = data_set.reduce_q_axis[:threshold_index+1]
            y_axis = data_set.reduce_y_axis[:threshold_index+1]
            e_axis = data_set.reduce_e_axis[:threshold_index+1]

        dataToFit = CreateWorkspace(DataX=x_axis,
                                    DataY=y_axis,
                                    DataE=e_axis,
                                    Nspec=1)

        dataToFit = ReplaceSpecialValues(InputWorkspace=dataToFit, 
                                         NaNValue=0,
                                         NaNError=0,
                                         InfinityValue=0,
                                         InfinityError=0)

        Fit(InputWorkspace = dataToFit, 
            Function = "name=UserFunction, Formula=a+b*x, a=1, b=2",
            Output='res')

        res = mtd['res_Parameters']

        b = res.cell(0,1)
        a = res.cell(1,1)

        return [a,b]

    def findNearest(self, array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    def scaleToApplyForBestOverlap(self, fit_range_to_use, a_left, b_left, a_right, b_right):
        '''
        This function will use the same overlap region and will determine the scaling to apply to 
        the second fit to get the best match
        '''
        left_mean = self.calculateMeanOfFunctionOverRange(fit_range_to_use, a_left, b_left)
        right_mean = self.calculateMeanOfFunctionOverRange(fit_range_to_use, a_right, b_right)
        _sf =  right_mean / left_mean
        return _sf

    def calculateMeanOfFunctionOverRange(self, range_to_use, a, b):
        '''
        will return the average value of the function over the given range
        '''
        sz_range = range_to_use.size
        _sum = 0
        for i in range(sz_range):
            _value = self.fct(a=a, b=b, x=range_to_use[i])
            _sum += _value
        _mean = float(_sum) / float(sz_range)
        return _mean

    def fct(self, a, b, x):
            _value = a * x + b
            return _value
