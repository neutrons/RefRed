# RefRed imports
from RefRed.plot.background_settings import backgrounds_settings
from RefRed.gui_handling.gui_utility import GuiUtility


class UpdatePlotWidgetStatus(object):
    """
    This class will check if the plot widgets can be enabled according to
    status of the main table and tab selected
    """

    parent = None

    def __init__(self, parent=None):
        self.parent = parent

    def disable_all(self):
        self.data_tab_widgets(status=False)
        self.norm_tab_widgets(status=False)

    def disable_data(self):
        self.data_tab_widgets(status=False)

    def enable_data(self):
        self.data_tab_widgets(status=True)

    def disable_norm(self):
        self.norm_tab_widgets(status=False)

    def enable_norm(self):
        self.norm_tab_widgets(status=True)

    def data_tab_widgets(self, status=False):
        parent = self.parent
        parent.ui.dataNormTabWidget.setEnabled(status)
        parent.ui.data_yt_plot.setEnabled(status)
        parent.ui.dataNameOfFile.setEnabled(status)
        parent.ui.data_yi_plot.setEnabled(status)
        parent.ui.data_it_plot.setEnabled(status)
        parent.ui.data_ix_plot.setEnabled(status)
        parent.ui.dataLowResFlag.setEnabled(status)
        parent.ui.dataLowResFromLabel.setEnabled(status)
        parent.ui.dataLowResFromValue.setEnabled(status)
        parent.ui.dataLowResToLabel.setEnabled(status)
        parent.ui.dataLowResToValue.setEnabled(status)
        parent.ui.peakToValue.setEnabled(status)
        parent.ui.peakFromValue.setEnabled(status)

        # let the background settings ultimately control the spinboxes visibility
        status_custom = status and backgrounds_settings["data"].subtract_background
        parent.ui.backToValue.setEnabled(status_custom)
        parent.ui.backFromValue.setEnabled(status_custom)
        status_custom = (
            status
            and backgrounds_settings["data"].subtract_background
            and backgrounds_settings["data"].two_backgrounds
        )
        parent.ui.back2ToValue.setEnabled(status_custom)
        parent.ui.back2FromValue.setEnabled(status_custom)

        self.parent.ui.dataTOFmanualLabel.setEnabled(status)
        self.parent.ui.dataTOFautoMode.setEnabled(status)
        self.parent.ui.dataTOFmanualMode.setEnabled(status)
        o_gui_utility = GuiUtility(parent=self.parent)
        if status:
            is_auto_tof_selected = o_gui_utility.is_auto_tof_range_radio_button_selected()
            o_gui_utility.set_auto_tof_range_widgets(status=is_auto_tof_selected)
        else:
            o_gui_utility.set_auto_tof_range_widgets(status=True)

    def norm_tab_widgets(self, status=False):
        parent = self.parent
        parent.ui.dataNormTabWidget.setEnabled(status)
        parent.ui.norm_yt_plot.setEnabled(status)
        parent.ui.normNameOfFile.setEnabled(status)
        parent.ui.norm_yi_plot.setEnabled(status)
        parent.ui.norm_it_plot.setEnabled(status)
        parent.ui.norm_ix_plot.setEnabled(status)
        parent.ui.normLowResFlag.setEnabled(status)
        parent.ui.normLowResFromLabel.setEnabled(status)
        parent.ui.normLowResFromValue.setEnabled(status)
        parent.ui.normLowResToLabel.setEnabled(status)
        parent.ui.normLowResToValue.setEnabled(status)
        parent.ui.normPeakToValue.setEnabled(status)
        parent.ui.normPeakFromValue.setEnabled(status)

        # let the background settings ultimately control the spinboxes visibility
        status_custom = status and backgrounds_settings["norm"].subtract_background
        parent.ui.normBackToValue.setEnabled(status_custom)
        parent.ui.normBackFromValue.setEnabled(status_custom)
        status_custom = (
            status
            and backgrounds_settings["norm"].subtract_background
            and backgrounds_settings["norm"].two_backgrounds
        )
        parent.ui.normBack2ToValue.setEnabled(status_custom)
        parent.ui.normBack2FromValue.setEnabled(status_custom)

        self.parent.ui.dataTOFmanualLabel.setEnabled(status)
        self.parent.ui.dataTOFautoMode.setEnabled(status)
        self.parent.ui.dataTOFmanualMode.setEnabled(status)

        o_gui_utility = GuiUtility(parent=self.parent)
        if status:
            is_auto_tof_selected = o_gui_utility.is_auto_tof_range_radio_button_selected()
            o_gui_utility.set_auto_tof_range_widgets(status=is_auto_tof_selected)
        else:
            o_gui_utility.set_auto_tof_range_widgets(status=True)
