from RefRed.configuration.export_stitching_ascii_settings import ExportStitchingAsciiSettings
from RefRed.reduction.global_reduction_settings_handler import GlobalReductionSettingsHandler
from RefRed.gui_handling.gui_utility import GuiUtility

class ExportXMLConfig(object):
    
    parent = None
    filename = ''
    str_array = []
    
    def __init__(self, parent=None, filename=''):
        self.parent = parent
        self.filename = filename
        
        self.prepare_big_table_data()
        self.header_part()
        self.main_part()
	self.save_xml()
        
    def	prepare_big_table_data(self):
	'''
	all data files used last data clocking values
	'''

	big_table_data = self.parent.big_table_data
	o_gui_utility = GuiUtility(parent = self.parent)
	row_highest_q = o_gui_utility.get_row_with_highest_q()
	print(row_highest_q)

	_ref_lrdata = big_table_data[row_highest_q, 0]
	_ref_clocking = _ref_lrdata.clocking

	for row in range(row_highest_q):
	    _lrdata = big_table_data[row, 0]
	    _lrdata.clocking = _ref_clocking
	    big_table_data[row, 0] = _lrdata
	    
	self.parent.big_table_data = big_table_data
        
    def header_part(self):
	str_array = self.str_array
        str_array.append('<Reduction>\n')
        str_array.append(' <instrument_name>REFL</instrument_name>\n')

        # time stamp
        import datetime
        str_array.append(' <timestamp>' + datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + '</timestamp>\n')

        # python version
        import sys
        str_array.append(' <python_version>' + sys.version + '</python_version>\n')

        # platform
        import platform
        str_array.append(' <platform>' + platform.system() + '</platform>\n')

        # architecture
        str_array.append(' <architecture>' + platform.machine() + '</architecture>\n')

        # mantid version
        import mantid
        str_array.append(' <mantid_version>' + mantid.__version__ + '</mantid_version>\n')

	# generator
	str_array.append('<generator>RefRed</generator>\n')

        # metadata
        str_array.append(' <DataSeries>\n')
        
        self.str_array = str_array
	
    def main_part(self):
	
	str_array = self.str_array
        _big_table_data = self.parent.big_table_data
	nbr_row = self.parent.nbr_row_table_reduction
	o_general_settings = GlobalReductionSettingsHandler(parent = self.parent)
	
        for row in range(nbr_row):

            _data = _big_table_data[row,0]
	    if _data is None:
		break

	    str_array.append('  <RefLData>\n')
	    str_array.append('   <peak_selection_type>narrow</peak_selection_type>\n')
	    
	    #data_full_file_name = _data.full_file_name
	    #if type(data_full_file_name) == type([]):
		#data_full_file_name = ','.join(data_full_file_name)
	    data_peak = _data.peak
	    data_back = _data.back
	    data_low_res = _data.low_res
	    data_back_flag = _data.back_flag
	    data_low_res_flag = bool(_data.low_res_flag)
	    data_lambda_requested = _data.lambda_requested
	    clocking = _data.clocking
	    tof = _data.tof_range
#	    tof_units = _data.tof_units
	    tof_auto_flag = _data.tof_auto_flag
	    q_range = _data.q_range
	    lambda_range = _data.lambda_range
	    incident_angle = _data.incident_angle

            _norm = _big_table_data[row,1]
	    if (_norm is not None):
		norm_full_file_name = _norm.full_file_name
		#if type(norm_full_file_name) == type([]):
		    #norm_full_file_name = ','.join(norm_full_file_name)
		norm_flag = _norm.use_it_flag
		norm_peak = _norm.peak
		norm_back = _norm.back
		norm_back_flag = _norm.back_flag
		norm_low_res = _norm.low_res
		norm_low_res_flag = _norm.low_res_flag
		norm_lambda_requested = _norm.lambda_requested
	    else:
		#norm_full_file_name = ''
		norm_flag = False
		norm_peak = [0,255]
		norm_back = [0,255]
		norm_back_flag = False
		norm_low_res = [0,255]
		norm_low_res_flag = False
		norm_lambda_requested = -1
	    
            str_array.append('   <from_peak_pixels>' + str(data_peak[0]) + '</from_peak_pixels>\n')
            str_array.append('   <to_peak_pixels>' + str(data_peak[1]) + '</to_peak_pixels>\n')
            str_array.append('   <peak_discrete_selection>N/A</peak_discrete_selection>\n')
            str_array.append('   <background_flag>' + str(data_back_flag) + '</background_flag>\n')
            str_array.append('   <back_roi1_from>' + str(data_back[0]) + '</back_roi1_from>\n')
            str_array.append('   <back_roi1_to>' + str(data_back[1]) + '</back_roi1_to>\n')
            str_array.append('   <back_roi2_from>0</back_roi2_from>\n')
            str_array.append('   <back_roi2_to>0</back_roi2_to>\n')
	    str_array.append('   <clocking_from>' + str(clocking[0]) + '</clocking_from>\n')
	    str_array.append('   <clocking_to>' + str(clocking[1]) + '</clocking_to>\n')
            str_array.append('   <tof_range_flag>True</tof_range_flag>\n')
            str_array.append('   <from_tof_range>' + str(tof[0]) + '</from_tof_range>\n')
            str_array.append('   <to_tof_range>' + str(tof[1]) + '</to_tof_range>\n')
            str_array.append('   <from_q_range>' + str(q_range[0]) + '</from_q_range>\n')
            str_array.append('   <to_q_range>' + str(q_range[1]) + '</to_q_range>\n')
            str_array.append('   <from_lambda_range>' + str(lambda_range[0]) + '</from_lambda_range>\n')
            str_array.append('   <to_lambda_range>' + str(lambda_range[1]) + '</to_lambda_range>\n')
            str_array.append('   <incident_angle>' + str(incident_angle) + '</incident_angle>\n')

            _data_run_number = self.parent.ui.reductionTable.item(row,1).text()
            str_array.append('   <data_sets>' + _data_run_number + '</data_sets>\n')
            #if type(data_full_file_name) == type([]):
                #data_full_file_name = ','.join(data_full_file_name)
            #str_array.append('   <data_full_file_name>' + data_full_file_name + '</data_full_file_name>\n')

            str_array.append('   <x_min_pixel>' + str(data_low_res[0]) + '</x_min_pixel>\n')
            str_array.append('   <x_max_pixel>' + str(data_low_res[1]) + '</x_max_pixel>\n')
            str_array.append('   <x_range_flag>' + str(data_low_res_flag) + '</x_range_flag>\n')

            tthd = self.parent.ui.metadatatthdValue.text()
            str_array.append('   <tthd_value>' + tthd + '</tthd_value>\n')
            ths = self.parent.ui.metadatathiValue.text()
            str_array.append('   <ths_value>' + ths + '</ths_value>\n')
            str_array.append('   <data_lambda_requested>' + str(data_lambda_requested) + '</data_lambda_requested>\n')

            str_array.append('   <norm_flag>' + str(norm_flag) + '</norm_flag>\n')
            str_array.append('   <norm_x_range_flag>' + str(norm_low_res_flag) + '</norm_x_range_flag>\n')
            str_array.append('   <norm_x_max>' + str(norm_low_res[1]) + '</norm_x_max>\n')
            str_array.append('   <norm_x_min>' + str(norm_low_res[0]) + '</norm_x_min>\n')
            str_array.append('   <norm_from_peak_pixels>' + str(norm_peak[0]) + '</norm_from_peak_pixels>\n')
            str_array.append('   <norm_to_peak_pixels>' + str(norm_peak[1]) + '</norm_to_peak_pixels>\n')
            str_array.append('   <norm_background_flag>' + str(norm_back_flag) + '</norm_background_flag>\n')
            str_array.append('   <norm_from_back_pixels>' + str(norm_back[0]) + '</norm_from_back_pixels>\n')
            str_array.append('   <norm_to_back_pixels>' + str(norm_back[1]) + '</norm_to_back_pixels>\n')
            str_array.append('   <norm_lambda_requested>' + str(norm_lambda_requested) + '</norm_lambda_requested>\n')

            _norm_run_number_cell = self.parent.ui.reductionTable.item(row,2)
            if _norm_run_number_cell is not None:
                _norm_run_number = _norm_run_number_cell.text()
            else:
                _norm_run_number = ''
            str_array.append('   <norm_dataset>' + _norm_run_number + '</norm_dataset>\n')
            #if type(norm_full_file_name) == type([]):
                #norm_full_file_name = ','.join(norm_full_file_name)
            #str_array.append('   <norm_full_file_name>' + norm_full_file_name + '</norm_full_file_name>\n')

            str_array.append('   <auto_q_binning>False</auto_q_binning>\n')
            _exportStitchingAsciiSettings = ExportStitchingAsciiSettings()
            _overlap_lowest_error = _exportStitchingAsciiSettings.use_lowest_error_value_flag
            str_array.append('   <overlap_lowest_error>' + str(_overlap_lowest_error) + '</overlap_lowest_error>\n')

            angleValue = self.parent.ui.angleOffsetValue.text()
            angleError = self.parent.ui.angleOffsetError.text()
            str_array.append('   <angle_offset>' + angleValue + '</angle_offset>\n')
            str_array.append('   <angle_offset_error>' + angleError + '</angle_offset_error>\n')
	    
	    q_step = self.parent.ui.qStep.text()
	    str_array.append('   <q_step>' + q_step + '</q_step>\n')
	    q_min = '0.001'
	    str_array.append('   <q_min>' + q_min + '</q_min>\n')
	    
            scalingFactorFlag = self.parent.ui.scalingFactorFlag.isChecked()
            str_array.append('   <scaling_factor_flag>' + str(scalingFactorFlag) + '</scaling_factor_flag>\n')
            scalingFactorFile = o_general_settings.scaling_factor_file
            str_array.append('   <scaling_factor_file>' + scalingFactorFile + '</scaling_factor_file>\n')

            # incident medium
            allItems = [str(self.parent.ui.selectIncidentMediumList.itemText(i)) for i in range(self.parent.ui.selectIncidentMediumList.count())] 
            finalList = allItems[1:]
            strFinalList = ",".join(finalList)
            str_array.append('   <incident_medium_list>' + strFinalList + '</incident_medium_list>\n')

            imIndex = self.parent.ui.selectIncidentMediumList.currentIndex()
            str_array.append('   <incident_medium_index_selected>' + str(imIndex) + '</incident_medium_index_selected>\n')

            # output
            fcFlag = _exportStitchingAsciiSettings.fourth_column_flag
            str_array.append('   <fourth_column_flag>' + str(fcFlag) + '</fourth_column_flag>\n')

            fcdq0 = _exportStitchingAsciiSettings.fourth_column_dq0
            str_array.append('   <fourth_column_dq0>' + str(fcdq0) + '</fourth_column_dq0>\n')

            fcdqoverq = _exportStitchingAsciiSettings.fourth_column_dq_over_q
            str_array.append('   <fourth_column_dq_over_q>' + str(fcdqoverq) + '</fourth_column_dq_over_q>\n')

            str_array.append('  </RefLData>\n')

        str_array.append('  </DataSeries>\n')
        str_array.append('</Reduction>\n')
	self.str_array = str_array

    def save_xml(self):
	filename = self.filename
	str_array = self.str_array
	
        # write out XML file
        f = open(filename, 'w')
        f.writelines(str_array)
        f.close()
	