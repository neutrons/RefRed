import os
from pathlib import Path

import pytest

from refred.configuration.loading_configuration import LoadingConfiguration
from refred.main import MainGui

wait = 1000


@pytest.mark.parametrize(
    "case",
    [
        {
            "conf": "REF_L_188298_auto_template.xml",
            "expected_angle_offset": "0.01",
        }
    ],
)
def test_angle_offset_from_config(qtbot, tmp_path, data_server, case):
    """Test that the angle offset UI element shows the correct value after loading a configuration file."""
    # Set the current working directory as the root of the repo
    os.chdir(Path(data_server.directory).parent.parent)

    window = MainGui()
    qtbot.addWidget(window)

    # Load the configuration file
    loader = LoadingConfiguration(parent=window)
    loader.check_config_file(data_server.path_to(case["conf"]))
    loader.loading()

    qtbot.wait(wait)

    # Assert that the angle offset value matches expected
    actual_angle_offset = window.ui.angleOffsetValue.text()
    assert actual_angle_offset == case["expected_angle_offset"], (
        f"Expected angle offset '{case['expected_angle_offset']}', but got '{actual_angle_offset}'"
    )
