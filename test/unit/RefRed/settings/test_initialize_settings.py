# package imports
from RefRed.settings.initialize_settings import InitializeSettings
from RefRed.settings.list_settings import ListSettings

# third party packages
import pytest
import unittest.mock as mock


class TestInitializeSettings(object):
    gui_metadata = {}

    def test_initialize_default_settings(self):
        InitializeSettings(self)
        assert ListSettings() == self.gui_metadata

    @mock.patch("qtpy.QtCore.QSettings.value")
    def test_initialize_qsettings(self, mockValueMethod):
        values = {
            'q_min': 1.005,
            'd_q0': 1.0004,
            'dq_over_q': 1.005,
            'tof_bin': 41,
            'q_bin': 1.01,
            'clocking_pixel': '1121, 1197',
            'angle_offset': 1.016,
            'angle_offset_error': 1.001,
        }

        def side_effect(arg):
            return values[arg]

        mockValueMethod.side_effect = side_effect
        InitializeSettings(self)
        mockValueMethod.assert_has_calls([mock.call(k) for k in values.keys()])
        for k in values.keys():
            if k != "clocking_pixel":
                assert self.gui_metadata[k] == values[k]
            else:
                assert self.gui_metadata[k] == [1121, 1197]


if __name__ == '__main__':
    pytest.main([__file__])
