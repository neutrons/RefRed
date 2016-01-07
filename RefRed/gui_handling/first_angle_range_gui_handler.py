class ParentGuiHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent


class FirstAngleRangeGuiHandler(ParentGuiHandler):
    '''
    This class allows to enable or not the First Angle widgets 
    according to status of SF or first_angle buttons in the 
    stitching tab
    '''

    def __init__(self, parent=None):
        super(FirstAngleRangeGuiHandler, self).__init__(parent=parent)
        
    def setWidgets(self, is_sf_button_clicked = True):
        self.parent.ui.qmin_label.setEnabled(not is_sf_button_clicked)
        self.parent.ui.qmax_label.setEnabled(not is_sf_button_clicked)
        self.parent.ui.sf_qmin_value.setEnabled(not is_sf_button_clicked)
        self.parent.ui.sf_qmax_value.setEnabled(not is_sf_button_clicked)
        self.parent.ui.qmin_units.setEnabled(not is_sf_button_clicked)
        self.parent.ui.qmax_units.setEnabled(not is_sf_button_clicked)
        self.parent.ui.sf_value.setEnabled(is_sf_button_clicked)
        
    def is_sf_button_clicked(self):
        return self.parent.ui.sf_button.isChecked()
    

class NormalizationOrStitchingButtonStatus(ParentGuiHandler):
    
    is_absolute_normalization = True
    is_auto_stitching = False
    is_manual_stitching = False
    
    def __init__(self, parent=None):
        super(NormalizationOrStitchingButtonStatus, self).__init__(parent = parent)

    def setWidget(self, activated_button=0):
        self.resetAllWidgets()
        if activated_button == 0:
            self.is_absolute_normalization = True
        elif activated_button == 1:
            self.is_auto_stitching = True
        else:
            self.is_manual_stitching = True
            
        self.handleWidgets()
        
    def handleWidgets(self):
        if self.is_manual_stitching:
            self.parent.ui.sf_first_angle_range_group.setEnabled(False)
            return
        else:
            self.parent.ui.sf_first_angle_range_group.setEnabled(True)
            
        first_angle_handler = FirstAngleRangeGuiHandler(parent = self.parent)
        is_sf_button_clicked = first_angle_handler.is_sf_button_clicked()
        if self.is_auto_stitching:
            self.parent.ui.first_angle_range_button.setEnabled(False)
            first_angle_handler.setWidgets(is_sf_button_clicked = False)
            self.parent.ui.sf_button.setEnabled(False)
            self.parent.ui.sf_value.setEnabled(False)
            return
        else:
            self.parent.ui.first_angle_range_button.setEnabled(True)
            first_angle_handler.setWidgets(is_sf_button_clicked = is_sf_button_clicked)
            self.parent.ui.sf_button.setEnabled(True)
            self.parent.ui.sf_value.setEnabled(True)
        
    def resetAllWidgets(self):
        self.is_absolute_normalization = False
        self.is_auto_stitching = False
        self.is_manual_stitching = False


class NormalizationOrStitchingGuiHandler(NormalizationOrStitchingButtonStatus):
    '''
    Various widgets have to be enabled or not according to 
    status of the 3 main buttons: Absolute_Normalization, Auto._Stitching and
    Manual_Stitching
    '''
    
    def __init__(self, parent=None):
        super(NormalizationOrStitchingGuiHandler, self).__init__(parent = parent)
        
    
        