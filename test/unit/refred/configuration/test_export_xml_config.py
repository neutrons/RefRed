from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from refred.configuration.export_xml_config import ExportXMLConfig


def _make_config_with_mock_gui(stitching_type="manual"):
    """Helper: return an ExportXMLConfig whose GuiUtility returns the given stitching_type."""
    parent = MagicMock()
    config = ExportXMLConfig(parent)
    # Patch GuiUtility used inside main_part
    config._gui_stitching_type = stitching_type
    return config


class TestExportXMLConfig:
    @patch("refred.configuration.export_xml_config.refred")
    @patch("refred.configuration.export_xml_config.mantid")
    def test_header_part(self, mantid_mock, refred_mock):
        refred_mock.__version__ = "2.0.0"
        mantid_mock.__version__ = "1.0.0"
        config = ExportXMLConfig(MagicMock())
        config.header_part()
        assert len(config.str_array) == 7
        header = "".join(config.str_array)
        assert datetime.now().strftime("%A, %d. %B %Y %I:%M%p") in header
        assert "<mantid_version>1.0.0</mantid_version>" in header
        assert "<generator>refred-2.0.0</generator>" in header

    @patch("refred.configuration.export_xml_config.GuiUtility")
    def test_main_part(self, mock_gui_utility):
        mock_gui_utility.return_value.getStitchingType.return_value = "manual"
        parent = MagicMock()
        parent.ui.normalize_first_angle_checkbox.isChecked.return_value = True
        config = ExportXMLConfig(parent)
        config.main_part()
        assert len(config.str_array) == 61

    @pytest.mark.parametrize("checked, expected_xml_value", [(True, "True"), (False, "False")])
    @patch("refred.configuration.export_xml_config.GuiUtility")
    def test_main_part_normalize_first_angle(self, mock_gui_utility, checked, expected_xml_value):
        """normalize_first_angle XML tag reflects the checkbox state."""
        mock_gui_utility.return_value.getStitchingType.return_value = "manual"
        parent = MagicMock()
        parent.ui.normalize_first_angle_checkbox.isChecked.return_value = checked
        config = ExportXMLConfig(parent)
        config.main_part()
        xml = "".join(s for s in config.str_array if isinstance(s, str))
        assert f"<normalize_first_angle>{expected_xml_value}</normalize_first_angle>" in xml

    @pytest.mark.parametrize(
        "stitching_type, expected_xml_value",
        [
            ("absolute", "AbsoluteNormalization"),
            ("auto", "AutomaticAverage"),
            ("manual", "None"),
        ],
    )
    @patch("refred.configuration.export_xml_config.GuiUtility")
    def test_main_part_stitching_type_tag(self, mock_gui_utility, stitching_type, expected_xml_value):
        mock_gui_utility.return_value.getStitchingType.return_value = stitching_type
        parent = MagicMock()
        parent.deadtime_settings.to_xml.return_value = ""
        parent.instrument_settings.to_xml.return_value = ""
        config = ExportXMLConfig(parent)
        config.main_part()
        xml = "".join(s for s in config.str_array if isinstance(s, str))
        assert f"<stitching_type>{expected_xml_value}</stitching_type>" in xml

    @pytest.mark.parametrize(
        "stitching_type, sf_field, sf_value",
        [
            ("absolute", "sf_abs_normalization", 2.5),
            ("auto", "sf_auto", 3.14),
            ("manual", "sf_manual", 0.75),
        ],
    )
    @patch("refred.configuration.export_xml_config.GuiUtility")
    def test_main_part_stitching_sf_from_lconfig(self, mock_gui_utility, stitching_type, sf_field, sf_value):
        """The per-row scale factor tag reflects the correct sf_* field on lconfig."""
        mock_gui_utility.return_value.getStitchingType.return_value = stitching_type

        parent = MagicMock()
        parent.deadtime_settings.to_xml.return_value = ""
        parent.instrument_settings.to_xml.return_value = ""

        lconfig = MagicMock()
        setattr(lconfig, sf_field, sf_value)

        def _getitem(key):
            row, col = key
            return lconfig if col == 2 else MagicMock()

        parent.big_table_data.__getitem__.side_effect = _getitem

        config = ExportXMLConfig(parent)
        config.main_part()
        xml = "".join(s for s in config.str_array if isinstance(s, str))
        assert f"<stitching_reflectivity_scale_factor>{sf_value}</stitching_reflectivity_scale_factor>" in xml

    @patch("refred.configuration.export_xml_config.GuiUtility")
    def test_main_part_stitching_sf_fallback_when_lconfig_none(self, mock_gui_utility):
        """When big_table_data[row, 2] is None the scale factor falls back to 1.0."""
        mock_gui_utility.return_value.getStitchingType.return_value = "manual"

        parent = MagicMock()
        parent.deadtime_settings.to_xml.return_value = ""
        parent.instrument_settings.to_xml.return_value = ""

        def _getitem(key):
            row, col = key
            return None if col == 2 else MagicMock()

        parent.big_table_data.__getitem__.side_effect = _getitem

        config = ExportXMLConfig(parent)
        config.main_part()
        xml = "".join(s for s in config.str_array if isinstance(s, str))
        assert "<stitching_reflectivity_scale_factor>1.0</stitching_reflectivity_scale_factor>" in xml


if __name__ == "__main__":
    pytest.main()
