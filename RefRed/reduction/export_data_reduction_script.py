from PyQt4 import QtGui
import time
import os
from RefRed.reduction.individual_reduction_settings_handler import IndividualReductionSettingsHandler
from RefRed.reduction.global_reduction_settings_handler import GlobalReductionSettingsHandler
from RefRed.utilities import createAsciiFile

class ExportDataReductionScript(object):

    sull_script = []
    export_filename = ''
    o_general_settings = None

    def __init__(self, parent=None):
        self.parent = parent
        self.init_parameters()

    def init_parameters(self):
        self.script = []
        self._data_run_numbers = ''
        self._norm_run_numbers = ''
        self._data_peak_range = []
        self._data_back_flag = True
        self._data_back_range = []
        self._norm_flag = True
        self._norm_peak_range = []
        self._norm_back_range = []
        self._norm_back_flag = True
        self._data_low_res_flag = True
        self._data_low_res_range = []
        self._norm_low_res_flag = True
        self._norm_low_res_range = []
        self._tof_range = []
        self._incident_medium_selected = ''
        self._geometry_correction_flag = True
        self._q_min = -1
        self._q_step = -1
        self._tof_steps = -1
        self._angle_offset = -1
        self._angle_offset_error = -1
        self._scaling_factor_file = ''
        self._crop_first_and_last_points_flag = True
        self._slits_width_flag = True
        self._output_workspace = ''

    def define_export_filename(self):
        parent = self.parent
        big_table_data = parent.big_table_data
        _data = big_table_data[0, 0]
        run_number = _data.run_number
        default_filename = 'REFL_' + run_number + '_data_reduction_script.py'
        path = parent.path_ascii
        default_filename = path + '/' + default_filename
        filename = str(QtGui.QFileDialog.getSaveFileName(parent,
                                                         'Python Script',
                                                         default_filename))
        if filename == '':
            return
        self.export_filename = filename
        self.parent.path_ascii = os.path.dirname(filename)

    def make_script(self):
        if self.export_filename == '':
            return
        self.make_header_script()
        self.retrieve_global_parameters()
        self.make_reduction_script()

    def create_file(self):
        if self.export_filename == '':
            return
        createAsciiFile(self.export_filename, self.full_script)

    def make_header_script(self):
        script = []
        script.append('# RefRed Reduction script')
        _date = time.strftime("%d_%m_%Y")
        script.append('# Script automatically generated on ' + _date + '\n')
        script.append('\n')
        script.append('import os\n')
        script.append('import mantid\n')
        script.append('from mantid.simpleapi import *\n')
        script.append('import LiquidsReflectometryReduction \n\n')
        self.full_script = script

    def retrieve_global_parameters(self):
        self.o_general_settings = GlobalReductionSettingsHandler(parent = self.parent)

    def make_reduction_script(self):
        nbr_reduction_process = self.calculate_nbr_reduction_process()
        for row_index in range(nbr_reduction_process):
            
            o_individual_settings = IndividualReductionSettingsHandler(parent=self.parent,
                                                                       row_index=row_index)
            self.make_individual_reduction_script(o_individual = o_individual_settings)

    def make_individual_reduction_script(self, o_individual=None):
        o_general = self.o_general_settings

        script = self.full_script
        script.append('LiquidsReflectometryReduction(')
        script.append(' RunNumbers = [%s],' % o_individual._data_run_numbers)
        script.append(' NormalizationRunNumber = %s,' % o_individual._norm_run_numbers)
        script.append(' SignalPeakPixelRange = [%d, %d],' % (o_individual._data_peak_range[0], 
                                                             o_individual._data_peak_range[1]))
        script.append(' SubtractSignalBackground = %s,' % str(o_individual._data_back_flag))
        script.append(' SignalBackgroundPixelRange = [%d, %d],' % (o_individual._data_back_range[0],
                                                                   o_individual._data_back_range[1]))
        script.append(' NormFlag = %s,' %str(o_individual._norm_flag))
        script.append(' NormPeakPixelRange = [%d, %d],' % (o_individual._norm_peak_range[0],
                                                           o_individual._norm_peak_range[1]))
        script.append(' NormBackgroundPixelRange = [%d, %d],' % (o_individual._norm_back_range[0],
                                                                 o_individual._norm_back_range[1]))
        script.append(' SubtractNormBackground = %s,' % str(o_individual._norm_back_flag))
        script.append(' LowResDataAxisPixelRangeFlag = %s,' % str(o_individual._data_low_res_flag))
        script.append(' LowResDataAxisPixelRange = [%d, %d],' % (o_individual._data_low_res_range[0],
                                                                 o_individual._data_low_res_range[1]))
        script.append(' LowResNormAxisPixelRangeFlag = %s,' % str(o_individual._norm_low_res_flag))
        script.append(' LowResNormAxisPixelRange = [%d, %d],' % (o_individual._norm_low_res_range[0],
                                                                 o_individual._norm_low_res_range[1]))
        script.append(' TOFRange = [%f, %f],' % (o_individual._tof_range[0],
                                                 o_individual._tof_range[1]))
        script.append(' IncidentMediumSelected = "%s",' % o_general.incident_medium_selected)
        script.append(' GeometryCorrectionFlag = %s,' % str(o_general.geometry_correction_flag))
        script.append(' QMin = %f,' % o_general.q_min)
        script.append(' QStep = %f,' % o_general.q_step)
        script.append(' TOFSteps = %f,' % o_general.tof_steps)
        script.append(' AngleOffset = %f,' % o_general.angle_offset)
        script.append(' AngleOffsetError = %f,' % o_general.angle_offset_error)
        script.append(' ScalingFactorFile = "%s",' % o_general.scaling_factor_file)
        script.append(' CropFirstAndLastPoints = True,')
        script.append(' SlitsWidthFlag = %s,' % str(o_general.slits_width_flag))
        script.append(' OutputWorkspace = "%s")' % o_individual._output_workspace_name)
        script.append('\n\n')

        self.full_script = script

    def calculate_nbr_reduction_process(self):
        nbr_row_table_reduction = self.parent.nbr_row_table_reduction
        _big_table_data = self.parent.big_table_data
        nbr_reduction = 0
        for row in range(nbr_row_table_reduction):
            if _big_table_data[row, 0] is None:
                return nbr_reduction
            nbr_reduction += 1
        return nbr_reduction
