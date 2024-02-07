# import sys
from qtpy import QtCore, QtWidgets
import logging
import numpy as np
import os

from RefRed.autopopulatemaintable.reductiontable_auto_fill import ReductionTableAutoFill
from RefRed.configuration.loading_configuration import LoadingConfiguration
from RefRed.configuration.saving_configuration import SavingConfiguration
from RefRed.configuration.user_configuration_handler import RetrieveUserConfiguration, SaveUserConfiguration
from RefRed.export.export_plot_ascii import ExportPlotAscii
from RefRed.gui_handling.data_norm_spinboxes import DataPeakSpinbox, NormPeakSpinbox
from RefRed.gui_handling.data_norm_spinboxes import DataBackSpinbox, NormBackSpinbox
from RefRed.gui_handling.data_norm_spinboxes import DataLowResSpinbox, NormLowResSpinbox
from RefRed.gui_handling.scaling_factor_widgets_handler import ScalingFactorWidgetsHandler
from RefRed.gui_handling.auto_tof_range_radio_button_handler import AutoTofRangeRadioButtonHandler
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.gui_handling.stitching_yscale_options_radio_button_handler import StitchingYScaleOptionsRadioButtonHandler
from RefRed.gui_handling.first_angle_range_gui_handler import (
    NormalizationOrStitchingButtonStatus,
    FirstAngleRangeGuiHandler,
)
from RefRed.gui_handling.refred_interface_handler import RefRedInterfaceHandler
from RefRed.gui_handling.observer import SpinBoxObserver
from RefRed.initialization.gui import Gui as InitializeGui
from RefRed.initialization.gui_connections import GuiConnections as MakeGuiConnections
from RefRed.interfaces import load_ui
from RefRed.load_reduced_data_set.load_reduced_data_set_handler import LoadReducedDataSetHandler
from RefRed.load_reduced_data_set.reduced_ascii_data_right_click import ReducedAsciiDataRightClick
from RefRed.metadata.metadata_finder import MetadataFinder
from RefRed.plot.display_plots import DisplayPlots
from RefRed.plot.single_click_plot import SingleClickPlot
from RefRed.plot.home_plot_button_clicked import HomePlotButtonClicked
from RefRed.plot.mouse_leave_plot import MouseLeavePlot
from RefRed.plot.log_plot_toggle import LogPlotToggle
from RefRed.plot.background_settings import backgrounds_settings, BackgroundSettingsView
from RefRed.preview_config.preview_config import PreviewConfig
from RefRed.reduction.live_reduction_handler import LiveReductionHandler
from RefRed.reduction.reduced_data_handler import ReducedDataHandler
from RefRed.reduction_table_handling.reduction_table_check_box import ReductionTableCheckBox
from RefRed.reduction_table_handling.update_reduction_table import UpdateReductionTable
from RefRed.reduction_table_handling.reduction_table_right_click import ReductionTableRightClick
from RefRed.reduction_table_handling.reduction_table_handler import ReductionTableHandler
from RefRed.settings.initialize_settings import InitializeSettings
from RefRed.settings.settings_editor import SettingsEditor
from RefRed.sf_calculator.sf_calculator import SFCalculator
from RefRed.sf_preview.sf_preview import SFPreview
from RefRed.decorators import config_file_has_been_modified, config_file_modification_reset
from RefRed.about_dialog import AboutDialog
from RefRed.browsing_runs import BrowsingRuns
from RefRed.config.mantid_config import MantidConfig
from RefRed.tabledata import TableData


class MainGui(QtWidgets.QMainWindow):
    '''Top class that handles the GUI'''

    file_loaded_signal = QtCore.Signal(int, bool, bool)

    # default location
    path_ascii = '.'  # ascii file such as scaling factor file

    full_scaling_factor_file_name = ''
    home_dir = os.path.expanduser("~")
    default_loaded_file = os.path.join(home_dir, 'tmp.xml')
    current_loaded_file = os.path.join(home_dir, 'tmp.xml')
    browsed_files = {'data': None, 'norm': None}
    current_ipts = ""

    o_user_configuration = None  # will record the various settings of the GUI defined by the user
    o_stitching_ascii_widget = None  # used when loading ascii files in reduced tab

    manual_x_axis_dialog = None
    manual_y_axis_dialog = None

    REDUCTIONTABLE_MAX_ROWCOUNT = 39  # the maximum number of runs to be reduced
    nbr_row_table_ascii = 8
    prev_table_reduction_row_selected = -1
    current_table_reduction_row_selected = -1
    reduction_table_check_box_state = np.zeros((REDUCTIONTABLE_MAX_ROWCOUNT), dtype=bool)
    loading_nxs_thread = {
        'thread1': None,
        'thread2': None,
        'thread3': None,
        'thread4': None,
        'thread5': None,
        'thread6': None,
        'thread7': None,
        'thread8': None,
        'thread9': None,
        'thread10': None,
        'thread11': None,
        'thread12': None,
        'thread13': None,
        'thread14': None,
        'thread15': None,
        'thread16': None,
        'thread17': None,
        'thread18': None,
        'thread19': None,
        'thread20': None,
        'thread21': None,
        'thread22': None,
        'thread23': None,
        'thread24': None,
        'thread25': None,
        'thread26': None,
        'thread27': None,
        'thread28': None,
    }
    index_free_thread = 0

    time_click1 = 0  # use by double click of plots

    big_table_data = TableData(REDUCTIONTABLE_MAX_ROWCOUNT)

    # various metadata such as q_min (for output reduced ascii)
    gui_metadata = {}

    def __init__(self, argv=[], parent=None):
        if parent is None:
            QtWidgets.QMainWindow.__init__(self)
        else:
            QtWidgets.QMainWindow.__init__(self, parent, QtCore.Qt.Window)
        self.ui = load_ui("refred_main_interface.ui", self)

        InitializeSettings(self)
        self.config = MantidConfig(self)
        InitializeGui(self)
        self.ui.reductionTable.setUI(self)
        MakeGuiConnections(parent=self)
        RetrieveUserConfiguration(parent=self)

        self.file_loaded_signal.connect(self.file_loaded)
        log_file = os.path.expanduser("~") + '/.refred.log'
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

        # backup the last value for each spinbox in this widget
        self.spinbox_observer = SpinBoxObserver()

        # initialize background settings' main GUI and background-related control spinbox visibilities
        backgrounds_settings.set_maingui(self)
        backgrounds_settings["data"].control_spinboxes_visibility(
            parent=self.ui,
            first_background=("backFromValue", "backToValue"),
            second_background=("back2FromValue", "back2ToValue"),
        )
        backgrounds_settings["norm"].control_spinboxes_visibility(
            parent=self.ui,
            first_background=("normBackFromValue", "normBackToValue"),
            second_background=("normBack2FromValue", "normBack2ToValue"),
        )

    # home button of plots
    def home_clicked_yi_plot(self):
        HomePlotButtonClicked(parent=self, plot_type='yi')

    def home_clicked_yt_plot(self):
        HomePlotButtonClicked(parent=self, plot_type='yt')

    def home_clicked_it_plot(self):
        HomePlotButtonClicked(parent=self, plot_type='it')

    def home_clicked_ix_plot(self):
        HomePlotButtonClicked(parent=self, plot_type='ix')

    def home_clicked_data_stitching_plot(self):
        HomePlotButtonClicked(parent=self, plot_type='stitching')

    # leave figure
    def leave_figure_yi_plot(self):
        MouseLeavePlot(parent=self, plot_type='yi')

    def leave_figure_yt_plot(self):
        MouseLeavePlot(parent=self, plot_type='yt')

    def leave_figure_it_plot(self):
        MouseLeavePlot(parent=self, plot_type='it')

    def leave_figure_ix_plot(self):
        MouseLeavePlot(parent=self, plot_type='ix')

    def leave_figure_data_stitching_plot(self):
        MouseLeavePlot(parent=self, plot_type='stitching')

    # single click
    def single_click_data_yi_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='data', plot_type='yi')

    def single_click_norm_yi_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='norm', plot_type='yi')

    def single_click_norm_yt_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='norm', plot_type='yt')

    def single_click_data_yt_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='data', plot_type='yt')

    def single_click_norm_it_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='norm', plot_type='it')

    def single_click_data_it_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='data', plot_type='it')

    def single_click_norm_ix_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='norm', plot_type='ix')

    def single_click_data_ix_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type='data', plot_type='ix')

    # toggle log
    def logy_toggle_yt_plot(self, checked):
        LogPlotToggle(parent=self, status=checked, plot_type='yt', is_y_log=True)

    def logy_toggle_it_plot(self, checked):
        LogPlotToggle(parent=self, status=checked, plot_type='it', is_y_log=True)

    def logy_toggle_ix_plot(self, checked):
        LogPlotToggle(parent=self, status=checked, plot_type='ix', is_y_log=True)

    def logx_toggle_yi_plot(self, checked):
        LogPlotToggle(parent=self, status=checked, plot_type='yi', is_y_log=False)

    def logx_toggle_data_stitching(self, checked):
        LogPlotToggle(parent=self, status=checked, plot_type='stitching', is_y_log=False)

    def logy_toggle_data_stitching(self, checked):
        LogPlotToggle(parent=self, status=checked, plot_type='stitching', is_y_log=True)

    # display row checkbox
    def reduction_table_visibility_changed_test(self, state, row):
        ReductionTableCheckBox(parent=self, row_selected=row)

    def file_loaded(self, row, is_data_displayed, is_display_requested):
        """Event call-back used to display plots and re-enable the reduction table after loading"""
        if is_display_requested:
            DisplayPlots(parent=self, row=row, is_data=is_data_displayed)
        self.ui.reductionTable.setEnabled(True)

    def table_reduction_cell_enter_pressed(self):
        """
        Deal with enter being pressed in a cell of the reduction table.
        To ensure that we don't keep unused data in memory, check
        whether we need to removed a run from memory.
        """
        row = self.ui.reductionTable.currentRow()
        col = self.ui.reductionTable.currentColumn()
        item = self.ui.reductionTable.item(row, col)
        if item is None:
            return
        self.select_next_field(current_row=row, current_col=col)
        runs = self.ui.reductionTable.item(row, col).text()
        # The application will dump core if it tries to load two files
        # at the same time, so ensure that this doesn't happen by
        # disabling the reduction table before loading.
        self.ui.reductionTable.setEnabled(False)
        UpdateReductionTable(parent=self, row=row, col=col, runs=runs)

    def select_next_field(self, current_row=-1, current_col=-1):
        # trick to be able to retrieve value in editing mode
        if current_row == self.ui.reductionTable.rowCount() - 1:
            self.ui.reductionTable.setCurrentCell(0, 1)
        elif current_col == 1:
            self.ui.reductionTable.setCurrentCell(current_row, current_col + 1)
        else:
            self.ui.reductionTable.setCurrentCell(current_row + 1, current_col - 1)

    def data_norm_tab_changed(self, index):
        o_gui_utility = GuiUtility(parent=self)
        _current_table_reduction_row_selected = o_gui_utility.get_current_table_reduction_check_box_checked()
        ReductionTableCheckBox(parent=self, row_selected=_current_table_reduction_row_selected)

    @config_file_has_been_modified
    def widget_modified(self, *args, **kwargs):
        pass

    @config_file_has_been_modified
    def data_back_spinbox_validation(self, *args, **kwargs):
        DataBackSpinbox(parent=self, entry_type="back")

    @config_file_has_been_modified
    def data_back2_spinbox_validation(self, *args, **kwargs):
        DataBackSpinbox(parent=self, entry_type="back2")

    @config_file_has_been_modified
    def display_data_background_settings(self, *args, **kwargs):
        BackgroundSettingsView(parent=self, run_type="data").show()

    @config_file_has_been_modified
    def display_norm_background_settings(self, *args, **kwargs):
        BackgroundSettingsView(parent=self, run_type="norm").show()

    def back_from_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox backFromValue, denoting
        the lower boundary of the background region.

        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.backFromValue):
            self.data_back_spinbox_validation(*args, **kwargs)

    def back_to_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox `backToValue`, denoting
        the upper boundary of the background region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.backToValue):
            self.data_back_spinbox_validation(*args, **kwargs)

    def back2_from_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox back2FromValue, denoting
        the lower boundary of the second background region.

        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.back2FromValue):
            self.data_back2_spinbox_validation(*args, **kwargs)

    def back2_to_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox `back2ToValue`, denoting
        the upper boundary of the second background region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.back2ToValue):
            self.data_back2_spinbox_validation(*args, **kwargs)

    @config_file_has_been_modified
    def data_back_checkbox(self, *args, **kwargs):
        DataBackSpinbox(parent=self)

    @config_file_has_been_modified
    def data_peak_spinbox_validation(self, *args, **kwargs):
        DataPeakSpinbox(parent=self)

    def peak_from_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox `peakFromValue`, denoting
        the lower boundary of the peak region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.peakFromValue):
            self.data_peak_spinbox_validation(*args, **kwargs)

    def peak_to_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox peakToValue, denoting
        the upper boundary of the peak region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.peakToValue):
            self.data_peak_spinbox_validation(*args, **kwargs)

    @config_file_has_been_modified
    def norm_peak_spinbox_validation(self, *args, **kwargs):
        NormPeakSpinbox(parent=self)

    def norm_peak_from_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox `normPeakFromValue`, denoting
        the lower boundary of the peak region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.normPeakFromValue):
            self.norm_peak_spinbox_validation(*args, **kwargs)

    def norm_peak_to_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox normPeakToValue, denoting
        the upper boundary of the peak region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.normPeakToValue):
            self.norm_peak_spinbox_validation(*args, **kwargs)

    @config_file_has_been_modified
    def norm_back_spinbox_validation(self, *args, **kwargs):
        NormBackSpinbox(parent=self)

    def norm_back_from_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox `normBackFromValue`, denoting
        the lower boundary of the peak region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.normBackFromValue):
            self.norm_back_spinbox_validation(*args, **kwargs)

    def norm_back_to_value_changed(self, *args, **kwargs):
        r"""Slot handing signal QSpinBox.valueChanged(int) for QSpinBox normBackToValue, denoting
        the upper boundary of the peak region.
        Only effect changes when the new value differs from the previous by one, indicating User
        clicked on the Up or Down arrows of the QSpinBox.
        """
        if self.spinbox_observer.quantum_change(self.ui.normBackToValue):
            self.norm_back_spinbox_validation(*args, **kwargs)

    @config_file_has_been_modified
    def norm_back_checkbox(self, *args, **kwargs):
        NormBackSpinbox(parent=self)

    @config_file_has_been_modified
    def data_low_res_validation(self, *args, **kwargs):
        DataLowResSpinbox(parent=self)

    @config_file_has_been_modified
    def norm_low_res_validation(self, *args, **kwargs):
        NormLowResSpinbox(parent=self)

    @config_file_has_been_modified
    def data_low_res_checkbox(self, *args, **kwargs):
        DataLowResSpinbox(parent=self)

    @config_file_has_been_modified
    def norm_low_res_checkbox(self, *args, **kwargs):
        NormLowResSpinbox(parent=self)

    @config_file_has_been_modified
    def auto_tof_range_radio_button(self, *args, **kwargs):
        o_auto_tof_range = AutoTofRangeRadioButtonHandler(parent=self)
        o_auto_tof_range.setup()
        o_auto_tof_range.radio_button_handler()

    @config_file_has_been_modified
    def manual_tof_range_line_edit_validation(self, *args, **kwargs):
        o_auto_tof_range = AutoTofRangeRadioButtonHandler(parent=self)
        o_auto_tof_range.setup()
        o_auto_tof_range.line_edit_validation()

    @config_file_has_been_modified
    def data_norm_sequence_event(self, *args, **kwargs):
        self.data_sequence_event()
        self.norm_sequence_event()

    @config_file_has_been_modified
    def data_sequence_event(self, *args, **kwargs):
        str_data_input = self.ui.data_sequence_lineEdit.text()
        ReductionTableAutoFill(parent=self, list_of_run_from_input=str_data_input, data_type_selected='data')
        self.ui.data_sequence_lineEdit.setText('')
        self.norm_sequence_event()

    @config_file_has_been_modified
    def data_browse_button(self, *args, **kwargs):
        BrowsingRuns(parent=self, data_type='data')
        ReductionTableAutoFill(parent=self, list_of_run_from_input='', data_type_selected='data')
        self.ui.data_sequence_lineEdit.setText('')

    @config_file_has_been_modified
    def norm_sequence_event(self, *args, **kwargs):
        str_norm_input = self.ui.norm_sequence_lineEdit.text()
        ReductionTableAutoFill(parent=self, list_of_run_from_input=str_norm_input, data_type_selected='norm')
        self.ui.norm_sequence_lineEdit.setText('')

    @config_file_has_been_modified
    def norm_browse_button(self, *args, **kwargs):
        BrowsingRuns(parent=self, data_type='norm')
        ReductionTableAutoFill(parent=self, list_of_run_from_input='', data_type_selected='norm')
        self.ui.norm_sequence_lineEdit.setText('')

    # Menu buttons
    def action_new(self):
        o_reduction_table_handler = ReductionTableHandler(parent=self)
        o_reduction_table_handler.full_clear()

        o_interface_handler = RefRedInterfaceHandler(parent=self)
        o_interface_handler.full_reset()

    def load_configuration(self):
        o_load_config = LoadingConfiguration(parent=self)
        o_load_config.run()

    @config_file_modification_reset
    def save_configuration(self, *args, **kwargs):
        o_save_config = SavingConfiguration(parent=self, filename=self.current_loaded_file)
        o_save_config.run()

    def save_as_configuration(self):
        o_save_config = SavingConfiguration(parent=self)
        o_save_config.run()

    def preview_live_config(self):
        o_preview_config = PreviewConfig(parent=self, is_live=True)
        o_preview_config.show()

    def preview_browse_config(self):
        o_preview_config = PreviewConfig(parent=self, is_live=False)
        o_preview_config.show()

    @config_file_has_been_modified
    def use_scaling_factor_checkbox(self, status, *args, **kwargs):
        o_scaling_factor = ScalingFactorWidgetsHandler(parent=self)
        o_scaling_factor.checkbox(status=status)

    @config_file_has_been_modified
    def browse_scaling_factor_button(self, *args, **kwargs):
        o_scaling_factor = ScalingFactorWidgetsHandler(parent=self)
        o_scaling_factor.browse()

    def preview_scaling_factor_button(self):
        o_sf_preview = SFPreview(parent=self)
        o_sf_preview.show()

    def run_reduction_button(self):
        o_live_reduction = LiveReductionHandler(parent=self)
        o_live_reduction.run()

    def export_reduction_script_button(self):
        o_reduction = LiveReductionHandler(parent=self)
        o_reduction.export()

    def data_stitching_table_manual_spin_box(self):
        o_reduction = ReducedDataHandler(parent=self)
        o_reduction.save_manual_sf()
        self.stitching_sf_radio_button()

    def export_stitching_data(self):
        o_export_plot = ExportPlotAscii(parent=self, data_type='stitched')
        o_export_plot.export()

    def export_it(self):
        o_export_plot = ExportPlotAscii(parent=self, data_type='it')
        o_export_plot.export()

    def export_yi(self):
        o_export_plot = ExportPlotAscii(parent=self, data_type='yi')
        o_export_plot.export()

    def export_ix(self):
        o_export_plot = ExportPlotAscii(parent=self, data_type='ix')
        o_export_plot.export()

    def export_yt(self):
        o_export_plot = ExportPlotAscii(parent=self, data_type='yt')
        o_export_plot.export()

    @config_file_has_been_modified
    def reduction_table_right_click(self, position, *args, **kwargs):
        o_reduction_table_right_click = ReductionTableRightClick(parent=self, position=position)
        o_reduction_table_right_click.run()

    def launch_metadata_finder(self):
        _meta_finder = MetadataFinder(parent=self)
        _meta_finder.show()

    def launch_sf_calculator(self):
        """
        Launch the scaling factor calculator
        """
        # We need to keep a reference to the created object for pyqt to properly start it.
        self.sf_calculator = SFCalculator(parent=self)
        self.sf_calculator.show()

    def stitching_sf_radio_button(self):
        o_reduced_plot = ReducedDataHandler(parent=self)
        o_reduced_plot.plot()

    def stitching_yscale_options_radio_button_1(self):
        '''R vs Q'''
        o_button_handler = StitchingYScaleOptionsRadioButtonHandler(parent=self)
        o_button_handler.set_index_button_clicked(index=0)
        self.stitching_sf_radio_button()

    def stitching_yscale_options_radio_button_2(self):
        '''RQ^4 vs Q'''
        o_button_handler = StitchingYScaleOptionsRadioButtonHandler(parent=self)
        o_button_handler.set_index_button_clicked(index=1)
        self.stitching_sf_radio_button()

    def load_reduced_data_set_button(self):
        o_load_reduced_set = LoadReducedDataSetHandler(parent=self)
        o_load_reduced_set.run()

    # display row of reduced ascii table
    def reduced_ascii_data_set_table_visibility_changed(self, state):
        # Clear and replot the reduced data, which includes the file data
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate(replot_only=True)

    def reduced_ascii_data_set_table_right_click(self, position):
        o_reduced_ascii_right_click = ReducedAsciiDataRightClick(parent=self, position=position)
        o_reduced_ascii_right_click.run()

    def sf_absolute_normalization_button(self):
        norm_or_stitching_object = NormalizationOrStitchingButtonStatus(parent=self)
        norm_or_stitching_object.setWidget(activated_button=0)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def sf_auto_stitching_button(self):
        norm_or_stitching_object = NormalizationOrStitchingButtonStatus(parent=self)
        norm_or_stitching_object.setWidget(activated_button=1)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def sf_manual_stitching_button(self):
        norm_or_stitching_object = NormalizationOrStitchingButtonStatus(parent=self)
        norm_or_stitching_object.setWidget(activated_button=2)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def sf_button_clicked(self):
        first_angle_handler = FirstAngleRangeGuiHandler(parent=self)
        first_angle_handler.setWidgets(is_sf_button_clicked=True)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def first_angle_range_button_clicked(self):
        first_angle_handler = FirstAngleRangeGuiHandler(parent=self)
        first_angle_handler.setWidgets(is_sf_button_clicked=False)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def sf_qmin_value_field(self):
        norm_or_stitching_object = NormalizationOrStitchingButtonStatus(parent=self)
        norm_or_stitching_object.setWidget(activated_button=0)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def sf_qmax_value_field(self):
        norm_or_stitching_object = NormalizationOrStitchingButtonStatus(parent=self)
        norm_or_stitching_object.setWidget(activated_button=0)
        live_reduction = LiveReductionHandler(parent=self)
        live_reduction.recalculate()

    def about_message(self):
        o_about_message = AboutDialog(parent=self)
        o_about_message.display()

    def settings_editor(self):
        o_settings_editor = SettingsEditor(parent=self)
        o_settings_editor.show()

    def closeEvent(self, event=None):
        SaveUserConfiguration(parent=self)
