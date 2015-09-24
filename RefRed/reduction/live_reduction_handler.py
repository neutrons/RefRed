from RefRed.mantid_utility import MantidUtility
from RefRed.lconfigdataset import LConfigDataset
from RefRed.reduction.live_calculate_sf import LiveCalculateSF
from RefRed.reduction.live_reduced_data_handler import LiveReducedDataHandler
from RefRed.gui_handling.progressbar_handler import ProgressBarHandler
from RefRed.reduction.export_data_reduction_script import ExportDataReductionScript
from RefRed.reduction.individual_reduction_settings_handler import IndividualReductionSettingsHandler
from RefRed.reduction.global_reduction_settings_handler import GlobalReductionSettingsHandler
from mantid.simpleapi import *
import mantid


class LiveReductionHandler(object):

    big_table_data = None
    list_reduced_workspace = []
    nbr_reduction_process = -1
    debug = False
    error = False
    
    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data
        
    def run(self):
        _big_table_data = self.big_table_data
        _data_0_0 = _big_table_data[0,0]
        if _data_0_0 is None:
            return
        
        self.parent.ui.reduceButton.setEnabled(False)
        
        self.nbr_reduction_process = self.calculate_nbr_reduction_process()
        self.cleanup()

        o_general_settings = GlobalReductionSettingsHandler(parent = self.parent)
        o_reduction_progressbar_handler = ProgressBarHandler(parent=self.parent)
        o_reduction_progressbar_handler.setup(nbr_reduction = self.nbr_reduction_process,
                                              label = 'Reduction Process ')
        
        for row_index in range(self.nbr_reduction_process):
            
            o_individual_settings = IndividualReductionSettingsHandler(parent = self.parent,
                                                                       row_index = row_index)
            
            # run reduction
            self.launch_reduction(o_general = o_general_settings,
                                  o_individual = o_individual_settings,
                                  debug = self.debug)
            if self.error:
                break
            
            self.save_reduction(row = row_index,
                                workspace = o_individual_settings._output_workspace_name)
            
            # scale
            o_calculate_sf = LiveCalculateSF(parent = self.parent,
                                             row_index = row_index)
            o_calculate_sf.run()
            
            # plot
            o_reduced_plot = LiveReducedDataHandler(parent = self.parent,
                                                    row_index = row_index)
            o_reduced_plot.populate_table()
            o_reduced_plot.live_plot()

            o_reduction_progressbar_handler.next_step()


        self.parent.big_table_data = self.big_table_data
        o_reduction_progressbar_handler.end()
        self.parent.ui.reduceButton.setEnabled(True)

    def export(self):
        o_export_script = ExportDataReductionScript(parent = self.parent)
        o_export_script.define_export_filename()
        o_export_script.make_script()
        o_export_script.create_file()
        
    def stitch(self):
        o_calculate_sf = CalculateSF(parent = self.parent,
                                     nbr_process = self.nbr_reduction_process)
        o_calculate_sf.run()

    def launch_reduction(self, o_general = None, o_individual = None, debug = False):
        
        if debug:
            print("Debugging LiquidsReflectrometryReduction")
            self.print_message('RunNumbers', o_individual._data_run_numbers)
            self.print_message('NormalizationRunNumber',  o_individual._norm_run_numbers)
            self.print_message('SignalPeakPixelRange', o_individual._data_peak_range)
            self.print_message('SubtractSignalBackground', o_individual._data_back_flag)
            self.print_message('SignalBackgroundPixelRange', o_individual._data_back_range)
            self.print_message('NormFlag', o_individual._norm_flag)
            self.print_message('NormPeakPixelRange', o_individual._norm_peak_range)
            self.print_message('NormBackgroundPixelRange', o_individual._norm_back_range)
            self.print_message('SubtractNormBackground', o_individual._norm_back_flag)
            self.print_message('LowResDataAxisPixelRangeFlag', o_individual._data_low_res_flag)
            self.print_message('LowResDataAxisPixelRange', o_individual._data_low_res_range)
            self.print_message('LowResNormAxisPixelRangeFlag', o_individual._norm_low_res_flag)
            self.print_message('LowResNormAxisPixelRange', o_individual._norm_low_res_range)
            self.print_message('TOFRange', o_individual._tof_range)
            self.print_message('IncidentMediumSelected', o_general.incident_medium_selected)
            self.print_message('GeometryCorrectionFlag', o_general.geometry_correction_flag)
            self.print_message('QMin', o_general.q_min)
            self.print_message('QStep', o_general.q_step)
            self.print_message('TOFSteps', o_general.tof_steps)
            self.print_message('AngleOffset', o_general.angle_offset)
            self.print_message('AngleOffsetError', o_general.angle_offset_error)
            self.print_message('ScalingFactorFile', o_general.scaling_factor_file)
            self.print_message('CropFirstAndLastPoints', True)
            self.print_message('SlitsWidthFlag', o_general.slits_width_flag)
            self.print_message('OutputWorkspace', o_individual._output_workspace_name)       
        
        try:
        
            LiquidsReflectometryReduction( RunNumbers = o_individual._data_run_numbers,
                                           NormalizationRunNumber = o_individual._norm_run_numbers,
                                           SignalPeakPixelRange = o_individual._data_peak_range,
                                           SubtractSignalBackground = o_individual._data_back_flag, 
                                           SignalBackgroundPixelRange = o_individual._data_back_range,
                                           NormFlag = o_individual._norm_flag,
                                           NormPeakPixelRange = o_individual._norm_peak_range,
                                           NormBackgroundPixelRange = o_individual._norm_back_range,
                                           SubtractNormBackground = o_individual._norm_back_flag,
                                           LowResDataAxisPixelRangeFlag = o_individual._data_low_res_flag,
                                           LowResDataAxisPixelRange = o_individual._data_low_res_range,
                                           LowResNormAxisPixelRangeFlag = o_individual._norm_low_res_flag,
                                           LowResNormAxisPixelRange = o_individual._norm_low_res_range,
                                           TOFRange = o_individual._tof_range,
                                           IncidentMediumSelected = o_general.incident_medium_selected,
                                           GeometryCorrectionFlag = o_general.geometry_correction_flag,
                                           QMin = o_general.q_min,
                                           QStep = o_general.q_step,
                                           TOFSteps = o_general.tof_steps,
                                           AngleOffset = o_general.angle_offset,
                                           AngleOffsetError = o_general.angle_offset_error,
                                           ScalingFactorFile = o_general.scaling_factor_file,
                                           CropFirstAndLastPoints = True,
                                           SlitsWidthFlag = o_general.slits_width_flag,
                                           OutputWorkspace = o_individual._output_workspace_name)
            self.list_reduced_workspace.append(o_individual._output_workspace_name)
            self.remove_tmp_workspaces()
        
        except:
            self.error = True
            
    def save_reduction(self, 
                       row = -1,
                       workspace = None):
        big_table_data = self.big_table_data
        _config = big_table_data[row, 2]
        if _config is None:
            _config = LConfigDataset()
        mtd_workspace = mtd[workspace]
        
        _config.proton_charge = float(mtd_workspace.getRun().getProperty('gd_prtn_chrg').value)
        _config.reduce_q_axis = mtd_workspace.readX(0)[:]
        _config.reduce_y_axis = mtd_workspace.readY(0)[:]
        _config.reduce_e_axis = mtd_workspace.readE(0)[:]
        _config.q_axis_for_display = mtd_workspace.readX(0)[:]
        _config.y_axis_for_display = mtd_workspace.readY(0)[:]
        _config.e_axis_for_display = mtd_workspace.readE(0)[:]
#        _config.sf_auto_found_match = mtd_workspace.getRun().getProperty('isSFfound').value
        
        big_table_data[row, 2] = _config
        self.big_table_data = big_table_data
        
    def remove_tmp_workspaces(self):
        list_mt = AnalysisDataService.getObjectNames()
        for _mt in list_mt:
            if _mt in self.list_reduced_workspace:
                continue
            AnalysisDataService.remove(_mt)
        
    def print_message(self, title, value):
        print('> %s ' %title)
        print('-> value: ', value, '-> type: ', type(value))

    def calculate_nbr_reduction_process(self):
        nbr_row_table_reduction = self.parent.nbr_row_table_reduction
        _big_table_data = self.big_table_data
        nbr_reduction = 0
        for row in range(nbr_row_table_reduction):
            if _big_table_data[row, 0] is None:
                return nbr_reduction
            nbr_reduction += 1
        return nbr_reduction
        
    def cleanup(self):
        o_mantid_utility = MantidUtility(parent = self.parent)
        o_mantid_utility.cleanup_workspaces()



