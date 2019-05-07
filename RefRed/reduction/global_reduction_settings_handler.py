class GlobalReductionSettingsHandler(object):

    incident_medium_selected = ''
    geometry_correction_flag = False
    q_min = 0.005
    q_step = 50
    scaling_factor_file = ''
    scaling_factor_flag = True
    slits_width_flag = True
    angle_offset = 0.0
    angle_offset_error = 0.0
    tof_steps = 40  # microS

    def __init__(self, parent=None):
        self.parent = parent
        self.retrieve()

    def retrieve(self):
        self.incident_medium_selected = self.get_incident_medium_selected()
        self.q_step = self.get_q_step()
        self.scaling_factor_flag = self.get_scaling_factor_flag()
        self.scaling_factor_file = self.get_scaling_factor_file()
        self.angle_offset = self.get_angle_offset()
        self.angle_offset_error = self.get_angle_offset_error()
        self.tof_steps = self.get_tof_steps()

    def get_tof_steps(self):
        return float(self.parent.ui.eventTofBins.text())

    def get_angle_offset(self):
        return float(self.parent.ui.angleOffsetValue.text())

    def get_angle_offset_error(self):
        return float(self.parent.ui.angleOffsetError.text())

    def get_scaling_factor_flag(self):
        return self.parent.ui.scalingFactorFlag.isChecked()

    def get_scaling_factor_file(self):
        return str(self.parent.full_scaling_factor_file_name)

    def get_q_step(self):
        _q_step = self.parent.ui.qStep.text()
        try:
            _q_value = float(_q_step)
        except:
            _q_value = 0.01
        return _q_value

    def get_incident_medium_selected(self):
        _medium_selected = str(self.parent.ui.selectIncidentMediumList.currentText()).strip()
        return str(_medium_selected)
