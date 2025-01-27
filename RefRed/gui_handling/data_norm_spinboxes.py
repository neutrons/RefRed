# standard imports
from typing import List

# third party imports
from qtpy.QtWidgets import QWidget

# application imports
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.plot.display_plots import DisplayPlots
from RefRed.tabledata import TableData


class SpinBox(object):
    parent = None

    def __init__(self, parent=None, is_data=True, entry_type: str = "peak", value_min=-1, value_max=-1, flag=True):
        self.parent = parent
        big_table_data: TableData = parent.big_table_data
        gui_utility = GuiUtility(parent=self.parent)

        # Find the active row in the reduction table
        active_row_index = gui_utility.get_current_table_reduction_check_box_checked()
        if active_row_index == gui_utility.NULL_ACTIVE_ROW:  # no active row
            return

        # find all indexes in the table for rows having the same run number as that stored in row `active_row_index`
        # for reflectometry data (is_data==True) there can be only one row
        all_rows: List[int] = gui_utility.get_other_row_with_same_run_number_as_row(
            row=active_row_index, is_data=is_data
        )
        for row_index in all_rows:
            if is_data:
                data = big_table_data.reflectometry_data(row_index)
            else:
                data = big_table_data.normalization_data(row_index)  # type: ignore
                assert data is not None

            val1 = value_min
            val2 = value_max

            if val1 > val2:
                val_min = val2
                val_max = val1
            else:
                val_min = val1
                val_max = val2

            is_plot_yt = True
            is_plot_yi = True
            is_plot_it = False
            is_plot_ix = False
            if entry_type == "peak":
                data.peak = [val_min, val_max]
            elif entry_type == "back":
                data.back = [val_min, val_max]
            elif entry_type == "back2":
                data.back2 = [val_min, val_max]
            elif entry_type == "low_res":
                is_plot_yt = False
                is_plot_yi = False
                is_plot_ix = True
                data.low_res = [val_min, val_max]
                data.low_res_flag = flag
            else:
                raise RuntimeError("unexpected entry type")

            if is_data:
                big_table_data.set_reflectometry_data(row_index, data)
            else:
                big_table_data.set_normalization_data(row_index, data)
            self.parent.big_table_data = big_table_data

            if active_row_index == row_index:
                DisplayPlots(
                    parent=self.parent,
                    row=active_row_index,
                    is_data=is_data,
                    plot_yt=is_plot_yt,
                    plot_yi=is_plot_yi,
                    plot_it=is_plot_it,
                    plot_ix=is_plot_ix,
                    refresh_reduction_table=False,
                )


class DataSpinbox(object):
    def __init__(self, parent=None, entry_type="peak", value_min=-1, value_max=-1, flag=True):
        SpinBox(parent=parent, is_data=True, entry_type=entry_type, value_min=value_min, value_max=value_max, flag=flag)


class NormSpinbox(object):
    def __init__(self, parent=None, entry_type="peak", value_min=-1, value_max=-1, flag=True):
        SpinBox(
            parent=parent, is_data=False, entry_type=entry_type, value_min=value_min, value_max=value_max, flag=flag
        )


class DataPeakSpinbox(object):
    parent = None

    def __init__(self, parent=None):
        self.parent = parent
        peak1 = self.parent.ui.peakFromValue.value()
        peak2 = self.parent.ui.peakToValue.value()
        DataSpinbox(parent=parent, entry_type="peak", value_min=peak1, value_max=peak2)


class DataBackSpinbox(object):
    r"""Validator for the SpinBoxes holding the lower and upper boundaries for the two backgrounds of the
    reflectivity data.

    Parameters
    ----------
    parent
        Widget owning the spinbox
    entry_type
        One of "back" or "back2", denoting the first or the second background ROI's
    """

    parent = None

    def __init__(self, parent: QWidget, entry_type: str = "back"):
        if entry_type == "back":
            back1, back2 = parent.ui.backFromValue.value(), parent.ui.backToValue.value()
        elif entry_type == "back2":
            back1, back2 = parent.ui.back2FromValue.value(), parent.ui.back2ToValue.value()
        else:
            raise ValueError("Valid `entry_type` options are 'back', 'back2'")
        DataSpinbox(parent=parent, entry_type=entry_type, value_min=back1, value_max=back2)


class NormPeakSpinbox(object):
    Parent = None

    def __init__(self, parent=None):
        self.parent = parent
        peak1 = self.parent.ui.normPeakFromValue.value()
        peak2 = self.parent.ui.normPeakToValue.value()
        NormSpinbox(parent=parent, entry_type="peak", value_min=peak1, value_max=peak2)


class NormBackSpinbox(object):
    r"""Validator for the SpinBoxes holding the lower and upper boundaries for the two backgrounds of the
    normalization data.

    Parameters
    ----------
    parent
        Widget owning the spinbox
    entry_type
        One of "back" or "back2", denoting the first or the second background ROI's
    """

    parent = None

    def __init__(self, parent: QWidget, entry_type: str = "back"):
        if entry_type == "back":
            back1, back2 = parent.ui.normBackFromValue.value(), parent.ui.normBackToValue.value()
        elif entry_type == "back2":
            back1, back2 = parent.ui.normBack2FromValue.value(), parent.ui.normBack2ToValue.value()
        else:
            raise ValueError(f"entry_type '{entry_type}' is not valid. Valid options are 'back', 'back2'")
        NormSpinbox(parent=parent, entry_type=entry_type, value_min=back1, value_max=back2)


class DataLowResSpinbox(object):
    parent = None

    def __init__(self, parent=None):
        self.parent = parent
        lowres1 = self.parent.ui.dataLowResFromValue.value()
        lowres2 = self.parent.ui.dataLowResToValue.value()
        flag = self.parent.ui.dataLowResFlag.isChecked()
        DataSpinbox(parent=parent, entry_type="low_res", value_min=lowres1, value_max=lowres2, flag=flag)


class NormLowResSpinbox(object):
    parent = None

    def __init__(self, parent=None):
        self.parent = parent
        lowres1 = self.parent.ui.normLowResFromValue.value()
        lowres2 = self.parent.ui.normLowResToValue.value()
        flag = self.parent.ui.normLowResFlag.isChecked()
        NormSpinbox(parent=parent, entry_type="low_res", value_min=lowres1, value_max=lowres2, flag=flag)
