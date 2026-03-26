from unittest.mock import MagicMock

import pytest

from refred.gui_handling.first_angle_range_gui_handler import NormalizationOrStitchingButtonStatus


@pytest.mark.parametrize(
    "activated_button, expected_enabled",
    [
        (0, False),  # Absolute Normalization → checkbox disabled
        (1, True),  # Auto. Stitching       → checkbox enabled
        (2, False),  # Manual Stitching      → checkbox disabled
    ],
)
def test_normalize_first_angle_checkbox_enabled_state(activated_button, expected_enabled):
    """normalize_first_angle_checkbox is enabled only when Auto. Stitching is selected."""
    parent = MagicMock()
    handler = NormalizationOrStitchingButtonStatus(parent=parent)
    handler.setWidget(activated_button=activated_button)
    parent.ui.normalize_first_angle_checkbox.setEnabled.assert_called_with(expected_enabled)
