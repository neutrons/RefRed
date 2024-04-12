from qtpy.QtWidgets import QDialog, QWidget

from RefRed.interfaces import load_ui


class DeadTimeSettingsView(QDialog):
    """
    Dialog to choose the dead time correction options.
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = load_ui(ui_filename="deadtime_settings.ui", baseinstance=self)
        self.options = self.get_state_from_form()

    def set_state(self, apply_correction, paralyzable, dead_time, tof_step):
        """
        Store options and populate the form
        :param apply_correction: If True, dead time correction will be applied
        :param paralyzable: If True, a paralyzable correction will be used
        :param dead_time: Value of the dead time in micro second
        :param tof_step: TOF binning in micro second
        """
        self.ui.apply_correction.setChecked(apply_correction)
        self.ui.use_paralyzable.setChecked(paralyzable)
        self.ui.dead_time_value.setValue(dead_time)
        self.ui.dead_time_tof.setValue(tof_step)
        self.options = self.get_state_from_form()

    def get_state_from_form(self):
        """
        Read the options from the form.
        """
        options = {}
        options['apply_correction'] = self.ui.apply_correction.isChecked()
        options['paralyzable'] = self.ui.use_paralyzable.isChecked()
        options['dead_time'] = self.ui.dead_time_value.value()
        options['tof_step'] = self.ui.dead_time_tof.value()
        return options

    def accept(self):
        """
        Read in the options on the form when the OK button is
        clicked.
        """
        self.options = self.get_state_from_form()
        self.close()
