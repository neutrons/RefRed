# RefRed imports
from RefRed.configuration.global_settings import GlobalSettings
from RefRed.interfaces.deadtime_settings import DeadTimeSettingsModel


class GlobalReductionSettingsHandler(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.settings = {}
        self.retrieve_settings()

    def __getattr__(self, item):
        r"""Values from the settings dictionary can be fetched with the dot operator

        Example:
            g = GlobalReductionSettingsHandler()
            assert g.settings["q_min"] == g.q_min
        """
        if item in self.settings:
            return self.settings[item]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def retrieve_settings(self):
        r"""Retrieve the values of all the global settings from the GUI or from the GlobalSettings instances"""
        self.settings["incident_medium_selected"] = str(self.parent.ui.selectIncidentMediumList.currentText()).strip()
        self.settings["q_min"] = float(self.parent.gui_metadata['q_min'])
        self.settings["q_step"] = float(self.parent.ui.qStep.text())
        self.settings["scaling_factor_flag"] = self.parent.ui.scalingFactorFlag.isChecked()
        self.settings["scaling_factor_file"] = str(self.parent.full_scaling_factor_file_name)
        self.settings["slits_width_flag"] = True
        self.settings["angle_offset"] = float(self.parent.ui.angleOffsetValue.text())
        self.settings["angle_offset_error"] = float(self.parent.ui.angleOffsetError.text())
        self.settings["tof_steps"] = float(self.parent.ui.eventTofBins.text())
        self.settings["apply_normalization"] = self.parent.ui.useNormalizationFlag.isChecked()
        self.settings["dead_time"]: DeadTimeSettingsModel = self.parent.deadtime_settings

    def to_dict(self):
        r"""Return a dictionary with all the settings"""
        options = {}
        for settings_name in self.settings:
            settings_value = getattr(self, settings_name)
            if isinstance(settings_value, GlobalSettings):
                # complex settings are "uncompressed" themselves into their components
                options.update(settings_value.to_dict())
            else:
                options[settings_name] = settings_value
        return options
