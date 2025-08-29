from dataclasses import dataclass
from typing import Any, Callable, Dict
from xml.dom.minidom import Document, Element

from qtpy.QtWidgets import (
    QCheckBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from refred.configuration.global_settings import GlobalSettings
from refred.interfaces import load_ui
from refred.utilities import str2bool


@dataclass
class DEFAULT_INSTRUMENT_SETTINGS:  # noqa: N801
    apply_instrument_settings: bool = False
    source_detector_distance: float = 15.75
    sample_detector_distance: float = 1.83
    num_x_pixels: int = 256
    num_y_pixels: int = 304
    pixel_width: float = 0.70
    xi_reference: float = 445
    s1_sample_distance: float = 1.485
    wavelength_resolution_dLambda_formula: str = "L - A * exp(-k * x)"
    wavelength_resolution_initial_parameters: str = "L=0.07564423, A=0.13093263, k=0.34918918"


class InstrumentSettingsEntryPoint(QGroupBox):
    def __init__(self, title="Instrument Settings"):
        super().__init__(title)
        self.initUI()

    def initUI(self):
        # Set the stylesheet for the group box to have a border
        self.setStyleSheet(
            "QGroupBox {"
            "  border: 1px solid gray;"
            "  border-radius: 5px;"
            "  margin-top: 1ex;"  # space above the group box
            "} "
            "QGroupBox::title {"
            "  subcontrol-origin: margin;"
            "  subcontrol-position: top center;"  # align the title to the center
            "  padding: 0 3px;"
            "}"
        )

        self.applyCheckBox = QCheckBox("Apply", self)
        self.applyCheckBox.stateChanged.connect(self.toggleSettingsButton)
        self.settingsButton = QPushButton("Settings", self)
        self.settingsButton.setEnabled(self.applyCheckBox.isChecked())

        # Create a horizontal layout for the checkbox and settings button
        hbox = QHBoxLayout()
        hbox.addWidget(self.applyCheckBox)
        hbox.addWidget(self.settingsButton)

        # Set the layout for the group box
        self.setLayout(hbox)

    def toggleSettingsButton(self, state):
        # Enable the settings button if the checkbox is checked, disable otherwise
        self.settingsButton.setEnabled(state)


class InstrumentSettingsDialog(QDialog):
    """
    Dialog to specify instrument geometry parameters.
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = load_ui(ui_filename="instrument_settings.ui", baseinstance=self)
        self.options = self.get_state_from_form()

    def set_state(
        self,
        # apply_instrument_settings,
        source_detector_distance,
        sample_detector_distance,
        num_x_pixels,
        num_y_pixels,
        pixel_width,
        xi_reference,
        s1_sample_distance,
        wavelength_resolution_dLambda_formula,
        wavelength_resolution_initial_parameters,
    ):
        """
        Store options and populate the form

        :param source_detector_distance: Source to detector distance in meters
        :param sample_detector_distance: Sample to detector distance in meters
        :param num_x_pixels: Number of pixels in the x direction
        :param num_y_pixels: Number of pixels in the y direction
        :param pixel_width: Pixel width in mm
        :param xi_reference: Reference xi value in mm
        :param s1_sample_distance: S1 to sample distance in meters
        :param wavelength_resolution_dLambda_formula: The formula used to calculate the wavelength resolution
        :param wavelength_resolution_initial_parameters: The parameters used to calculate the wavelength resolution
        """
        self.ui.source_detector_distance.setValue(source_detector_distance)
        self.ui.sample_detector_distance.setValue(sample_detector_distance)
        self.ui.num_x_pixels.setValue(num_x_pixels)
        self.ui.num_y_pixels.setValue(num_y_pixels)
        self.ui.pixel_width.setValue(pixel_width)
        self.ui.xi_reference.setValue(xi_reference)
        self.ui.s1_sample_distance.setValue(s1_sample_distance)
        self.ui.wavelength_resolution_dLambda_formula.setText(wavelength_resolution_dLambda_formula)
        self.ui.wavelength_resolution_initial_parameters.setText(wavelength_resolution_initial_parameters)
        self.options = self.get_state_from_form()

    def get_state_from_form(self) -> dict:
        r"""Read the options from the form.

        Returns
        -------
        Dictionary whose keys must match fields of class `InstrumentSettings`
        """
        return {
            "source_detector_distance": self.ui.source_detector_distance.value(),
            "sample_detector_distance": self.ui.sample_detector_distance.value(),
            "num_x_pixels": self.ui.num_x_pixels.value(),
            "num_y_pixels": self.ui.num_y_pixels.value(),
            "pixel_width": self.ui.pixel_width.value(),
            "xi_reference": self.ui.xi_reference.value(),
            "s1_sample_distance": self.ui.s1_sample_distance.value(),
            "wavelength_resolution_dLambda_formula": self.ui.wavelength_resolution_dLambda_formula.text(),
            "wavelength_resolution_initial_parameters": self.ui.wavelength_resolution_initial_parameters.text(),
        }

    def accept(self):
        """
        Read in the options on the form when the OK button is clicked.
        """
        self.options = self.get_state_from_form()
        self.close()


class InstrumentSettings(GlobalSettings):
    """Dataclass to store instrument geometry parameters. These are global options

    Default values are determined by settings.json from lr_reduction
    """

    # pydantic fields
    apply_instrument_settings: bool = DEFAULT_INSTRUMENT_SETTINGS.apply_instrument_settings
    source_detector_distance: float = DEFAULT_INSTRUMENT_SETTINGS.source_detector_distance
    sample_detector_distance: float = DEFAULT_INSTRUMENT_SETTINGS.sample_detector_distance
    num_x_pixels: int = DEFAULT_INSTRUMENT_SETTINGS.num_x_pixels
    num_y_pixels: int = DEFAULT_INSTRUMENT_SETTINGS.num_y_pixels
    pixel_width: float = DEFAULT_INSTRUMENT_SETTINGS.pixel_width
    xi_reference: float = DEFAULT_INSTRUMENT_SETTINGS.xi_reference
    s1_sample_distance: float = DEFAULT_INSTRUMENT_SETTINGS.s1_sample_distance
    wavelength_resolution_dLambda_formula: str = DEFAULT_INSTRUMENT_SETTINGS.wavelength_resolution_dLambda_formula
    wavelength_resolution_initial_parameters: str = DEFAULT_INSTRUMENT_SETTINGS.wavelength_resolution_initial_parameters

    # class variable, translates fields to XML tag names, same names as the lr_reduction package
    def to_xml(self, indent: str = "") -> str:
        r"""Convert the settings to an XML string

        The XML tag names are same as those used by lr_reduction.reduction_template_reader.to_xml()

        Example
        -------
        The XML string would look like:
        <refred>
            <some_entry1>value1</some_entry1>
            <some_entry2>value2</some_entry2>
            <some_entry3>value3</some_entry3>
        </refred>
        """
        doc: Document = Document()
        xml = ""
        for field, value in self.model_dump().items():
            child: Element = doc.createElement(field)
            child.appendChild(doc.createTextNode(str(value)))
            xml += f"{indent}{child.toxml()}\n"
        return xml

    def from_xml(self, node: Element):
        r"""
        Update the settings from the contents of an XML element
        XML tag names name are same as those produced by lr_reduction.reduction_template_reader.to_xml()

        Example
        -------
        A valid input XML element would look like:
        <refred>
            <some_entry1>value1</some_entry1>
            <some_entry2>value2</some_entry2>
            <some_entry3>value3</some_entry3>
        </refred>
        """
        # cast each value (of type `str`) to the type appropriate to the corresponding pydantic field
        converters: Dict[str, Callable[[str], Any]] = {
            "apply_instrument_settings": str2bool,
            "source_detector_distance": float,
            "sample_detector_distance": float,
            "num_x_pixels": int,
            "num_y_pixels": int,
            "pixel_width": float,
            "xi_reference": float,
            "s1_sample_distance": float,
            "wavelength_resolution_dLambda_formula": str,
            "wavelength_resolution_initial_parameters": str,
        }
        for field, converter in converters.items():
            tmp: list = node.getElementsByTagName(field)
            if len(tmp):
                value = tmp[0].childNodes[0].nodeValue
                setattr(self, field, converter(value))
            else:
                # if the field is not found in the XML, we use the default value
                setattr(self, field, DEFAULT_INSTRUMENT_SETTINGS.__dict__[field])

        return self

    def as_template_reader_dict(self) -> Dict[str, Any]:
        r"""Save the settings as a dictionary for lr_reduction.reduction_template_reader.from_dict()"""
        return self.model_dump()
