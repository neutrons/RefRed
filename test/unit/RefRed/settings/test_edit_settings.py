# package imports
from RefRed.settings.settings_editor import SettingsEditor
from RefRed.settings.list_settings import ListSettings

# third party packages
import pytest
import unittest.mock as mock

DEFAULT_SETTINGS = ListSettings()


class TestEditSettings(object):
    gui_metadata = {
        'q_min': DEFAULT_SETTINGS.q_min,
        'd_q0': DEFAULT_SETTINGS.d_q0,
        'dq_over_q': DEFAULT_SETTINGS.dq_over_q,
        'tof_bin': DEFAULT_SETTINGS.tof_bin,
        'q_bin': DEFAULT_SETTINGS.q_bin,
        'angle_offset': DEFAULT_SETTINGS.angle_offset,
        'angle_offset_error': DEFAULT_SETTINGS.angle_offset_error,
    }
    '''
    {'q_min': 1.005,
                  'd_q0': 1.0004,
                  'dq_over_q': 1.005,
                  'tof_bin': 41,
                  'q_bin': 1.01,
                  'angle_offset': 1.016,
                  'angle_offset_error': 1.001}
                  '''

    @mock.patch("qtpy.QtWidgets.QMainWindow.__init__")
    def test_reset_button(self, mockSuperInit):
        # create a parent widget
        parent_item = mock.Mock()
        parent_item.gui_metadata = self.gui_metadata
        # create the object to test
        editor = SettingsEditor(parent_item, loadUI=False)
        assert mockSuperInit.called
        editor.ui = mock.Mock()
        editor.populate_table()
        # modify a value
        parent_item.gui_metadata['d_q0'] = 1.0004
        assert parent_item.gui_metadata != DEFAULT_SETTINGS, "should have changed"
        # reset everything
        editor.reset_button()
        assert parent_item.gui_metadata == DEFAULT_SETTINGS, "should be identical"


if __name__ == '__main__':
    pytest.main([__file__])
