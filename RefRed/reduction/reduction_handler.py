from RefRed.mantid_utility import MantidUtility
from RefRed.lconfigdataset import LConfigDataset
from RefRed.reduction.calculate_sf import CalculateSF
from RefRed.gui_handling.progressbar_handler import ProgressBarHandler
from mantid.simpleapi import *
import mantid


class ReductionHandler(object):

    big_table_data = None
    list_reduced_workspace = []
    nbr_reduction_process = -1
    debug = False
    
    def __init__(self, parent=None):
        self.parent = parent
        self.big_table_data = self.parent.big_table_data
        
    def run(self):
        _big_table_data = self.big_table_data
        _data_0_0 = _big_table_data[0,0]
        if _data_0_0 is None:
            return
        
        self.nbr_reduction_process = self.calculate_nbr_reduction_process()
        self.cleanup()

        o_general_settings = GlobalReductionSettingsHandler(parent = self.parent)
        o_reduction_progressbar_handler = ProgressBarHandler(parent=self.parent)
        o_reduction_progressbar_handler.setup(nbr_reduction = self.nbr_reduction_process,
                                              label = 'Reduction Process ')
        
        for row_index in range(self.nbr_reduction_process):
            
            o_individual_settings = IndividualReductionSettingsHandler(parent = self.parent,
                                                                       row_index = row_index)
            
            self.launch_reduction(o_general = o_general_settings,
                                  o_individual = o_individual_settings,
                                  debug = self.debug)
            self.save_reduction(row = row_index,
                                workspace = o_individual_settings._output_workspace_name)
            o_reduction_progressbar_handler.next_step()
            
            
        self.parent.big_table_data = self.big_table_data
        o_reduction_progressbar_handler.end()

    def export(self):
        o_export_script = ExportDataReductionScript(parent = self.parent)
        o_export_script.define_export_filename()
        o_export_script.make_script()
        
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
            self.print_message('CropFirstAndLastPoints', False)
            self.print_message('SlitsWidthFlag', o_general.slits_width_flag)
            self.print_message('OutputWorkspace', o_individual._output_workspace_name)       
        
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


class IndividualReductionSettingsHandler(object):
    
    data = None
    norm = None
    output_workspace = ''
    
    def __init__(self, parent=None, row_index=-1):
        self.parent = parent
        self.row_index = row_index
        big_table_data = self.parent.big_table_data
        self.data = big_table_data[row_index, 0]
        self.norm = big_table_data[row_index, 1]
        self.retrieve()
        
    def retrieve(self):
        self._data_run_numbers = self.get_data_run_numbers()
        self._data_peak_range = self.get_data_peak_range()
        self._data_back_flag = self.get_data_back_flag()
        self._data_back_range = self.get_data_back_range()
        self._data_low_res_flag = self.get_data_low_res_flag()
        self._data_low_res_range = self.get_data_low_res_range()

        self._norm_flag = self.get_norm_flag()
        self._norm_run_numbers = self.get_norm_run_numbers()
        self._norm_peak_range = self.get_norm_peak_range()
        self._norm_back_flag = self.get_norm_back_flag()
        self._norm_back_range = self.get_norm_back_range()
        self._norm_low_res_flag = self.get_norm_low_res_flag()
        self._norm_low_res_range = self.get_norm_low_res_range()
        
        self._tof_range = self.get_tof_range()
        self._output_workspace_name = self.define_output_workspace_name(run_numbers = 
                                                                        self._data_run_numbers)
        
    def define_output_workspace_name(self, run_numbers = None):
        str_run_numbers = run_numbers
        return "reflectivity_%s" % str_run_numbers
        
    def get_tof_range(self):
        is_auto_tof_range_selected = self.is_auto_tof_range_selected()
        if is_auto_tof_range_selected:
            tof_range = self.get_auto_tof_range()
        else:
            tof_range = self.get_manual_tof_range()
        tof_range_micros = self.convert_tof_range_to_micros(tof_range = tof_range)
        return tof_range_micros
        
    def convert_tof_range_to_micros(self, tof_range = None):
        tof1 = float(tof_range[0])
        if tof1 < 100:
            tof1_micros = tof1 * 1000.
            tof2_micros = float(tof_range[1]) * 1000.
        else:
            tof1_micros = tof1
            tof2_micros = float(tof_range[1])
        return [tof1_micros, tof2_micros]
        
    def get_auto_tof_range(self):
        _data = self.data
        return _data.tof_range_auto
        
    def get_manual_tof_range(self):
        _data = self.data
        return _data.tof_range_manual

    def is_auto_tof_range_selected(self):
        _data = self.data
        return bool(_data.tof_range_auto_flag)
        
    def get_data_low_res_flag(self):
        _data = self.data
        return self.get_low_res_flag(data = _data)
        
    def get_norm_low_res_flag(self):
        _norm = self.norm
        return self.get_low_res_flag(data = _norm)
        
    def get_low_res_flag(self, data = None):
        return bool(data.low_res_flag)
        
    def get_data_low_res_range(self):
        _data = self.data
        return self.get_low_res_range(data = _data)
    
    def get_norm_low_res_range(self):
        _norm = self.norm
        return self.get_low_res_range(data = _norm)

    def get_low_res_range(self, data = None):
        low_res1 = int(data.low_res[0])
        low_res2 = int(data.low_res[1])
        low_res_min = min([low_res1, low_res2])
        low_res_max = max([low_res1, low_res2])
        return [low_res_min, low_res_max]
        
    def get_norm_flag(self):
        _norm = self.norm
        return _norm.use_it_flag
        
    def get_data_back_range(self):
        _data = self.data
        return self.get_back_range(data = _data)
    
    def get_norm_back_range(self):
        _norm = self.norm
        return self.get_back_range(data = _norm)
    
    def get_back_range(self, data = None):
        back1 = int(data.back[0])
        back2 = int(data.back[1])
        back_min = min([back1, back2])
        back_max = max([back1, back2])
        return [back_min, back_max]
    
    def get_data_back_flag(self):
        _data = self.data
        return self.get_back_flag(data = _data)
    
    def get_norm_back_flag(self):
        _norm = self.norm
        return self.get_back_flag(data = _norm)
    
    def get_back_flag(self, data = None):
        return bool(data.back_flag)
        
    def get_data_peak_range(self):
        _data = self.data
        return self.get_peak_range(data=_data)
    
    def get_norm_peak_range(self):
        _norm = self.norm
        return self.get_peak_range(data=_norm)
    
    def get_peak_range(self, data=None):
        peak1 = int(data.peak[0])
        peak2 = int(data.peak[1])
        peak_min = min([peak1, peak2])
        peak_max = max([peak1, peak2])
        return [peak_min, peak_max]
        
    def get_norm_run_numbers(self):
        return self.get_run_numbers(column_index = 2)
        
    def get_data_run_numbers(self):
        return self.get_run_numbers(column_index = 1)

    def get_run_numbers(self, column_index = 1):
        run_numbers = self.parent.ui.reductionTable.item(self.row_index, column_index).text()
        return str(run_numbers)

class GlobalReductionSettingsHandler(object):
    
    incident_medium_selected = ''
    geometry_correction_flag = False
    q_min = 0.005
    q_step = 50
    scaling_factor_file = ''
    scaling_factor_flag = True
    slits_width_flag = True
    angle_offset = 0.0
    angle_offset_error = 0.0
    tof_steps = 40 # microS
    
    def __init__(self, parent=None):
        self.parent = parent
        self.retrieve()
        
    def retrieve(self):
        self.incident_medium_selected = self.get_incident_medium_selected()
        self.q_step = self.get_q_step()
        self.scaling_factor_flag = self.get_scaling_factor_flag()
        self.scaling_factor_file = self.get_scaling_factor_file()
        self.angle_offset = self.get_angle_offset()
        self.angle_offset_error = self.get_angle_offset_error()
        self.tof_steps = self.get_tof_steps()
        
    def get_tof_steps(self):
        return float(self.parent.ui.eventTofBins.text())
        
    def get_angle_offset(self):
        return float(self.parent.ui.angleOffsetValue.text())

    def get_angle_offset_error(self):
        return float(self.parent.ui.angleOffsetError.text())
        
    def get_scaling_factor_flag(self):
        return self.parent.ui.scalingFactorFlag.isChecked()
        
    def get_scaling_factor_file(self):
        return str(self.parent.full_scaling_factor_file_name)
        
    def get_q_step(self):
        _q_step = self.parent.ui.qStep.text()
        return float(_q_step)
        
    def get_incident_medium_selected(self):
        _medium_selected = str(self.parent.ui.selectIncidentMediumList.currentText()).strip()
        return str(_medium_selected)
        
        
        
        
        
