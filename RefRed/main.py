from PyQt4 import QtGui
import numpy as np

from refred_main_interface import Ui_MainWindow
from initialization.gui import Gui as InitializeGui
from config_file_launcher import ConfigFileLauncher
from initialization.gui_connections import GuiConnections as MakeGuiConnections
from initialization.reduction_table_check_box import ReductionTableCheckBox

#from RefRed.export_plot_ascii import ExportPlotAscii
#from RefRed.home_plot_button_clicked import HomePlotButtonClicked
#from RefRed.mouse_leave_plot import MouseLeavePlot
#from RefRed.single_plot_click import SinglePlotClick
#from RefRed.log_plot_toggle import LogPlotToggle

class MainGui(QtGui.QMainWindow):
    ''' Top class that handles the GUI '''
    
    # default location
    path_ascii = '.'  # ascii files
    nbr_row_table_reduction = 30
    prev_table_reduction_row_selected = -1
    reduction_table_check_box_state = np.zeros((nbr_row_table_reduction), dtype=bool)

    def __init__(self, argv=[], parent=None):
        if parent is None:
            QtGui.QMainWindow.__init__(self)
        else:
            QtGui.QMainWindow.__init__(self, parent, QtCore.Qt.Window)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        InitializeGui(self)
#        MakeGuiConnections(self)


    # config files from menu
    def launch_config_file1(self):
        ConfigFileLauncher(self, 0)
    def launch_config_file2(self):
        ConfigFileLauncher(self, 1)
    def launch_config_file3(self):
        ConfigFileLauncher(self, 2)
    def launch_config_file4(self):
        ConfigFileLauncher(self, 3)
    def launch_config_file5(self):
        ConfigFileLauncher(self, 4)
    def launch_config_file6(self):
        ConfigFileLauncher(self, 5)
    def launch_config_file7(self):
        ConfigFileLauncher(self, 6)
    def launch_config_file8(self):
        ConfigFileLauncher(self, 7)
    def launch_config_file9(self):
        ConfigFileLauncher(self, 8)
    def launch_config_file10(self):
        ConfigFileLauncher(self, 9)
    
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
        HomePlotButtonClicked(self, type='yi')
    def home_clicked_yt_plot(self):
        HomePlotButtonClicked(self, type='yt')
    def home_clicked_it_plot(self):
        HomePlotButtonClicked(self, type='it')
    def home_clicked_ix_plot(self):
        HomePlotButtonClicked(self, type='ix')
    def home_clicked_data_stitching_plot(self):
        HomePlotButtonClicked(self, type='stitching')

    # leave figure 
    def leave_figure_yi_plot(self):
        MouseLeavePlot(self, type='yi', retain_all=self.retain_all)
    def leave_figure_yt_plot(self):
        MouseLeavePlot(self, type='yt', retain_all=self.retain_all)
    def leave_figure_it_plot(self):
        MouseLeavePlot(self, type='it', retain_all=self.retain_all)
    def leave_figure_ix_plot(self):
        MouseLeavePlot(self, type='ix', retain_all=self.retain_all)
    def leave_figure_data_stitching_plot(self):
        MouseLeavePlot(self, type='stitching')

    # single click
    def single_click_data_yi_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self, 'data','yi')
    def single_click_norm_yi_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'norm','yi')
    def single_click_norm_yt_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'norm','yt')
    def single_click_data_yt_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'data','yt')
    def single_click_norm_it_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self, 'norm','it')
    def single_click_data_it_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'data','it')
    def single_click_norm_ix_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'norm','ix')
    def single_click_data_ix_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'data','ix')
    def single_click_data_stitching_plot(self, isPanOrZoomActivated):
        SinglePlotClick(self,'data','stitching')

    # toggle log
    def logy_toggle_yt_plot(self, checked):
        LogPlotToggle(self,checked,'yt',is_y_log=True)
    def logy_toggle_it_plot(self, checked):
        LogPlotToggle(self,checked,'it',is_y_log=True)
    def logy_toggle_ix_plot(self, checked):
        LogPlotToggle(self,checked,'ix',is_y_log=True)
    def logx_toggle_yi_plot(self, checked):
        LogPlotToggle(self,checked,'yi',is_y_log=False)
    def logx_toggle_data_stitching(self, checked):
        LogPlotToggle(self,checked,'stitching',is_y_log=False)
    def logy_toggle_data_stitching(self, checked):
        LogPlotToggle(self,checked,'stitching',is_y_log=True)

    def reduction_table_visibility_changed_0(self, state):
        print(state)
        ReductionTableCheckBox(parent=self, row_selected=0)
    def reduction_table_visibility_changed_1(self, state):
        ReductionTableCheckBox(parent=self, row_selected=1)
    def reduction_table_visibility_changed_2(self, state):
        ReductionTableCheckBox(parent=self, row_selected=2)
    def reduction_table_visibility_changed_3(self, state):
        ReductionTableCheckBox(parent=self, row_selected=3)
    def reduction_table_visibility_changed_4(self, state):
        ReductionTableCheckBox(parent=self, row_selected=4)
    def reduction_table_visibility_changed_5(self, state):
        ReductionTableCheckBox(parent=self, row_selected=5)
    def reduction_table_visibility_changed_6(self, state):
        ReductionTableCheckBox(parent=self, row_selected=6)
    def reduction_table_visibility_changed_7(self, state):
        ReductionTableCheckBox(parent=self, row_selected=7)
    def reduction_table_visibility_changed_8(self, state):
        ReductionTableCheckBox(parent=self, row_selected=8)
    def reduction_table_visibility_changed_9(self, state):
        ReductionTableCheckBox(parent=self, row_selected=9)
    def reduction_table_visibility_changed_10(self, state):
        ReductionTableCheckBox(parent=self, row_selected=10)
    def reduction_table_visibility_changed_11(self, state):
        ReductionTableCheckBox(parent=self, row_selected=11)
    def reduction_table_visibility_changed_12(self, state):
        ReductionTableCheckBox(parent=self, row_selected=12)
    def reduction_table_visibility_changed_13(self, state):
        ReductionTableCheckBox(parent=self, row_selected=13)
    def reduction_table_visibility_changed_14(self, state):
        ReductionTableCheckBox(parent=self, row_selected=14)
    def reduction_table_visibility_changed_15(self, state):
        ReductionTableCheckBox(parent=self, row_selected=15)
    def reduction_table_visibility_changed_16(self, state):
        ReductionTableCheckBox(parent=self, row_selected=16)
    def reduction_table_visibility_changed_17(self, state):
        ReductionTableCheckBox(parent=self, row_selected=17)
    def reduction_table_visibility_changed_18(self, state):
        ReductionTableCheckBox(parent=self, row_selected=18)
    def reduction_table_visibility_changed_19(self, state):
        ReductionTableCheckBox(parent=self, row_selected=19)
    def reduction_table_visibility_changed_20(self, state):
        ReductionTableCheckBox(parent=self, row_selected=20)
    def reduction_table_visibility_changed_21(self, state):
        ReductionTableCheckBox(parent=self, row_selected=21)
    def reduction_table_visibility_changed_22(self, state):
        ReductionTableCheckBox(parent=self, row_selected=22)
    def reduction_table_visibility_changed_23(self, state):
        ReductionTableCheckBox(parent=self, row_selected=23)
    def reduction_table_visibility_changed_24(self, state):
        ReductionTableCheckBox(parent=self, row_selected=24)
    def reduction_table_visibility_changed_25(self, state):
        ReductionTableCheckBox(parent=self, row_selected=25)
    def reduction_table_visibility_changed_26(self, state):
        ReductionTableCheckBox(parent=self, row_selected=26)
    def reduction_table_visibility_changed_27(self, state):
        ReductionTableCheckBox(parent=self, row_selected=27)
    def reduction_table_visibility_changed_28(self, state):
        ReductionTableCheckBox(parent=self, row_selected=28)
    def reduction_table_visibility_changed_29(self, state):
        ReductionTableCheckBox(parent=self, row_selected=29)
