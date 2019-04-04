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

    def __init__(self, parent=None, row_index=0):
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
            self.absolute_normalization_calculation(row_index=self.row_index)
        elif stitching_type is 'auto':
            self.auto_stitching_calculation(row_index=self.row_index)
        else:
            self.manual_stitching_calculation(row_index=self.row_index)

    def absolute_normalization_calculation(self, row_index = row_index):
        '''
        will perform the absolute normalization
        '''
        o_abs_norm = AbsoluteNormalization(parent=self.parent, row_index=row_index)
        o_abs_norm.run()

    def auto_stitching_calculation(self, row_index=row_index):
        '''
        will perform the auto stitching normalization
        '''
        o_auto_stit = AutomaticStitching(parent=self.parent, row_index=row_index)
        o_auto_stit.run()

    def manual_stitching_calculation(self, row_index = row_index):
        '''
        will perform the manual stitching normalization
        '''
        o_manual_stit = ManualStitching(parent=self.parent, row_index=row_index)
        o_manual_stit.run()
