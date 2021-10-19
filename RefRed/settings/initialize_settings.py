from qtpy.QtCore import QSettings
from RefRed.settings.list_settings import ListSettings


class InitializeSettings(object):

    list_key = []

    def __init__(self, parent=None):
        self.parent = parent

        o_list_settings = ListSettings()
        _list_keys = list(o_list_settings.__dict__.keys())

        _settings = QSettings()
        _gui_metadata = {}
        for _key in _list_keys:
            if _key == 'clocking_pixel':
                _value = str(_settings.value(_key))
                if _value in ['', 'None']:
                    _value = o_list_settings.__dict__[_key]
                else:
                    [px1, px2] = _value.split(",")
                    _value = [int(px1), int(px2)]
            else:
                _value = str(_settings.value(_key))
                if _value in ['', 'None']:
                    _value = o_list_settings.__dict__[_key]
                else:
                    _value = float(_value)
            _gui_metadata[_key] = _value

        self.parent.gui_metadata = _gui_metadata
