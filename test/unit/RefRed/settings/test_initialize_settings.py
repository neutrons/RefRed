# package imports
from RefRed.settings.initialize_settings import InitializeSettings
from RefRed.settings.list_settings import ListSettings
from qtpy.QtCore import QSettings  # type: ignore

# third party packages
import pytest


class SettingsContext:
    def __init__(self, suffix='', items={}):
        self.settings = QSettings('neutron', 'RefRed' + suffix)
        for key, value in items.items():
            self.settings.setValue(key, str(value))

    def __enter__(self):
        return self.settings

    def __exit__(self, type, value, traceback):
        self.settings.clear()


class TestInitializeSettings(object):
    gui_metadata = {}

    def test_initialize_default_settings(self):
        with SettingsContext('-TestInitializeSettings') as settings:
            InitializeSettings(self, settings)
            assert self.gui_metadata == ListSettings()

    def test_initialize_qsettings(self):
        values = {
            'q_min': 1.005,
            'd_q0': 1.0004,
            'dq_over_q': 1.005,
            'tof_bin': 41,
            'q_bin': 1.01,
            'angle_offset': 1.016,
            'angle_offset_error': 1.001,
        }

        with SettingsContext('-TestInitializeSettings', values) as settings:
            InitializeSettings(self, settings)
            for k in values.keys():
                assert self.gui_metadata[k] == values[k], k


if __name__ == '__main__':
    pytest.main([__file__])
