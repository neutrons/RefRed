# third-party imports
from qtpy.QtWidgets import QDialog, QWidget

# RefRed imports
from RefRed.configuration.global_settings import GlobalSettings
from RefRed.interfaces import load_ui


class DeadTimeSettingsModel(GlobalSettings):
    r"""Stores all options for the dead time correction. These are global options

    Examples of Use:

    settings.to_xml() output:
        <apply_deadtime>True</apply_deadtime>
        <paralyzable>True</paralyzable>
        <dead_time>4.2</dead_time>
        <tof_step>150</tof_step>

    Input to settings.from_xml():
        <RefRed>
            <some_entry1>value1</some_entry1>
            <some_entry2>value2</some_entry2>
            <apply_deadtime>True</apply_deadtime>
            <paralyzable>True</paralyzable>
            <dead_time>4.2</dead_time>
            <tof_step>150</tof_step>
            <some_entry3>value3</some_entry3>
        </RefRed>
    """
    apply_deadtime: bool = True
    paralyzable: bool = True
    dead_time: float = 4.2
    tof_step: int = 150


class DeadTimeSettingsView(QDialog):
    """
    Dialog to choose the dead time correction options.
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = load_ui(ui_filename="deadtime_settings.ui", baseinstance=self)
        self.options = self.get_state_from_form()

    def set_state(self, paralyzable, dead_time, tof_step):
        """
        Store options and populate the form
        :param apply_correction: If True, dead time correction will be applied
        :param paralyzable: If True, a paralyzable correction will be used
        :param dead_time: Value of the dead time in micro second
        :param tof_step: TOF binning in micro second
        """
        self.ui.use_paralyzable.setChecked(paralyzable)
        self.ui.dead_time_value.setValue(dead_time)
        self.ui.dead_time_tof.setValue(tof_step)
        self.options = self.get_state_from_form()

    def get_state_from_form(self):
        """
        Read the options from the form.
        """
        options = {}
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
