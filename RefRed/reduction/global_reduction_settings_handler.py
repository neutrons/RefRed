# RefRed imports
from RefRed.configuration.global_settings import GlobalSettings


class GlobalReductionSettingsHandler(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.settings = {}

        self.retrieve_settings()

    def __getattr__(self, item):
        r"""Enables values from dictionary `self.settings` to be fetched with the dot operator

        Example
        -------
        g = GlobalReductionSettingsHandler()
        assert g.q_min == g.settings["q_min"]
        """
        if item in self.settings:
            return self.settings[item]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def retrieve_settings(self):
        r"""Retrieve the values of all the global settings from the GUI or from GlobalSettings instances"""
        self.settings.update(
            {
                "incident_medium_selected": str(self.parent.ui.selectIncidentMediumList.currentText()).strip(),
                "q_min": float(self.parent.gui_metadata['q_min']),
                "q_step": float(self.parent.ui.qStep.text()),
                "scaling_factor_flag": self.parent.ui.scalingFactorFlag.isChecked(),
                "scaling_factor_file": str(self.parent.full_scaling_factor_file_name),
                "slits_width_flag": True,
                "angle_offset": 0,
                "angle_offset_error": 0,
                "tof_steps": float(self.parent.ui.eventTofBins.text()),
                "apply_normalization": self.parent.ui.useNormalizationFlag.isChecked(),
                "dead_time": self.parent.deadtime_settings,  # an instance of `DeadTimeSettingsModel`
            }
        )

    def to_dict(self):
        r"""Return a dictionary with all the settings"""
        options = {}
        for settings_name in self.settings:
            settings_value = getattr(self, settings_name)
            if isinstance(settings_value, GlobalSettings):
                options.update(settings_value.as_template_reader_dict())
            else:
                options[settings_name] = settings_value
        return options
