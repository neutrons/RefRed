import math
from mantid.simpleapi import *
import numpy as np

from RefRed.reduction.normalization_stitching import AbsoluteNormalization
from RefRed.reduction.normalization_stitching import AutomaticStitching
from RefRed.reduction.normalization_stitching import ManualStitching
from RefRed.gui_handling.gui_utility import GuiUtility


class LiveCalculateSF(object):
    '''
    This class will determine the best scaling factor (SF) to apply to the data to stitch them
    '''

    big_table_data = []
    parent = None
    row_index = 0

    def __init__(self, parent=None, row_index = 0):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data
        self.row_index = row_index

    def run(self):
        '''
        main part of the program that will calculate the various SF
        '''
        
        o_gui = GuiUtility(parent = self.parent)
        stitching_type = o_gui.getStitchingType()
        
        if stitching_type is 'absolute':
            self.absolute_normalization_calculation(row_index = self.row_index)
        elif stitching_type is 'auto':
            self.auto_stitching_calculation(row_index = self.row_index)
        else:
            self.manual_stitching_calculation(row_index = self.row_index)

    def absolute_normalization_calculation(self, row_index = row_index):
        '''
        will perform the absolute normalization
        '''
        o_abs_norm = AbsoluteNormalization(parent = self.parent, row_index = row_index)
        o_abs_norm.run()

    def auto_stitching_calculation(self, row_index = row_index):
        '''
        will perform the auto stitching normalization
        '''
        o_auto_stit = AutomaticStitching(parent = self.parent, row_index = row_index)
        o_auto_stit.run()
    
    def manual_stitching_calculation(self, row_index = row_index):
        '''
        will perform the manual stitching normalization
        '''
        o_manual_stit = ManualStitching(parent = self.parent, row_index = row_index)
        o_manual_stit.run()

    

   
    #def fit_data_of_overlap_range(self, left_set, right_set):
        #'''
        #fit data of the overlaping region between left and right sets
        #'''
        #left_x_axis = left_set.reduce_q_axis
        #right_x_axis = right_set.reduce_q_axis
        #[min_x, max_x, index_min_in_left, index_max_in_right, no_overlap] = self.calculate_overlap_axis(left_x_axis, right_x_axis)
        #if no_overlap:
            #_sf = 1

        #else:
            #[a_left, b_left] = self.fit_data(left_set, index_min_in_left, type='left')
            #[a_right, b_right] = self.fit_data(right_set, index_max_in_right, type='right')

            #nbr_points = 10
            #fit_range_to_use = self.git_fitting_overlap_range(min_x, max_x, nbr_points)

            #_sf = self.scale_to_apply_for_best_overlap(fit_range_to_use, a_left, b_left, a_right, b_right)

        #return _sf


    #def calculate_ratio_of_left_right_mean(self, left_set, right_set):
        #'''
        #calculate ratio of left and right mean
        #'''
        #left_x_axis = left_set.reduce_q_axis
        #right_x_axis = right_set.reduce_q_axis
        #[min_x, max_x, no_overlap] = self.calculate_overlap_axis(left_x_axis, right_x_axis)
        #if no_overlap:
            #_sf = 1
        #else:
            #left_mean = self.calculate_left_weighted_mean(min_x, max_x, left_set.tmp_y_axis, tmp_e_axis)
            #right_mean = self.calculateRightweighted_mean(min_x, max_x, right_set.reduce_y_axis, right_set.reduce_e_axis)


    #def apply_left_sf(self, left_set):
        #'''
        #In order to calculate the right SF, we must apply the previously calculated left SF
        #'''
        #y_axis = left_set.reduce_y_axis
        #e_axis = left_set.reduce_e_axis
        #sf = left_set.sf_auto

        #y_axis = y_axis * sf
        #e_axis = e_axis * sf

        #left_set.tmp_y_axis = y_axis
        #left_set.tmp_e_axis = e_axis

        #return left_set


    #def  calculate_left_weighted_mean(self, min_x, max_x, x_axis, y_axis, e_axis):
        #pass


    #def fit_data(self, data_set, threshold_index, type='right'):
        #'''
        #will fit the data with linear fitting y=ax + b
        #'''
        #a = 0
        #b = 0

        #if type == 'left':
            #x_axis = data_set.reduce_q_axis[threshold_index:]
            #y_axis = data_set.tmp_y_axis[threshold_index:]
            #e_axis = data_set.tmp_e_axis[threshold_index:]
        #else:
            #x_axis = data_set.reduce_q_axis[:threshold_index+1]
            #y_axis = data_set.reduce_y_axis[:threshold_index+1]
            #e_axis = data_set.reduce_e_axis[:threshold_index+1]


        #dataToFit = CreateWorkspace(DataX = x_axis,
                                    #DataY = y_axis,
                                    #DataE = e_axis,
                                    #Nspec = 1)

        #dataToFit = ReplaceSpecialValues(InputWorkspace = dataToFit, 
                                         #NaNValue = 0,
                                         #NaNError = 0,
                                         #InfinityValue = 0,
                                         #InfinityError = 0)

        #Fit(InputWorkspace = dataToFit, 
            #Function = "name=UserFunction, Formula=a+b*x, a=1, b=2",
            #Output='res')

        #res = mtd['res_Parameters']

        #b = res.cell(0,1)
        #a = res.cell(1,1)

        #return [a,b]


    #def scale_to_apply_for_best_overlap(self, fit_range_to_use, a_left, b_left, a_right, b_right):
        #'''
        #This function will use the same overlap region and will determine the scaling to apply to 
        #the second fit to get the best match
        #'''

        #left_mean = self.calculate_mean_of_function_over_range(fit_range_to_use, a_left, b_left)
        #right_mean = self.calculate_mean_of_function_over_range(fit_range_to_use, a_right, b_right)

        #_sf =  right_mean / left_mean

        #return _sf


    #def calculate_overlap_axis(self, left_axis, right_axis):
        #'''
        #calculate the overlap region of the two axis
        #'''
        #global_min = min([left_axis[0], right_axis[0]])
        #global_max = max([left_axis[-1], right_axis[-1]])

        #_min_x = -1
        #_max_x = -1
        #no_overlap = True
        #left_min_index = 0
        #right_max_index = -1

        #if left_axis[-1] <= right_axis[0]: # no overlap
            #return [_min_x, _max_x, left_min_index, right_max_index, no_overlap]

        #_min_x = right_axis[0]
        #_max_x = left_axis[-1]
        #no_overlap = False

        #left_min_index = self.find_nearest(left_axis, _min_x)
        #right_max_index = self.find_nearest(right_axis, _max_x)

        #return [_min_x, _max_x, left_min_index, right_max_index, no_overlap]


    #def find_nearest(self, array, value):
        #idx = (np.abs(array-value)).argmin()
        #return idx


    #def git_fitting_overlap_range(self, min_x, max_x, nbr_points):

        #step = (float(max_x) - float(min_x)) / float(nbr_points)
        #_fit_range = np.arange(min_x, max_x + step, step)
        #return _fit_range


   