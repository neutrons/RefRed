import datetime
import logging
import os
from typing import Optional

import lr_reduction
import mantid

import RefRed
from RefRed.calculations.lr_data import LRData
from RefRed.reduction.global_reduction_settings_handler import (
    GlobalReductionSettingsHandler,
)


class ExportXMLConfig(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.str_array = []

    def header_part(self):
        str_array = self.str_array
        str_array.append("<Reduction>\n")
        str_array.append(" <instrument_name>REFL</instrument_name>\n")
        str_array.append(" <timestamp>" + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "</timestamp>\n")
        str_array.append(" <version>%s</version>\n" % lr_reduction.__version__)
        str_array.append(" <mantid_version>" + mantid.__version__ + "</mantid_version>\n")
        str_array.append("<generator>RefRed-%s</generator>\n" % RefRed.__version__)

        # metadata
        str_array.append(" <DataSeries>\n")

        self.str_array = str_array

    def main_part(self):
        str_array = self.str_array
        _big_table_data = self.parent.big_table_data
        nbr_row = self.parent.REDUCTIONTABLE_MAX_ROWCOUNT
        o_general_settings = GlobalReductionSettingsHandler(parent=self.parent)

        for row in range(nbr_row):
            _data: LRData = _big_table_data[row, 0]
            if _data is None:
                break  # we found the first empty row in the reduction table. No more runs available

            str_array.append("  <RefLData>\n")
            str_array.append("   <peak_selection_type>narrow</peak_selection_type>\n")

            data_peak = _data.peak
            data_back = _data.back
            data_back2 = _data.back2
            data_low_res = _data.low_res
            data_back_flag = _data.back_flag
            data_two_backgrounds = _data.two_backgrounds
            data_low_res_flag = bool(_data.low_res_flag)
            data_lambda_requested = _data.lambda_requested
            tof = _data.tof_range
            q_range = _data.q_range
            lambda_range = _data.lambda_range
            incident_angle = _data.incident_angle
            const_q = _data.const_q

            _norm: Optional[LRData] = _big_table_data[row, 1]
            if _norm is not None:
                norm_flag = o_general_settings.apply_normalization
                norm_peak = _norm.peak
                norm_back = _norm.back
                norm_back2 = _norm.back2
                norm_back_flag = _norm.back_flag
                norm_two_backgrounds = _norm.two_backgrounds

                norm_low_res = _norm.low_res
                norm_low_res_flag = _norm.low_res_flag
                norm_lambda_requested = _norm.lambda_requested
            else:
                norm_flag = False
                norm_peak = [0, 255]
                norm_back = [0, 255]
                norm_back_flag = False
                norm_two_backgrounds = False
                norm_low_res = [0, 255]
                norm_low_res_flag = False
                norm_lambda_requested = -1

            str_array.append("   <from_peak_pixels>" + str(data_peak[0]) + "</from_peak_pixels>\n")
            str_array.append("   <to_peak_pixels>" + str(data_peak[1]) + "</to_peak_pixels>\n")
            str_array.append("   <peak_discrete_selection>N/A</peak_discrete_selection>\n")
            str_array.append("   <background_flag>" + str(data_back_flag) + "</background_flag>\n")
            str_array.append("   <two_backgrounds>" + str(data_two_backgrounds) + "</two_backgrounds>\n")
            str_array.append("   <back_roi1_from>" + str(data_back[0]) + "</back_roi1_from>\n")
            str_array.append("   <back_roi1_to>" + str(data_back[1]) + "</back_roi1_to>\n")
            str_array.append("   <back_roi2_from>" + str(data_back2[0]) + "</back_roi2_from>\n")
            str_array.append("   <back_roi2_to>" + str(data_back2[1]) + "</back_roi2_to>\n")
            str_array.append("   <tof_range_flag>True</tof_range_flag>\n")
            str_array.append("   <from_tof_range>" + str(tof[0]) + "</from_tof_range>\n")
            str_array.append("   <to_tof_range>" + str(tof[1]) + "</to_tof_range>\n")
            str_array.append("   <from_q_range>" + str(q_range[0]) + "</from_q_range>\n")
            str_array.append("   <to_q_range>" + str(q_range[1]) + "</to_q_range>\n")
            str_array.append("   <from_lambda_range>" + str(lambda_range[0]) + "</from_lambda_range>\n")
            str_array.append("   <to_lambda_range>" + str(lambda_range[1]) + "</to_lambda_range>\n")
            str_array.append("   <incident_angle>" + str(incident_angle) + "</incident_angle>\n")

            _data_run_number = str(self.parent.ui.reductionTable.item(row, 1).text())
            str_array.append("   <data_sets>" + _data_run_number + "</data_sets>\n")
            # if type(data_full_file_name) == type([]):
            # data_full_file_name = ','.join(data_full_file_name)
            # str_array.append('   <data_full_file_name>' + data_full_file_name + '</data_full_file_name>\n')

            str_array.append("   <x_min_pixel>" + str(data_low_res[0]) + "</x_min_pixel>\n")
            str_array.append("   <x_max_pixel>" + str(data_low_res[1]) + "</x_max_pixel>\n")
            str_array.append("   <x_range_flag>" + str(data_low_res_flag) + "</x_range_flag>\n")

            tthd = str(self.parent.ui.metadatatthdValue.text())
            str_array.append("   <tthd_value>" + tthd + "</tthd_value>\n")
            ths = str(self.parent.ui.metadatathiValue.text())
            str_array.append("   <ths_value>" + ths + "</ths_value>\n")
            str_array.append("   <data_lambda_requested>" + str(data_lambda_requested) + "</data_lambda_requested>\n")

            str_array.append("   <norm_flag>" + str(norm_flag) + "</norm_flag>\n")
            str_array.append("   <norm_x_range_flag>" + str(norm_low_res_flag) + "</norm_x_range_flag>\n")
            str_array.append("   <norm_x_max>" + str(norm_low_res[1]) + "</norm_x_max>\n")
            str_array.append("   <norm_x_min>" + str(norm_low_res[0]) + "</norm_x_min>\n")
            str_array.append("   <norm_from_peak_pixels>" + str(norm_peak[0]) + "</norm_from_peak_pixels>\n")
            str_array.append("   <norm_to_peak_pixels>" + str(norm_peak[1]) + "</norm_to_peak_pixels>\n")
            str_array.append("   <norm_background_flag>" + str(norm_back_flag) + "</norm_background_flag>\n")
            str_array.append("   <norm_two_backgrounds>" + str(norm_two_backgrounds) + "</norm_two_backgrounds>\n")
            str_array.append("   <norm_from_back_pixels>" + str(norm_back[0]) + "</norm_from_back_pixels>\n")
            str_array.append("   <norm_to_back_pixels>" + str(norm_back[1]) + "</norm_to_back_pixels>\n")
            str_array.append("   <norm_from_back2_pixels>" + str(norm_back2[0]) + "</norm_from_back2_pixels>\n")
            str_array.append("   <norm_to_back2_pixels>" + str(norm_back2[1]) + "</norm_to_back2_pixels>\n")
            str_array.append("   <norm_lambda_requested>" + str(norm_lambda_requested) + "</norm_lambda_requested>\n")

            _norm_run_number_cell = self.parent.ui.reductionTable.item(row, 2).text()
            if str(_norm_run_number_cell) != "":
                _norm_run_number = str(_norm_run_number_cell)
            else:
                _norm_run_number = "0"
            str_array.append("   <norm_dataset>" + _norm_run_number + "</norm_dataset>\n")
            # if type(norm_full_file_name) == type([]):
            # norm_full_file_name = ','.join(norm_full_file_name)
            # str_array.append('   <norm_full_file_name>' + norm_full_file_name + '</norm_full_file_name>\n')

            str_array.append("   <auto_q_binning>False</auto_q_binning>\n")

            # The angle offset is currently not exposed in the UI, so we set it to 0.
            str_array.append("   <angle_offset> 0 </angle_offset>\n")
            str_array.append("   <angle_offset_error> 0 </angle_offset_error>\n")

            q_step = str(self.parent.ui.qStep.text())
            str_array.append("   <q_step>" + q_step + "</q_step>\n")
            q_min = str(self.parent.gui_metadata["q_min"])
            str_array.append("   <q_min>" + q_min + "</q_min>\n")

            scalingFactorFlag = self.parent.ui.scalingFactorFlag.isChecked()
            str_array.append("   <scaling_factor_flag>" + str(scalingFactorFlag) + "</scaling_factor_flag>\n")
            scalingFactorFile = o_general_settings.scaling_factor_file
            str_array.append("   <scaling_factor_file>" + scalingFactorFile + "</scaling_factor_file>\n")

            # incident medium
            allItems = [
                str(self.parent.ui.selectIncidentMediumList.itemText(i))
                for i in range(self.parent.ui.selectIncidentMediumList.count())
            ]
            finalList = allItems[1:]
            strFinalList = ",".join(finalList)
            str_array.append("   <incident_medium_list>" + strFinalList + "</incident_medium_list>\n")

            imIndex = self.parent.ui.selectIncidentMediumList.currentIndex()
            str_array.append(
                "   <incident_medium_index_selected>" + str(imIndex - 1) + "</incident_medium_index_selected>\n"
            )

            str_array.append("   <slits_width_flag>True</slits_width_flag>\n")

            # dead time settings
            str_array.append(o_general_settings.dead_time.to_xml(indent="   ") + "\n")

            # instrument settings
            str_array.append(o_general_settings.instrument_settings.to_xml(indent="   ") + "\n")

            str_array.append("   <const_q>" + str(const_q) + "</const_q>\n")

            str_array.append("  </RefLData>\n")

        str_array.append("  </DataSeries>\n")
        str_array.append("</Reduction>\n")
        self.str_array = str_array

    def save(self, filename: str):
        r"""Save the current configuration for each run

        Parameters
        ----------
        filename: str
            The name of the file to which the configuration will be saved.
        """
        self.header_part()
        self.main_part()

        if os.path.isfile(filename):
            os.remove(filename)
        with open(filename, "w") as outfile:
            outfile.writelines(self.str_array)

        logging.info(f"Config is saved to {filename}.")
