# package imports
from RefRed.settings.initialize_settings import InitializeSettings

# third party packages
import pytest
import unittest.mock as mock


class TestInitializeSettings(object):
    gui_metadata = {}

    def test_initialize_default_settings(self):
        InitializeSettings(self)
        assert len(self.gui_metadata) > 0
        assert self.gui_metadata['q_min'] == 0.005
        assert self.gui_metadata['d_q0'] == 0.0004
        assert self.gui_metadata['dq_over_q'] == 0.005
        assert self.gui_metadata['tof_bin'] == 40  # micros
        assert self.gui_metadata['q_bin'] == 0.01  # logarithmic binning
        assert self.gui_metadata['clocking_pixel'] == [121, 197]
        assert self.gui_metadata['angle_offset'] == 0.016
        assert self.gui_metadata['angle_offset_error'] == 0.001

    @mock.patch("qtpy.QtCore.QSettings.value")
    def test_initialize_qsettings(self, mockValueMethod):
        values = {'q_min': 1.005,
                  'd_q0': 1.0004,
                  'dq_over_q': 1.005,
                  'tof_bin': 41,
                  'q_bin': 1.01,
                  'clocking_pixel': '1121, 1197',
                  'angle_offset': 1.016,
                  'angle_offset_error': 1.001}

        def side_effect(arg):
            return values[arg]
        mockValueMethod.side_effect = side_effect
        InitializeSettings(self)
        mockValueMethod.assert_has_calls([mock.call(k) for k in values.keys()])
        for k in values.keys():
            if k != 'clocking_pixel':
                assert self.gui_metadata[k] == values[k]
            else:
                assert self.gui_metadata[k] == [1121, 1197]


if __name__ == '__main__':
    pytest.main([__file__])
