from PyQt4.QtGui import QDialog, QFileDialog, QPalette
from PyQt4.QtCore import Qt
from mantid.simpleapi import *
import os
import numpy as np
import time

from RefRed.interfaces.output_reduced_data_dialog import Ui_Dialog as UiDialog
from RefRed.export.stitching_ascii_widget import StitchingAsciiWidget
from RefRed.configuration.export_stitching_ascii_settings import ExportStitchingAsciiSettings
from RefRed.export.reduced_ascii_loader import ReducedAsciiLoader
from RefRed.gui_handling.gui_utility import GuiUtility
from RefRed.reduction.reduced_data_handler import ReducedDataHandler
import RefRed.utilities

class OutputReducedData(QDialog):
	
	_open_instances = []
	o_stitching_ascii_widget = None
	parent = None
	filename = ''
	
	q_axis = None
	y_axis = None
	e_axis = None
	
	R_THRESHOLD = 1e-15
	
	metadata = None
	text_data = None
	is_with_4th_column_flag = False
	dq0 = None
	dq_over_q = None
	use_lowest_error_value_flag = True
	
	def __init__(self, parent = None):
		QDialog.__init__(self, parent = parent)
		self.setWindowModality(False)
		self._open_instances.append(self)
		self.ui = UiDialog()
		self.ui.setupUi(self)
		self.parent = parent
		
		self.ui.folder_error.setVisible(False)
		palette = QPalette()
		palette.setColor(QPalette.Foreground, Qt.red)
		self.ui.folder_error.setPalette(palette)
		
		o_loaded_ascii = ReducedAsciiLoader(parent = parent,
		                                    ascii_file_name = '',
		                                    is_live_reduction = True)
		if parent.o_stitching_ascii_widget is None:
			o_stitching_ascii_widget = StitchingAsciiWidget(parent = self.parent,
			                                                loaded_ascii = o_loaded_ascii)
			parent.o_stitching_ascii_widget = o_stitching_ascii_widget
		
		# retrieve gui parameters 
		_export_stitching_ascii_settings = ExportStitchingAsciiSettings()
		self.dq0 = str(_export_stitching_ascii_settings.fourth_column_dq0)
		self.dq_over_q = str(_export_stitching_ascii_settings.fourth_column_dq_over_q)
		self.is_with_4th_column_flag = bool(_export_stitching_ascii_settings.fourth_column_flag)
		self.use_lowest_error_value_flag = bool(_export_stitching_ascii_settings.use_lowest_error_value_flag)
		
		self.ui.dq0Value.setText(self.dq0)
		self.ui.dQoverQvalue.setText(self.dq_over_q)
		self.ui.output4thColumnFlag.setChecked(self.is_with_4th_column_flag)
		self.ui.usingLessErrorValueFlag.setChecked(self.use_lowest_error_value_flag)
		self.ui.usingMeanValueFalg.setChecked(not self.use_lowest_error_value_flag)
		
	def create_reduce_ascii_button_event(self):
		self.ui.folder_error.setVisible(False)
		if self.parent.o_stitching_ascii_widget is None:
			return
		
		run_number = self.parent.ui.reductionTable.item(0,1).text()
		default_filename = 'REFL_' + run_number + '_reduced_stitched_data.txt'
		path = self.parent.path_ascii
		default_filename = path + '/' + default_filename
		directory = path
		_filter = u"Reduced Ascii (*.txt);; All (*.*)"
		filename = str(QFileDialog.getSaveFileName(self, 
		                                           'Select Location and Name', 
		                                           directory = default_filename,
		                                           filter = (_filter)))
		if filename.strip() == '':
			return
		
		folder = os.path.dirname(filename)
		if not self.is_folder_access_granted(folder):
			self.ui.folder_error.setVisible(True)
			return
		
		self.filename = filename
		self.parent.path_ascii = os.path.dirname(filename)

		#try:
		self.write_ascii()
		self.close()
		self.save_back_widget_parameters_used()
		#except:
		#     pass
		
	def save_back_widget_parameters_used(self):
		_is_with_4th_column_flag = self.ui.output4thColumnFlag.isChecked()
		_dq0 = self.ui.dq0Value.text()
		_dq_over_q = self.ui.dQoverQvalue.text()
		_use_lowest_error_value_flag = self.ui.usingLessErrorValueFlag.isChecked()
		
		_export_stitching_ascii_settings = ExportStitchingAsciiSettings()
		_export_stitching_ascii_settings.fourth_column_dq0 = _dq0
		_export_stitching_ascii_settings.fourth_column_dq_over_q = _dq_over_q
		_export_stitching_ascii_settings.fourth_column_flag = _is_with_4th_column_flag
		_export_stitching_ascii_settings.use_lowest_error_value_flag = _use_lowest_error_value_flag
		self.parent.exportStitchingAsciiSettings = _export_stitching_ascii_settings
		
	def is_folder_access_granted(self, filename):
		return os.access(filename,os.W_OK)
	
	def write_ascii(self):
		text = self.retrieve_metadata()
		self.is_with_4th_column_flag = self.ui.output4thColumnFlag.isChecked()
		dq_over_q = self.ui.dQoverQvalue.text()
		self.dq_over_q = float(dq_over_q)
		if self.is_with_4th_column_flag:
			dq0 = self.ui.dq0Value.text()
			self.dq0 = float(dq0)
			line1 = '# dQ0[1/Angstroms]= ' + dq0
			line2 = '# dQ/Q= ' + dq_over_q
			line3 = '# Q[1/Angstroms] R delta_R Precision'
			text.append(line1)
			text.append(line2)
			text.append("#")
			text.append(line3)
		else:
			text.append('# Q[1/Angstroms] R delta_R')
			
		self.use_lowest_error_value_flag = self.ui.usingLessErrorValueFlag.isChecked()
		self.text_data = text
		self.produce_data_with_common_q_axis()
		self.format_data()
		self.create_file()
		
	def retrieve_metadata(self):
		reduction_table = self.parent.ui.reductionTable
		text = []
		
		o_gui_utility = GuiUtility(parent = self.parent)
		_date = time.strftime("# Date: %d_%m_%Y")
		_reduction_method = '# Reduction method: manual'
		_reduction_engine = '# Reduction engine: RefRed'
		_reduction_date = '# %s' %_date
		_ipts = o_gui_utility.get_ipts(row = 0)
		for _entry in [_date, _reduction_method, _reduction_engine, _reduction_date]:
			text.append(_entry)
		text.append("#")
		
		nbr_row = o_gui_utility.reductionTable_nbr_row()
		_legend = "# DataRun\tNormRun\t2theta(degrees)\tLambdaMin(A)\tLambdaMax(A)\tQmin(1/A)\tQmax(1/A)\tScalingFactor"
		text.append(_legend)
		for _row in range(nbr_row):
			_data_run = str(reduction_table.item(_row, 1).text())
			_norm_run = str(reduction_table.item(_row, 2).text())
			_2_theta  = str(reduction_table.item(_row, 3).text())
			_lambda_min = str(reduction_table.item(_row, 4).text())
			_lambda_max = str(reduction_table.item(_row, 5).text())
			_q_min = str(reduction_table.item(_row, 6).text())
			_q_max = str(reduction_table.item(_row, 7).text())
			_scaling_factor = self.retrieve_scaling_factor(row = _row)
			_value = "# %s\t%s\t%s\t\t%s\t\t%s\t\t%s\t\t%s\t\t%s" %(_data_run,
			                                              _norm_run,
			                                              _2_theta,
			                                              _lambda_min,
			                                              _lambda_max,
			                                              _q_min,
			                                              _q_max,
			                                              _scaling_factor)
			text.append(_value)
		return text
	
	def retrieve_scaling_factor(self, row=-1):
		o_reduced_data_hanlder = ReducedDataHandler(parent = self.parent)
		big_table_data = self.parent.big_table_data
		_lconfig = big_table_data[row, 2]
		sf = o_reduced_data_hanlder.generate_selected_sf(lconfig = _lconfig)
		return str(sf)

	def create_file(self):
		RefRed.utilities.write_ascii_file(self.filename, self.text_data)
		
	def produce_data_with_common_q_axis(self):
		o_gui_utility = GuiUtility(parent = self.parent)
		nbr_row = o_gui_utility.reductionTable_nbr_row()

		_dataObject = self.parent.o_stitching_ascii_widget.loaded_ascii_array[0]
		_big_table_data = _dataObject.big_table_data
		
		minQ = 100
		maxQ = 0
		
		for i in range(nbr_row):
			_data = _big_table_data[i,2]
			
			tmp_wks_name = 'wks_' + str(i)
			
			_q_axis = _data.reduce_q_axis
			_y_axis = _data.reduce_y_axis[:-1]
			_e_axis = _data.reduce_e_axis[:-1]
			
			[_y_axis, _e_axis] = self.applySF(_data, _y_axis, _e_axis)
			
			minQ = min([_q_axis[0], minQ])
			maxQ = max([_q_axis[-1], maxQ])
			
			tmp_wks_name = CreateWorkspace(DataX = _q_axis,
					               DataY = _y_axis,
					               DataE = _e_axis,
					               Nspec = 1,
					               UnitX = "Wavelength",
					               OutputWorkspace = tmp_wks_name)
			tmp_wks_name.setDistribution(True)
			    
			# rebin everyting using the same Q binning parameters  
		binQ = self.dq_over_q
		bin_parameters = str(minQ) + ',-' + str(binQ) + ',' + str(maxQ)
		for i in range(nbr_row):  
				
			tmp_wks_name = 'wks_' + str(i)
			ConvertToHistogram(InputWorkspace = tmp_wks_name,
			                   OutputWorkspace = tmp_wks_name)
			
			Rebin(InputWorkspace = tmp_wks_name, 
			      Params = bin_parameters,
			      OutputWorkspace = tmp_wks_name)
			
		# we use the first histo as output reference
		data_y = mtd['wks_0'].dataY(0).copy()
		data_e = mtd['wks_0'].dataE(0).copy()
			
		skip_index = 0
		point_to_skip = 2
			
		for k in range(1, nbr_row):

			skip_point = True
			can_skip_last_point = False
			
			data_y_k = mtd['wks_' + str(k)].dataY(0)
			data_e_k = mtd['wks_' + str(k)].dataE(0)
			for j in range(len(data_y_k)-1):
					
				if data_y_k[j] > 0:
						
					can_skip_last_point = True
					if skip_point:
						skip_index += 1
						if skip_index == point_to_skip:
							skip_point = False
							skip_index = 0
						else:
							continue
						
				if can_skip_last_point and (data_y_k[j+1] == 0):
					break
					
				if data_y[j] > 0 and data_y_k[j] > 0:
					  
					if self.use_lowest_error_value_flag:
						if (data_e[j] > data_e_k[j]):
							data_y[j] = data_y_k[j]
							data_e[j] = data_e_k[j]
							
					else:
						[data_y[j], data_e[j]] = RefRed.utilities.weighted_mean([data_y[j], data_y_k[j]],
						                                                 [data_e[j], data_e_k[j]])
							
				elif (data_y[j] == 0) and (data_y_k[j]>0):
					data_y[j] = data_y_k[j]
					data_e[j] = data_e_k[j]
						
		data_x = mtd['wks_1'].dataX(0)
						
		self.q_axis = data_x
		self.y_axis = data_y
		self.e_axis = data_e
		
	def applySF(self, _data, y_array, e_array):
		if self.parent.ui.autoSF.isChecked():
			_sf = _data.sf_auto
		elif self.parent.ui.manualSF.isChecked():
			_sf = _data.sf_manual
		else:
			_sf = 1
		
		y_array = np.array(y_array, dtype=np.float)
		e_array = np.array(e_array, dtype=np.float)
		y_array /= _sf
		e_array /= _sf
		
		return [y_array, e_array]

	def format_data(self):
		_q_axis = self.q_axis
		_y_axis = self.y_axis
		_e_axis = self.e_axis
		text = self.text_data
		
		if self.is_with_4th_column_flag:
			dq0 = self.dq0
			dq_over_q = self.dq_over_q
		
		sz = len(_q_axis) - 1
		for i in range(sz):
			if _y_axis[i] > self.R_THRESHOLD:
				_line = str(_q_axis[i])
				_line += ' ' + str(_y_axis[i])
				_line += ' ' + str(_e_axis[i])
				if self.is_with_4th_column_flag:
					_precision = str(dq0 + dq_over_q * _q_axis[i])
					_line += ' ' + _precision
				text.append(_line)
		
		self.text_data = text