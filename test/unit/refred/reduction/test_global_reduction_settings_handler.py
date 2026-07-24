from unittest.mock import MagicMock, patch

import pytest

from refred.reduction.global_reduction_settings_handler import GlobalReductionSettingsHandler


class TestGlobalReductionSettingsHandler:
    @pytest.mark.parametrize(
        "gui_stitching_type, expected_xml_value",
        [
            ("absolute", "AbsoluteNormalization"),
            ("auto", "AutomaticAverage"),
            ("manual", "None"),
        ],
    )
    @patch("refred.reduction.global_reduction_settings_handler.GuiUtility")
    def test_stitching_type_in_settings(self, mock_gui_utility_cls, gui_stitching_type, expected_xml_value):
        """stitching_type is present in settings and mapped to the correct XML value."""
        mock_gui_utility_cls.return_value.getStitchingType.return_value = gui_stitching_type

        parent = MagicMock()
        handler = GlobalReductionSettingsHandler(parent=parent)

        assert "stitching_type" in handler.settings
        assert handler.settings["stitching_type"] == expected_xml_value

    @patch("refred.reduction.global_reduction_settings_handler.GuiUtility")
    def test_stitching_type_unknown_defaults_to_none(self, mock_gui_utility_cls):
        """An unrecognized GUI stitching type maps to 'None' as a safe default."""
        mock_gui_utility_cls.return_value.getStitchingType.return_value = "unknown_type"

        parent = MagicMock()
        handler = GlobalReductionSettingsHandler(parent=parent)

        assert handler.settings["stitching_type"] == "None"


if __name__ == "__main__":
    pytest.main([__file__])
