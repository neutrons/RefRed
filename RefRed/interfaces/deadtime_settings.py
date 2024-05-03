# standard imports
from xml.dom.minidom import Document, Element

# third-party imports
from qtpy.QtWidgets import QDialog, QWidget
from pydantic import BaseModel

# RefRed imports
from RefRed.interfaces import load_ui
from RefRed.utilities import str2bool


class DeadTimeSettingsModel(BaseModel):
    apply_deadtime: bool = True
    paralyzable: bool = True
    dead_time: float = 4.2
    tof_step: int = 150

    def to_xml(self) -> str:
        r"""Serialize the dead time settings to XML format"""
        doc = Document()  # Create a new XML document

        def _to_xml(field: str) -> str:
            r"""Serialize one of the dead time settings to XML format"""
            element = doc.createElement(field)
            element_text = doc.createTextNode(str(getattr(self, field)))
            element.appendChild(element_text)
            return element.toxml()

        return "\n".join([_to_xml(field) for field in self.dict()])

    def from_xml(self, node: Element):
        r"""Update the dead time settings from the contents of an XML element

        If the XMl element is missing one (or more) setting, the setting(s) are not updated
        """
        converters = {"apply_deadtime": str2bool, "paralyzable": str2bool, "dead_time": float, "tof_step": int}
        for field, converter in converters.items():
            tmp: list = node.getElementsByTagName(field)
            if len(tmp):
                value = tmp[0].childNodes[0].nodeValue
                setattr(self, field, converter(value))
        return self


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
