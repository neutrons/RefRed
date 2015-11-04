from PyQt4 import QtGui
import logging
import numpy as np
import os

from RefRed.autopopulatemaintable.reductiontable_auto_fill import ReductionTableAutoFill
from RefRed.config_file_launcher import ConfigFileLauncher
from RefRed.configuration.loading_configuration import LoadingConfiguration
from RefRed.configuration.saving_configuration import SavingConfiguration
from RefRed.configuration.user_configuration_handler import RetrieveUserConfiguration, SaveUserConfiguration
from RefRed.export.export_plot_ascii import ExportPlotAscii
from RefRed.gui_handling.data_norm_spinboxes import DataPeakSpinbox, NormPeakSpinbox
from RefRed.gui_handling.data_norm_spinboxes import DataBackSpinbox, NormBackSpinbox
from RefRed.gui_handling.data_norm_spinboxes import DataLowResSpinbox, NormLowResSpinbox
from RefRed.gui_handling.data_norm_spinboxes import DataClockingSpinbox
from RefRed.gui_handling.scaling_factor_widgets_handler import ScalingFactorWidgetsHandler
from RefRed.gui_handling.auto_tof_range_radio_button_handler import AutoTofRangeRadioButtonHandler
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.gui_handling.stitching_yscale_options_radio_button_handler import StitchingYScaleOptionsRadioButtonHandler
from RefRed.initialization.gui import Gui as InitializeGui
from RefRed.initialization.gui_connections import GuiConnections as MakeGuiConnections
from RefRed.interfaces.refred_main_interface import Ui_MainWindow
from RefRed.load_reduced_data_set.load_reduced_data_set_handler import LoadReducedDataSetHandler
from RefRed.load_reduced_data_set.reduced_ascii_data_right_click import ReducedAsciiDataRightClick
from RefRed.metadata.metadata_finder import MetadataFinder
from RefRed.plot.single_click_plot import SingleClickPlot
from RefRed.plot.home_plot_button_clicked import HomePlotButtonClicked
from RefRed.plot.mouse_leave_plot import MouseLeavePlot
from RefRed.plot.log_plot_toggle import LogPlotToggle
from RefRed.reduction.reduction_handler import ReductionHandler
from RefRed.reduction.live_reduction_handler import LiveReductionHandler
from RefRed.reduction.reduced_data_handler import ReducedDataHandler
from RefRed.reduction_table_handling.reduction_table_check_box import ReductionTableCheckBox
from RefRed.reduction_table_handling.update_reduction_table import UpdateReductionTable
from RefRed.reduction_table_handling.reduction_table_right_click import ReductionTableRightClick
from RefRed.update_data_norm_tab import UpdateDataNormTab
from RefRed.sf_calculator.sf_calculator import SFCalculator
from RefRed.sf_preview.sf_preview import SFPreview
from RefRed.decorators import config_file_has_been_modified, config_file_modification_reset
#from RefRed.log_plot_toggle import LogPlotToggle

class MainGui(QtGui.QMainWindow):
    ''' Top class that handles the GUI '''
    
    # default location
    path_ascii = '.'  # ascii file such as scaling factor file
    path_config = '/home/j35/sandbox' # config file of RefRed
    
    full_scaling_factor_file_name = ''
    current_loaded_file = '~/tmp.xml'
    
    o_user_configuration = None # will record the various settings of the GUI defined by the user
    o_stitching_ascii_widget = None # used when loading ascii files in reduced tab

    nbr_row_table_reduction = 30
    nbr_row_table_ascii = 8
    prev_table_reduction_row_selected = -1
    current_table_reduction_row_selected = -1
    reduction_table_check_box_state = np.zeros((nbr_row_table_reduction), dtype=bool)
    loading_nxs_thread = {'thread1': None, 'thread2': None, 'thread3': None, 'thread4': None,
                          'thread5': None, 'thread6': None, 'thread7': None, 'thread8': None,
                          'thread9': None, 'thread10': None, 'thread11': None, 'thread12': None,
                          'thread13': None, 'thread14': None, 'thread15': None, 'thread16': None,
                          'thread17': None, 'thread18': None, 'thread19': None, 'thread20': None,
                          'thread21': None, 'thread22': None, 'thread23': None, 'thread24': None,
                          'thread25': None, 'thread26': None, 'thread27': None, 'thread28': None}
    index_free_thread = 0

    time_click1 = 0 #use by double click of plots

    #[data, norm, lconfig]
    big_table_data = np.empty((nbr_row_table_reduction, 3), dtype=object)

    #Reduced ascii data sets
    #o_stitched_ascii = None

    def __init__(self, argv=[], parent=None):
        if parent is None:
            QtGui.QMainWindow.__init__(self)
        else:
            QtGui.QMainWindow.__init__(self, parent, QtCore.Qt.Window)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)        
        
        InitializeGui(self)
        self.ui.reductionTable.setUI(self)   
        MakeGuiConnections(parent = self)
        RetrieveUserConfiguration(parent = self)

        log_file = os.path.expanduser("~") + '/.refred.log'
        logging.basicConfig(filename=log_file, level=logging.DEBUG)

    # export plot into ascii files
    def export_ix(self):
        ExportPlotAscii(self, type='ix')
    def export_it(self):
        ExportPlotAscii(self, type='it')
    def export_yt(self):
        ExportPlotAscii(self, type='yt')
    def export_yi(self):
        ExportPlotAscii(self, type='yi')
    def export_stitching_data(self):
        ExportPlotAscii(self, type='stitched')

    # home button of plots
    def home_clicked_yi_plot(self):
        HomePlotButtonClicked(parent = self, plot_type = 'yi')
    def home_clicked_yt_plot(self):
        HomePlotButtonClicked(parent = self, plot_type = 'yt')
    def home_clicked_it_plot(self):
        HomePlotButtonClicked(parent = self, plot_type = 'it')
    def home_clicked_ix_plot(self):
        HomePlotButtonClicked(parent = self, plot_type = 'ix')
    def home_clicked_data_stitching_plot(self):
        HomePlotButtonClicked(parent = self, plot_type = 'stitching')

    # leave figure 
    def leave_figure_yi_plot(self):
        MouseLeavePlot(parent = self, plot_type = 'yi')
    def leave_figure_yt_plot(self):
        MouseLeavePlot(parent = self, plot_type = 'yt')
    def leave_figure_it_plot(self):
        MouseLeavePlot(parent = self, plot_type = 'it')
    def leave_figure_ix_plot(self):
        MouseLeavePlot(parent = self, plot_type = 'ix')
    def leave_figure_data_stitching_plot(self):
        MouseLeavePlot(parent = self, plot_type = 'stitching')

    # single click
    def single_click_data_yi_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'data', plot_type = 'yi')
    def single_click_norm_yi_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'norm', plot_type = 'yi')
    def single_click_norm_yt_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'norm', plot_type = 'yt')
    def single_click_data_yt_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'data', plot_type = 'yt')
    def single_click_norm_it_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'norm', plot_type = 'it')
    def single_click_data_it_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'data', plot_type = 'it')
    def single_click_norm_ix_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'norm', plot_type = 'ix')
    def single_click_data_ix_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'data', plot_type = 'ix')
    def single_click_data_stitching_plot(self, isPanOrZoomActivated):
        SingleClickPlot(self, data_type = 'data', plot_type = 'stitching')

    # toggle log
    def logy_toggle_yt_plot(self, checked):
        LogPlotToggle(parent = self,
                      status = checked,
                      plot_type = 'yt',
                      is_y_log = True)
    def logy_toggle_it_plot(self, checked):
        LogPlotToggle(parnt = self,
                      status = checked,
                      plot_type = 'it',
                      is_y_log = True)
    def logy_toggle_ix_plot(self, checked):
        LogPlotToggle(parent = self,
                      status = checked,
                      plot_type = 'ix',
                      is_y_log = True)
    def logx_toggle_yi_plot(self, checked):
        LogPlotToggle(parent = self,
                      status = checked,
                      plot_type = 'yi',
                      is_y_log = False)
    def logx_toggle_data_stitching(self, checked):
        LogPlotToggle(parent = self,
                      status = checked,
                      plot_type = 'stitching',
                      is_y_log = False)
    def logy_toggle_data_stitching(self, checked):
        LogPlotToggle(parent = self,
                      status = checked,
                      plot_type = 'stitching',
                      is_y_log = True)

    # display row checkbox
    def reduction_table_visibility_changed_test(self, state, row):
        ReductionTableCheckBox(parent = self, row_selected = row)
        
    def table_reduction_cell_enter_pressed(self):
        row = self.ui.reductionTable.currentRow()
        col = self.ui.reductionTable.currentColumn()
        item = self.ui.reductionTable.item(row, col)
        if item is None:
            return
        self.select_next_field(current_row=row, current_col=col)
        runs = self.ui.reductionTable.item(row, col).text()
        UpdateReductionTable(parent=self, row=row, col=col, runs=runs)
        
    def select_next_field(self, current_row=-1, current_col=-1):
        # trick to be able to retrieve value in editing mode
        if current_row == self.ui.reductionTable.rowCount()-1:
            self.ui.reductionTable.setCurrentCell(0, 1)
        elif current_col == 1:
            self.ui.reductionTable.setCurrentCell(current_row, current_col+1)
        else:
            self.ui.reductionTable.setCurrentCell(current_row+1, current_col-1)
        
    def data_norm_tab_changed(self, index):
        o_gui_utility = GuiUtility(parent = self)
        _current_table_reduction_row_selected = o_gui_utility.get_current_table_reduction_check_box_checked()
        ReductionTableCheckBox(parent = self,
                               row_selected = _current_table_reduction_row_selected)
        
    @config_file_has_been_modified
    def widget_modified(self, value_changed):
        pass

    @config_file_has_been_modified
    def data_back_spinbox_validation(self):
        DataBackSpinbox(parent = self)
    
    @config_file_has_been_modified
    def data_back_checkbox(self):
        DataBackSpinbox(parent = self)
    
    @config_file_has_been_modified
    def data_peak_spinbox_validation(self):
        DataPeakSpinbox(parent = self)
    
    @config_file_has_been_modified
    def norm_back_spinbox_validation(self):
        NormBackSpinbox(parent = self)
        
    @config_file_has_been_modified
    def norm_back_checkbox(self):
        NormBackSpinbox(parent = self)
    
    @config_file_has_been_modified
    def norm_peak_spinbox_validation(self):
        NormPeakSpinbox(parent = self)

    @config_file_has_been_modified
    def data_low_res_validation(self):
        DataLowResSpinbox(parent = self)
        
    @config_file_has_been_modified
    def norm_low_res_validation(self):
        NormLowResSpinbox(parent = self)
        
    @config_file_has_been_modified
    def data_low_res_checkbox(self):
        DataLowResSpinbox(parent = self)
        
    @config_file_has_been_modified
    def norm_low_res_checkbox(self):
        NormLowResSpinbox(parent = self)
    
    @config_file_has_been_modified
    def clock_validation(self):
        DataClockingSpinbox(parent = self)
    
    @config_file_has_been_modified
    def auto_tof_range_radio_button(self):
        o_auto_tof_range = AutoTofRangeRadioButtonHandler(parent = self)
        o_auto_tof_range.setup()
        o_auto_tof_range.radio_button_handler()

    @config_file_has_been_modified
    def manual_tof_range_line_edit_validation(self):
        o_auto_tof_range = AutoTofRangeRadioButtonHandler(parent = self)
        o_auto_tof_range.setup()
        o_auto_tof_range.line_edit_validation()
        
    @config_file_has_been_modified
    def data_norm_sequence_event(self):
        self.data_sequence_event()
        self.norm_sequence_event()

    @config_file_has_been_modified
    def data_sequence_event(self):
        str_data_input = self.ui.data_sequence_lineEdit.text()
        ReductionTableAutoFill(parent = self,
                               list_of_run_from_input = str_data_input,
                               data_type_selected = 'data')
        self.ui.data_sequence_lineEdit.setText('')
        self.norm_sequence_event()
        
    @config_file_has_been_modified
    def norm_sequence_event(self):
        str_norm_input = self.ui.norm_sequence_lineEdit.text()
        ReductionTableAutoFill(parent = self,
                               list_of_run_from_input = str_norm_input,
                               data_type_selected = 'norm')
        self.ui.norm_sequence_lineEdit.setText('')
        
    def load_configuration(self):
        o_load_config = LoadingConfiguration(parent = self)
        o_load_config.run()
        
    @config_file_modification_reset
    def save_configuration(self):
        o_save_config = SavingConfiguration(parent = self,
                                            filename = self.current_loaded_file)
        o_save_config.run()
        
    def save_as_configuration(self):
        o_save_config = SavingConfiguration(parent = self)
        o_save_config.run()
        
    @config_file_has_been_modified
    def use_scaling_factor_checkbox(self, status):
        o_scaling_factor = ScalingFactorWidgetsHandler(parent = self)
        o_scaling_factor.checkbox(status = status)
        
    @config_file_has_been_modified
    def browse_scaling_factor_button(self):
        o_scaling_factor = ScalingFactorWidgetsHandler(parent = self)
        o_scaling_factor.browse()
        
    def preview_scaling_factor_button(self):
        o_sf_preview = SFPreview(parent=self)
        o_sf_preview.show()
        
    def run_reduction_button(self):
        o_live_reduction = LiveReductionHandler(parent = self)
        o_live_reduction.run()

        #o_reduction = ReductionHandler(parent = self)
        #o_reduction.run()
        #o_reduction.stitch()
        
        #o_reduced_plot = ReducedDataHandler(parent = self)
        #o_reduced_plot.populate_table()
        #o_reduced_plot.plot()

    def export_reduction_script_button(self):
        o_reduction = ReductionHandler(parent = self)
        o_reduction.export()

    def data_stitching_table_manual_spin_box(self):
        o_reduction = ReducedDataHandler(parent = self)
        o_reduction.save_manual_sf()
        self.stitching_sf_radio_button()
    
    def export_stitching_data(self):
        o_export_plot = ExportPlotAscii(parent = self,
                                        data_type = 'stitched')
        o_export_plot.export()
        
    def export_it(self):
        o_export_plot = ExportPlotAscii(parent = self,
                                        data_type = 'it')
        o_export_plot.export()
        
    def export_yi(self):
        o_export_plot = ExportPlotAscii(parent = self,
                                        data_type = 'yi')
        o_export_plot.export()
        
    def export_ix(self):
        o_export_plot = ExportPlotAscii(parent = self,
                                        data_type = 'ix')
        o_export_plot.export()
        
    def export_yt(self):
        o_export_plot = ExportPlotAscii(parent = self,
                                        data_type = 'yt')
        o_export_plot.export()
        
    @config_file_has_been_modified
    def reduction_table_right_click(self, position):
        o_reduction_table_right_click = ReductionTableRightClick(parent = self,
                                                                 position = position)
        o_reduction_table_right_click.run()
        
    def launch_metadata_finder(self):
        _meta_finder = MetadataFinder(parent = self)
        _meta_finder.show()        
        
    def launch_sf_calculator(self):
        o_sf_calculator = SFCalculator()
        o_sf_calculator.show()
        
    def stitching_sf_radio_button(self):
        o_reduced_plot = ReducedDataHandler(parent = self)
        o_reduced_plot.plot()
        
    def stitching_yscale_options_radio_button_1(self):
        '''R vs Q'''
        o_button_handler = StitchingYScaleOptionsRadioButtonHandler(parent = self)
        o_button_handler.set_index_button_clicked(index = 0)
        self.stitching_sf_radio_button()
        
    def stitching_yscale_options_radio_button_2(self):
        '''RQ^4 vs Q'''
        o_button_handler = StitchingYScaleOptionsRadioButtonHandler(parent = self)
        o_button_handler.set_index_button_clicked(index = 1)
        self.stitching_sf_radio_button()

    def stitching_yscale_options_radio_button_3(self):
        '''LogR vs Q'''
        o_button_handler = StitchingYScaleOptionsRadioButtonHandler(parent = self)
        o_button_handler.set_index_button_clicked(index = 2)
        self.stitching_sf_radio_button()
        
    def load_reduced_data_set_button(self):
        o_load_reduced_set = LoadReducedDataSetHandler(parent = self)
        o_load_reduced_set.run()
        
    # display row of reduced ascii table
    def reduced_ascii_data_set_table_visibility_changed(self, state):
        o_load_reduced = LoadReducedDataSetHandler(parent = self)
        o_load_reduced.plot()

    def reduced_ascii_data_set_table_right_click(self, position):
        o_reduced_ascii_right_click = ReducedAsciiDataRightClick(parent = self,
                                                                 position = position)
        o_reduced_ascii_right_click.run()
        
    def closeEvent(self, event=None):
        SaveUserConfiguration(parent = self)
        
        