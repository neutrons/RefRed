from qtpy.QtCore import QSettings  # type: ignore
from RefRed import ORGANIZATION, APPNAME
from RefRed.settings.list_settings import ListSettings


class InitializeSettings(object):
    def __init__(self, parent=None, qsettings=None):
        self.parent = parent

        o_list_settings = ListSettings()

        if qsettings:
            _settings = qsettings
        else:  # load from filesystem
            _settings = QSettings(ORGANIZATION, APPNAME)

        _gui_metadata = {}
        for _key in list(o_list_settings.__dict__.keys()):
            _gui_metadata[_key] = self.__getValue(_key, o_list_settings, _settings)

        self.parent.gui_metadata = _gui_metadata

    def __getValue(self, key: str, lsettings, qsettings):
        # default value
        value = lsettings.__dict__[key]
        # value from qsettings
        if qsettings.contains(key):
            _value = str(qsettings.value(key) or '').strip()
            if _value:
                value = _value

            # convert to correct primative type
            value = float(value)

        return value
