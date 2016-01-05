class FirstAngleRangeGuiHandler(object):
    
    def __init__(self, parent=None):
        self.parent = parent
        
    def setWidgets(self, is_sf_button_clicked = True):
        self.parent.ui.qmin_label.setEnabled(not is_sf_button_clicked)
        self.parent.ui.qmax_label.setEnabled(not is_sf_button_clicked)
        self.parent.ui.sf_qmin_value.setEnabled(not is_sf_button_clicked)
        self.parent.ui.sf_qmax_value.setEnabled(not is_sf_button_clicked)
        self.parent.ui.qmin_units.setEnabled(not is_sf_button_clicked)
        self.parent.ui.qmax_units.setEnabled(not is_sf_button_clicked)
        self.parent.ui.sf_value.setEnabled(is_sf_button_clicked)