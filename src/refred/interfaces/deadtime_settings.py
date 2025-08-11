from typing import Any, Callable, Dict
from xml.dom.minidom import Document, Element

from qtpy.QtWidgets import QDialog, QWidget

from refred.configuration.global_settings import GlobalSettings
from refred.interfaces import load_ui
from refred.utilities import str2bool


class DeadTimeSettingsModel(GlobalSettings):
    r"""Stores all options for the dead time correction. These are global options"""

    # pydantic fields
    apply_deadtime: bool = False
    paralyzable: bool = True
    dead_time: float = 4.2
    tof_step: float = 150.0

    # class variable, translates fields to XML tag names, same names as the lr_reduction package
    _to_xmltag = {
        "apply_deadtime": "dead_time_correction",
        "paralyzable": "dead_time_paralyzable",
        "dead_time": "dead_time_value",
        "tof_step": "dead_time_tof_step",
    }

    def to_xml(self, indent: str = "") -> str:
        r"""Serialize the settings to XML format.

        XML tags names are those expected by lr_reduction.reduction_template_reader.from_xml()

        Parameters
        ----------
        indent: str
            Prefix to prepend each line of XML. Typically, a certain number of spaces

        Example
        -------
        One example of the expected output by this method would look like:
        <dead_time_correction>True</dead_time_correction>
        <dead_time_paralyzable>True</dead_time_paralyzable>
        <dead_time_value>4.2</dead_time_value>
        <dead_time_tof_step>150</dead_time_tof_step>
        """
        doc: Document = Document()
        xml = ""
        for field, value in self.model_dump().items():
            child: Element = doc.createElement(self._to_xmltag[field])
            child.appendChild(doc.createTextNode(str(value)))
            xml += f"{indent}{child.toxml()}\n"
        return xml

    def from_xml(self, node: Element):
        r"""Update the settings from the contents of an XML element

        If the XMl element is missing one (or more) setting, the setting(s) are not updated except for
        field `apply_deadtime`, which is set to `False.
        XML tag names name are same as those produced by lr_reduction.reduction_template_reader.to_xml()

        Example
        -------
        A valid input XML element would look like:
        <refred>
            <some_entry1>value1</some_entry1>
            <some_entry2>value2</some_entry2>
            <dead_time_correction>True</dead_time_correction>
            <dead_time_paralyzable>True</dead_time_paralyzable>
            <dead_time_value>4.2</dead_time_value>
            <dead_time_tof_step>150</dead_time_tof_step>
            <some_entry3>value3</some_entry3>
        </refred>
        """
        # cast each value (of type `str`) to the type appropriate to the corresponding pydantic field
        converters: Dict[str, Callable[[str], Any]] = {
            "apply_deadtime": str2bool,
            "paralyzable": str2bool,
            "dead_time": float,
            "tof_step": float,
        }
        for field, converter in converters.items():
            tmp: list = node.getElementsByTagName(self._to_xmltag[field])
            if len(tmp):
                value = tmp[0].childNodes[0].nodeValue
                setattr(self, field, converter(value))
            elif field == "apply_deadtime":
                # old XML files don't have dead time info, so we make sure it's not used.
                setattr(self, "apply_deadtime", False)
        return self

    def as_template_reader_dict(self) -> Dict[str, Any]:
        r"""Save the settings as a dictionary that can be understood by
        lr_reduction.reduction_template_reader.from_dict()
        """
        # The values in this dictionary are attribute names of instances of
        # class lr_reduction.reduction_template_reader.ReductionParameters
        _to_reader_key = {
            "apply_deadtime": "dead_time",
            "paralyzable": "paralyzable",
            "dead_time": "dead_time_value",
            "tof_step": "dead_time_tof_step",
        }
        return {_to_reader_key[field]: value for field, value in self.model_dump().items()}


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

    def get_state_from_form(self) -> dict:
        r"""Read the options from the form.

        Returns
        -------
        Dictionary whose keys must match fields of class `DeadTimeSettingsModel`
        """
        return {
            "paralyzable": self.ui.use_paralyzable.isChecked(),
            "dead_time": self.ui.dead_time_value.value(),
            "tof_step": self.ui.dead_time_tof.value(),
        }

    def accept(self):
        """
        Read in the options on the form when the OK button is clicked.
        """
        self.options = self.get_state_from_form()
        self.close()
