from RefRed.gui_handling.gui_utility import GuiUtility
import RefRed.constants


class AngleOffsetCalculation(object):
    
    parent = None
    angle_offset = None
    
    def __init__(self, parent=None, row=-1):
        
        self.parent = parent
        self.row = row
        self.calculate_angle_offset()
        self.set_new_angle_offset()
        
    def calculate_angle_offset(self):
        o_gui_utility = GuiUtility(parent = self.parent)
        if not o_gui_utility.is_data_tab_selected:
            self.angle_offset = float(str(self.parent.ui.angleOffsetValue.text()))
            return
        
        if self.row == -1:
            if o_gui_utility.data_norm_tab_widget_row_to_display != 0:
                self.angle_offset = float(str(self.parent.ui.angleOffsetValue.text()))
                return
        elif self.row != 0:
            self.angle_offset = float(str(self.parent.ui.angleOffsetValue.text()))
            return
            
        self.__get_angle_offset()
        
    def __get_angle_offset(self):
        peak1 = float(str(self.parent.ui.dataPeakFromValue.text()))
        peak2 = float(str(self.parent.ui.dataPeakToValue.text()))
        
        central_peak = (peak1 + peak2) / 2.
        ideal_central_offset = RefRed.constants.central_pixel
        
        delta_pixel = central_peak - ideal_central_offset
        size_pixel = RefRed.constants.pixel_size_mm
        delta_mm = delta_pixel * size_pixel
        
        # delta_mm / 2*lSD
        angle_value = delta_mm / (2 * RefRed.constants.distance_sample_detector)
        ideal_angle_offset = RefRed.constants.ideal_angle_offset

        self.angle_offset = angle_value + ideal_angle_offset
        
    def set_new_angle_offset(self):
        str_angle_offset = "%.4f" %self.angle_offset
        self.parent.ui.angleOffsetValue.setText(str_angle_offset)
            