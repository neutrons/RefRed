# package imports
from RefRed.settings.initialize_settings import InitializeSettings

# third party packages
import pytest


class TestInitializeSettings(object):
    gui_metadata = {}

    def test_initialize_settings(self):
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

if __name__ == '__main__':
    pytest.main([__file__])