from xml.dom.minidom import parseString

import pytest
from qtpy.QtCore import Qt  # type: ignore

from refred.interfaces.instrument_settings import InstrumentSettings, InstrumentSettingsEntryPoint

# Test the InstrumentSettingsEntryPoint


@pytest.fixture
def instrument_settings_entry_point(qtbot):
    widget = InstrumentSettingsEntryPoint()
    qtbot.addWidget(widget)
    return widget


def test_initial_state(instrument_settings_entry_point):
    assert not instrument_settings_entry_point.applyCheckBox.isChecked()
    assert not instrument_settings_entry_point.settingsButton.isEnabled()


def test_checkbox_interaction(instrument_settings_entry_point, qtbot):
    # Simulate checking the checkbox
    qtbot.mouseClick(instrument_settings_entry_point.applyCheckBox, Qt.LeftButton)
    # Test if the checkbox is checked
    assert instrument_settings_entry_point.applyCheckBox.isChecked()
    # Test if the settings button is now enabled
    assert instrument_settings_entry_point.settingsButton.isEnabled()


def test_uncheck_checkbox(instrument_settings_entry_point, qtbot):
    # First, check the checkbox
    qtbot.mouseClick(instrument_settings_entry_point.applyCheckBox, Qt.LeftButton)
    # Now, uncheck it
    qtbot.mouseClick(instrument_settings_entry_point.applyCheckBox, Qt.LeftButton)
    # Test if the checkbox is unchecked
    assert not instrument_settings_entry_point.applyCheckBox.isChecked()
    # Test if the settings button is now disabled
    assert not instrument_settings_entry_point.settingsButton.isEnabled()


# Test the InstrumentSettings Model


class TestInstrumentSettingsModel:
    custom_settings = {
        "apply_instrument_settings": True,
        "source_detector_distance": 1.0,
        "sample_detector_distance": 2.0,
        "num_x_pixels": 3,
        "num_y_pixels": 4,
        "pixel_width": 5.0,
        "xi_reference": 6.0,
        "s1_sample_distance": 7.0,
        "wavelength_resolution_dLambda_formula": "L - A * exp(-k * x)",
        "wavelength_resolution_initial_parameters": "L=8.0, A=9.0, k=10.0",
    }

    def test_initialization_with_defaults(self):
        model = InstrumentSettings()
        assert model.apply_instrument_settings is False
        assert model.source_detector_distance == 15.75
        assert model.sample_detector_distance == 1.83
        assert model.num_x_pixels == 256
        assert model.num_y_pixels == 304
        assert model.pixel_width == 0.70
        assert model.xi_reference == 445
        assert model.s1_sample_distance == 1.485
        assert model.wavelength_resolution_dLambda_formula == "L - A * exp(-k * x)"
        assert model.wavelength_resolution_initial_parameters == "L=0.07564423, A=0.13093263, k=0.34918918"

    def test_initialization_with_custom_values(self):
        model = InstrumentSettings(**self.custom_settings)
        assert model.__dict__ == self.custom_settings

    def test_to_xml(self):
        expected_xml = (
            "<apply_instrument_settings>True</apply_instrument_settings>\n"
            "<source_detector_distance>1.0</source_detector_distance>\n"
            "<sample_detector_distance>2.0</sample_detector_distance>\n"
            "<num_x_pixels>3</num_x_pixels>\n"
            "<num_y_pixels>4</num_y_pixels>\n"
            "<pixel_width>5.0</pixel_width>\n"
            "<xi_reference>6.0</xi_reference>\n"
            "<s1_sample_distance>7.0</s1_sample_distance>\n"
            "<wavelength_resolution_dLambda_formula>L - A * exp(-k * x)</wavelength_resolution_dLambda_formula>\n"  # noqa: E501
            "<wavelength_resolution_initial_parameters>L=8.0, A=9.0, k=10.0</wavelength_resolution_initial_parameters>\n"  # noqa: E501
            # noqa: E501
        )
        model = InstrumentSettings(**self.custom_settings)
        xml_output = model.to_xml()
        assert xml_output == expected_xml

    def test_from_xml(self):
        xml_input = (
            "<refred>"
            "<spurious>True</spurious>\n"
            "<apply_instrument_settings>True</apply_instrument_settings>\n"
            "<source_detector_distance>1.0</source_detector_distance>\n"
            "<sample_detector_distance>2.0</sample_detector_distance>\n"
            "<num_x_pixels>3</num_x_pixels>\n"
            "<num_y_pixels>4</num_y_pixels>\n"
            "<pixel_width>5.0</pixel_width>\n"
            "<xi_reference>6.0</xi_reference>\n"
            "<s1_sample_distance>7.0</s1_sample_distance>\n"
            "<wavelength_resolution_dLambda_formula>L - A * exp(-k * x)</wavelength_resolution_dLambda_formula>\n"  # noqa: E501
            "<wavelength_resolution_initial_parameters>L=8.0, A=9.0, k=10.0</wavelength_resolution_initial_parameters>\n"  # noqa: E501
            "<another_spurious>True</another_spurious>\n"
            "</refred>"
        )
        dom = parseString(xml_input)
        model = InstrumentSettings().from_xml(dom.documentElement)
        assert model.__dict__ == self.custom_settings


if __name__ == "__main__":
    pytest.main([__file__])
