# standard imports

# third-party imports
from qtpy.QtWidgets import QDialog, QCheckBox, QWidget

# application imports
from RefRed.interfaces import load_ui


class BackgroundSettingsModel:
    r"""Singleton class storing settings for the background

    Parameters
    ----------
    main_window
        reference to the application's main window
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            if kwargs["main_window"] is None:
                raise ValueError("A widget for `main_window` is required at first instantiation")
            cls._instance = super(BackgroundSettingsModel, cls).__new__(cls)
        return cls._instance

    def __init__(self, main_window: QWidget = None):
        self.main_window = main_window
        self._subtract_background = True
        self._functional_background = False
        self._two_backgrounds = False

    @property
    def subtract_background(self) -> bool:
        return self._subtract_background

    @subtract_background.setter
    def subtract_background(self, value: bool):
        self._subtract_background = value

    @property
    def functional_background(self) -> bool:
        return self._functional_background

    @functional_background.setter
    def functional_background(self, value: bool):
        self._functional_background = value

    @property
    def two_backgrounds(self) -> bool:
        return self._two_backgrounds

    @two_backgrounds.setter
    def two_backgrounds(self, value: bool):
        self._two_backgrounds = value


class BackgroundSettingsView(QDialog):

    # checkbox names as well as names for the model properties
    options = ["subtract_background", "functional_background", "two_backgrounds"]

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.ui = load_ui(ui_filename="background_settings.ui", baseinstance=self)
        self.model = BackgroundSettingsModel()  # fetch the singleton model
        self._update_view()

    def _update_view(self, option: str = None):
        r"""Fetch current boolean option(s) from the model"""
        options = self.options if option is None else [option]
        for _option in options:
            value: bool = getattr(self.model, _option)
            checkbox: QCheckBox = getattr(self.ui, _option)
            checkbox.setChecked(value)

    def _update_model(self, option: str) -> None:
        checkbox: QCheckBox = getattr(self.ui, option)
        value = checkbox.isChecked()  # True if checkbox is checked
        setattr(self.model, option, value)
