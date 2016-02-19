from PyQt4.QtCore import QSettings
from RefRed.settings.list_settings import ListSettings


class InitializeSettings(object):
    
    list_key = []
    
    def __init__(self, parent=None):
        self.parent = parent
        
        o_list_settings = ListSettings()
        _list_keys = o_list_settings.__dict__.keys()
        
        _settings = QSettings()
        _gui_metadata = {}
        for _key in _list_keys:
            _value = str(_settings.value(_key).toString())
            if _value == '':
                _value = o_list_settings.__dict__[_key]
                _gui_metadata[_key] = _value
        self.parent.gui_metadata = _gui_metadata