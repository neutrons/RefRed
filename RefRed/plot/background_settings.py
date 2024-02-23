# standard imports
from typing import List, Optional, Tuple

# third-party imports
from qtpy.QtCore import Qt, QObject, Signal  # type: ignore
from qtpy.QtWidgets import QDialog, QCheckBox, QWidget

# application imports
from RefRed.calculations.lr_data import LRData
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.interfaces import load_ui
from RefRed.tabledata import TableData


class BackgroundSettingsModel(QObject):
    signal_first_background = Signal(bool)
    signal_second_background = Signal(bool)
    signal_functional_background = Signal(bool)
    signal_two_backgrounds = Signal(bool)

    def __init__(self):
        super(BackgroundSettingsModel, self).__init__()
        self._subtract_background = True
        self._functional_background = False
        self._two_backgrounds = False
        self.maingui = None

    @property
    def subtract_background(self) -> bool:
        return self._subtract_background

    @subtract_background.setter
    def subtract_background(self, value: bool):
        self._subtract_background = value
        self.signal_first_background.emit(value)
        self.signal_second_background.emit(value and self.two_backgrounds)

    @property
    def functional_background(self) -> bool:
        return self._functional_background

    @functional_background.setter
    def functional_background(self, value: bool):
        self._functional_background = value
        self.signal_functional_background.emit(value)

    @property
    def two_backgrounds(self) -> bool:
        return self._two_backgrounds

    @two_backgrounds.setter
    def two_backgrounds(self, value: bool):
        self._two_backgrounds = value
        self.signal_two_backgrounds.emit(value)
        self.signal_second_background.emit(self.subtract_background and value)

    def update_all_settings(
        self, subtract_background: bool = True, functional_background: bool = False, two_backgrounds: bool = False
    ):
        self.subtract_background = subtract_background
        self.functional_background = functional_background
        self.two_backgrounds = two_backgrounds

    def set_spinbox_visibilities(self, parent: QWidget, first_background: Tuple[str], second_background: Tuple[str]):
        for spinbox in first_background:
            getattr(parent, spinbox).setEnabled(self.subtract_background)
        for spinbox in second_background:
            getattr(parent, spinbox).setEnabled(self.subtract_background and self.two_backgrounds)

    def control_spinboxes_visibility(
        self, parent: QWidget, first_background: Tuple[str], second_background: Tuple[str]
    ):
        self.set_spinbox_visibilities(parent, first_background, second_background)
        for spinbox in first_background:
            slot = getattr(parent, spinbox).setEnabled
            self.signal_first_background.connect(slot)
        for spinbox in second_background:
            slot = getattr(parent, spinbox).setEnabled
            self.signal_second_background.connect(slot)

    def emit_backgrounds_state(self):
        r"""Emit signals corresponding to whether the first and/or second backgrounds are active"""
        self.signal_first_background.emit(self.subtract_background)
        self.signal_second_background.emit(self.subtract_background and self.two_backgrounds)


class CompositeBackgroundSettings:
    _instance = None
    r"""Singleton class storing settings for the backgrounds of the reflectivity and direct-beam runs
    currently selected in the reduction table

    Responsibilities:
    1. Automatically updates the background settings stored for the currently selected row of data structure
       `big_table_data` whenever User modifies any background settings.
    2. Automatically updates the the visibility of the different spinboxes than control the lower and upper
       boundaries for the two backgrounds (either for reflectivity or normalization data)
    3. Automatically updates itself when the user clicks on a different row in the reduction table.
    """

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CompositeBackgroundSettings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.data = BackgroundSettingsModel()
        self.norm = BackgroundSettingsModel()
        self.maingui: Optional[QObject] = None

    def __getitem__(self, key):
        if key == 'data':
            return self.data
        elif key == 'norm':
            return self.norm
        else:
            raise KeyError(f"No attribute with key '{key}' found in CompositeBackgroundSettings")

    def set_maingui(self, maingui):
        self.maingui = maingui
        self._initialize_reduction_table_updaters()

    def update_from_table(self, active_row_index: int, is_data: bool):
        r"""Update all background settings for the reflectivity or normalization data with  the`LRData`
        instances from the currently active row in the reduction table.

        Parameters
        ----------
        active_row_index
            Currently selected row in the reduction table
        is_data
            Update background settings for the reflectivity (True) or normalization (False) data
        """
        if self.maingui is None:
            return RuntimeError("MainGui unitialized in CompositeBackgroundSettings")
        data_fetcher = {
            True: self.maingui.big_table_data.reflectometry_data,
            False: self.maingui.big_table_data.normalization_data,
        }
        data: LRData = data_fetcher[is_data](active_row_index)
        if data is None:  # the active row in the reduction table has no reflectivity and/or direct-beam data
            return
        updater = {True: self.data.update_all_settings, False: self.norm.update_all_settings}
        updater[is_data](data.back_flag, data.functional_background, data.two_backgrounds)

    def table_updater_factory(self, setting: str, data_type: str):
        r"""Generate anonymous functions to serve as callback when any of the background settings
        are updated either for the reflectivity or normalization `LRData` instances for the currently active
        row in the reduction table.

        Each callback will be associated to one background setting. Upon invoked, `big_table_data` will be
        updated with the new value of the background setting.

        Parameters
        ----------
        setting
            the background setting in `big_table` to update. One of `back_flag`, `functional_background`,
            `two_backgrounds`
        data_type
            whether to update the reflectivity or the normalization `LRData` instances for the currently active
            row in the reduction table
        Returns
        -------

        """

        def table_updater(value: bool):
            if self.maingui is None:
                return RuntimeError("MainGui unitialized in CompositeBackgroundSettings")
            gui_utility = GuiUtility(parent=self.maingui)
            # Find the active row in the reduction table
            active_row_index = gui_utility.get_current_table_reduction_check_box_checked()
            if active_row_index == gui_utility.NULL_ACTIVE_ROW:  # no active row
                return
            # find all indexes in the table for rows having the same run number as that stored in
            # row `active_row_index` for reflectometry data (is_data==True) there can be only one row
            is_data = True if data_type == "data" else False
            all_rows: List[int] = gui_utility.get_other_row_with_same_run_number_as_row(
                row=active_row_index, is_data=is_data
            )
            big_table_data: TableData = self.maingui.big_table_data
            for row_index in all_rows:
                if is_data:
                    data: Optional[LRData] = big_table_data.reflectometry_data(row_index)
                else:
                    data = big_table_data.normalization_data(row_index)
                assert data is not None
                setattr(data, setting, value)

        return table_updater

    def _initialize_reduction_table_updaters(self):
        r"""Create a set of callbacks in charge of updating the background settings for the active row
        in `big_table_data` whenever any of the background settings values are updated, either in the
        `data` or `norm` BackgroundSettingsModel instances.
        """
        # names of some of the signals emitted by self.data and self.norm
        signal_names = ["signal_first_background", "signal_functional_background", "signal_two_backgrounds"]
        # names of the background settings attributes in the LRData instaces of `big_table_data`
        setting_names = ["back_flag", "functional_background", "two_backgrounds"]
        # connect the signals to dedicated slots that will update the LRData instances
        for signal_name, setting_name in zip(signal_names, setting_names):
            signal = getattr(self.data, signal_name)
            signal.connect(self.table_updater_factory(setting_name, data_type="data"))
            signal = getattr(self.norm, signal_name)
            signal.connect(self.table_updater_factory(setting_name, data_type="norm"))


backgrounds_settings = CompositeBackgroundSettings()  # singleton instance


class BackgroundSettingsView(QDialog):

    # checkbox names as well as names for the model properties
    options = ["subtract_background", "functional_background", "two_backgrounds"]

    def __init__(self, parent: QWidget, run_type="data"):
        super().__init__(parent)
        self.ui = load_ui(ui_filename="background_settings.ui", baseinstance=self)
        self.model = backgrounds_settings[run_type]  # fetch from the singleton model
        self._update_view()
        self._set_connections()

    def _set_connections(self):
        for box_name in ["subtract_background", "functional_background", "two_backgrounds"]:
            checkbox: QCheckBox = getattr(self.ui, box_name)
            # signal stateChanged emits `state`, which we pass to our anonymous `lambda`
            # `option=box_name` in effect allows us to define a different lambda` function for each checkbox
            checkbox.stateChanged.connect(lambda state, option=box_name: self._update_model(option, state))

    def _update_view(self, option: Optional[str] = None):
        r"""Fetch current boolean option(s) from the model"""
        options = self.options if option is None else [option]
        for _option in options:
            value: bool = getattr(self.model, _option)
            checkbox: QCheckBox = getattr(self.ui, _option)
            checkbox.setChecked(value)

    def _update_model(self, option: str, state) -> None:
        r"""
        Update the model with the current state of the selected checkbox

        Parameters
        ----------
        option
            the name of one of the chekboxes of the dialog
        state
            the state of the checkbox (either clicked or unclicked)
        """
        setattr(self.model, option, state == Qt.Checked)
