from PyQt4 import QtGui, QtCore
import RefRed.colors
from RefRed.plot.clear_plots import ClearPlots

class DisplayPlots(object):
	
	parent = None
	_data = None

	row = -1
	col = -1

	def __init__(self, parent=None, 
	             row=-1,
	             is_data=True,
	             plot_yt=True, 
	             plot_yi=True, 
	             plot_it=True, 
	             plot_ix=True, 
	             plot_reduced=False, 
	             plot_stitched=False):
		if row == -1:
			return
		
		self.parent = parent
		
		if is_data:
			col = 0
		else:
			col = 1
		self.row = row
		self.col = col

		_data = self.parent.big_table_data[row, col]
		if _data is None:
			print("clear plots")
			#ClearPlots(parent, is_data=self.isDataSelected(), is_norm=not self.isDataSelected(), all_plots=True)
			return






		self._data = _data
		if (not _active_data.new_detector_geometry_flag):
			self.xlim = 303
			self.ylim = 255
		
		if self.parent.retain_all:
			_active_data.all_plot_axis.yi_view_interval = self.parent.global_yi_view_interval
			_active_data.all_plot_axis.yt_view_interval = self.parent.global_yt_view_interval
			_active_data.all_plot_axis.it_view_interval = self.parent.global_it_view_interval
			_active_data.all_plot_axis.ix_view_interval = self.parent.global_ix_view_interval
			_active_data.all_plot_axis.yi_data_interval = self.parent.global_yi_view_interval
			_active_data.all_plot_axis.yt_data_interval = self.parent.global_yt_view_interval
			_active_data.all_plot_axis.it_data_interval = self.parent.global_it_view_interval
			_active_data.all_plot_axis.ix_data_interval = self.parent.global_ix_view_interval

			_active_data = self.activeData
			_data.active_data = _active_data
			parent.bigTableData[row,col] = _data
		
		if parent.ui.dataTOFmanualMode.isChecked():
			self.tofRangeAuto = self.getTOFrangeInMs(_active_data.tof_range)
		else:
			self.tofRangeAuto = self.getTOFrangeInMs(_active_data.tof_range_auto)

		self.tofAxis = self.getTOFrangeInMs(_active_data.tof_axis_auto_with_margin)
		self.fullTofAxis = self.getFullTOFinMs(_active_data.tof_axis_auto_with_margin)
		
		self.xy  = _active_data.xydata
		self.ytof = _active_data.ytofdata
		self.countstofdata = _active_data.countstofdata
		self.countsxdata = _active_data.countsxdata
		self.ycountsdata = _active_data.ycountsdata
		
		self.peak = self.sortIntArray(_active_data.peak)
		self.back = self.sortIntArray(_active_data.back)
		self.lowRes = self.sortIntArray(_active_data.low_res)
		self.backFlag = bool(_active_data.back_flag)
		self.lowResFlag = bool(_active_data.low_res_flag)
		
		is_data = True
		is_norm = False
		
		if self.isDataSelected():
			self.qRange = _active_data.q_range
			self.incidentAngle = _active_data.incident_angle
			self.lambdaRange = _active_data.lambda_range
			self.workWithData()
		else:
			is_data = False
			is_norm = True
			self.useItFlag = _active_data.use_it_flag
			self.workWithNorm()
		
		if plot_yt:
			ClearPlots(self.parent, plot_yt=True, is_data=is_data, is_norm=is_norm)
			self.plot_yt()

		if plot_it:
			ClearPlots(self.parent, plot_it=True, is_data=is_data, is_norm=is_norm)
			self.plot_it()
			
		if plot_yi:
			ClearPlots(self.parent, plot_yi=True, is_data=is_data, is_norm=is_norm)
			self.plot_yi()
			
		if plot_ix:
			ClearPlots(self.parent, plot_ix=True, is_data=is_data, is_norm=is_norm)
			self.plot_ix()
		
		if plot_yt or plot_it or plot_yi or plot_ix:
			if self.isDataSelected():
				parent.ui.dataNameOfFile.setText('%s'%(self.filename))
			else:
				parent.ui.normNameOfFile.setText('%s'%(self.filename))
			self.displayMetadata()
					
	def displayMetadata(self):
		self.clearMetadataWidgets()
		d = self.activeData
		if d is None:
			return
		parent = self.parent
		parent.ui.metadataProtonChargeValue.setText('%.2e'%d.proton_charge)
		parent.ui.metadataProtonChargeUnits.setText('%s'%d.proton_charge_units)
		parent.ui.metadataLambdaRequestedValue.setText('%.2f'%d.lambda_requested)
		parent.ui.metadataLambdaRequestedUnits.setText('%s'%d.lambda_requested_units)
		parent.ui.metadatathiValue.setText('%.2f'%d.thi)
		parent.ui.metadatathiUnits.setText('%s'%d.thi_units)
		parent.ui.metadatatthdValue.setText('%.2f'%d.tthd)
		parent.ui.metadatatthdUnits.setText('%s'%d.tthd_units)
		parent.ui.metadataS1WValue.setText('%.2f'%d.S1W)
		parent.ui.metadataS1HValue.setText('%.2f'%d.S1H)
		if d.isSiThere:
			parent.ui.S2SiWlabel.setText('SiW')
			parent.ui.S2SiHlabel.setText('SiH')
			parent.ui.metadataS2WValue.setText('%.2f'%d.SiW)
			parent.ui.metadataS2HValue.setText('%.2f'%d.SiH)
		else:
			parent.ui.S2SiWlabel.setText('S2W')
			parent.ui.S2SiHlabel.setText('S2H')
			parent.ui.metadataS2WValue.setText('%.2f'%d.S2W)
			parent.ui.metadataS2HValue.setText('%.2f'%d.S2H)

	def clearMetadataWidgets(self):
		parent = self.parent
		parent.ui.metadataProtonChargeValue.setText('N/A')
		parent.ui.metadataLambdaRequestedValue.setText('N/A')
		parent.ui.metadataS1HValue.setText('N/A')
		parent.ui.metadataS1WValue.setText('N/A')
		parent.ui.metadataS2HValue.setText('N/A')
		parent.ui.metadataS2WValue.setText('N/A')
		parent.ui.metadatathiValue.setText('N/A')
		parent.ui.metadatatthdValue.setText('N/A')
			
	def plot_ix(self):
		_countsxdata = self.countsxdata
		self.ix_plot_ui.canvas.ax.plot(_countsxdata)
		self.ix_plot_ui.canvas.ax.set_xlabel(u'pixels')
		self.ix_plot_ui.canvas.ax.set_ylabel(u'counts')
		self.ix_plot_ui.canvas.ax.set_xlim(0, self.xlim)
		
		if self.lowResFlag:
			self.ix_plot_ui.canvas.ax.axvline(self.lowRes[0], color=colors.LOWRESOLUTION_SELECTION_COLOR)
			self.ix_plot_ui.canvas.ax.axvline(self.lowRes[1], color=colors.LOWRESOLUTION_SELECTION_COLOR)
			
		if self.activeData.all_plot_axis.is_ix_ylog:
			self.ix_plot_ui.canvas.ax.set_yscale('log')
		else:
			self.ix_plot_ui.canvas.ax.set_yscale('linear')
			
		if self.activeData.all_plot_axis.ix_data_interval is None:
			self.ix_plot_ui.canvas.draw()
			[xmin,xmax] = self.ix_plot_ui.canvas.ax.xaxis.get_view_interval()
			[ymin,ymax] = self.ix_plot_ui.canvas.ax.yaxis.get_view_interval()
			self.activeData.all_plot_axis.ix_data_interval = [xmin,xmax,ymin,ymax]
			self.activeData.all_plot_axis.ix_view_interval = [xmin,xmax,ymin,ymax]
			self.ix_plot_ui.toolbar.home_settings = [xmin,xmax,ymin,ymax]
		else:
			[xmin,xmax,ymin,ymax] = self.activeData.all_plot_axis.ix_view_interval
			self.ix_plot_ui.canvas.ax.set_xlim([xmin,xmax])
			self.ix_plot_ui.canvas.ax.set_ylim([ymin,ymax])
			self.ix_plot_ui.canvas.draw()
			
	def plot_yi(self):
		_ycountsdata = self.ycountsdata
		_xaxis = range(len(_ycountsdata))
		self.yi_plot_ui.canvas.ax.plot(_ycountsdata, _xaxis, color=colors.COLOR_LIST[1])
		self.yi_plot_ui.canvas.ax.set_xlabel(u'counts')
		self.yi_plot_ui.canvas.ax.set_ylabel(u'y (pixel)')
		
		if self.activeData.all_plot_axis.yi_data_interval is None:
			self.yi_plot_ui.canvas.ax.set_ylim(0, self.ylim)
		
		self.yi_plot_ui.canvas.ax.axhline(self.peak[0], color=colors.PEAK_SELECTION_COLOR)
		self.yi_plot_ui.canvas.ax.axhline(self.peak[1], color=colors.PEAK_SELECTION_COLOR)
		
		if self.backFlag:
			self.yi_plot_ui.canvas.ax.axhline(self.back[0], color=colors.BACK_SELECTION_COLOR)
			self.yi_plot_ui.canvas.ax.axhline(self.back[1], color=colors.BACK_SELECTION_COLOR)
			
		if self.activeData.all_plot_axis.is_yi_xlog:
			self.yi_plot_ui.canvas.ax.set_xscale('log')
		else:
			self.yi_plot_ui.canvas.ax.set_xscale('linear')
			
		if self.activeData.all_plot_axis.yi_data_interval is None:
			self.yi_plot_ui.canvas.draw()
			[xmin, xmax] = self.yi_plot_ui.canvas.ax.xaxis.get_view_interval()
			[ymin, ymax] = self.yi_plot_ui.canvas.ax.yaxis.get_view_interval()
			self.activeData.all_plot_axis.yi_data_interval = [xmin, xmax, ymin, ymax]
			self.activeData.all_plot_axis.yi_view_interval = [xmin, xmax, ymin, ymax]
			self.yi_plot_ui.toolbar.home_settings = [xmin, xmax, ymin, ymax]
		else:
			[xmin, xmax, ymin, ymax] = self.activeData.all_plot_axis.yi_view_interval
			self.yi_plot_ui.canvas.ax.set_xlim([xmin, xmax])
			self.yi_plot_ui.canvas.ax.set_ylim([ymin, ymax])
			self.yi_plot_ui.canvas.draw()

	def plot_it(self):
		_tof_axis =self.fullTofAxis
		_countstofdata = self.countstofdata
		
		self.it_plot_ui.canvas.ax.plot(_tof_axis[0:-1], _countstofdata)
		self.it_plot_ui.canvas.ax.set_xlabel(u't (ms)')
		self.it_plot_ui.canvas.ax.set_ylabel(u'Counts')

		autotmin = float(self.tofRangeAuto[0])
		autotmax = float(self.tofRangeAuto[1])
		self.it_plot_ui.canvas.ax.axvline(autotmin, color=colors.TOF_SELECTION_COLOR)
		self.it_plot_ui.canvas.ax.axvline(autotmax, color=colors.TOF_SELECTION_COLOR)
		self.it_plot_ui.canvas.draw()
		
		if self.activeData.all_plot_axis.is_it_ylog:
			self.it_plot_ui.canvas.ax.set_yscale('log')
		else:
			self.it_plot_ui.canvas.ax.set_yscale('linear')
		self.it_plot_ui.canvas.draw()

#		return
			
		if self.activeData.all_plot_axis.it_data_interval is None:
			self.it_plot_ui.canvas.draw()
			[xmin,xmax] = self.it_plot_ui.canvas.ax.xaxis.get_view_interval()
			[ymin,ymax] = self.it_plot_ui.canvas.ax.yaxis.get_view_interval()
			self.activeData.all_plot_axis.it_data_interval = [xmin,xmax,ymin,ymax]
			self.activeData.all_plot_axis.it_view_interval = [xmin,xmax,ymin,ymax]
			self.it_plot_ui.toolbar.home_settings = [xmin,xmax,ymin,ymax]
		else:
			[xmin,xmax,ymin,ymax]= self.activeData.all_plot_axis.it_view_interval
			self.it_plot_ui.canvas.ax.set_xlim([xmin,xmax])
			self.it_plot_ui.canvas.ax.set_ylim([ymin,ymax])
			self.it_plot_ui.canvas.draw()
	
	def plot_yt(self):
		
		_ytof = self.ytof
		_isLog = True
		_tof_axis = self.tofAxis
		_extent = [_tof_axis[0], _tof_axis[1],0, self.ylim]
		self.yt_plot_ui.imshow(_ytof, log=_isLog, 
		                      aspect='auto', 
		                      origin='lower',
		                      extent=_extent)
		self.yt_plot_ui.set_xlabel(u't (ms)')
		self.yt_plot_ui.set_ylabel(u'y (pixel)')
		
		autotmin = float(self.tofRangeAuto[0])
		autotmax = float(self.tofRangeAuto[1])
		self.displayTOFrange(autotmin, autotmax, 'ms')
		[tmin, tmax] = self.getTOFrangeInMs([autotmin, autotmax])
		self.yt_plot_ui.canvas.ax.axvline(tmin, color=colors.TOF_SELECTION_COLOR)
		self.yt_plot_ui.canvas.ax.axvline(tmax, color=colors.TOF_SELECTION_COLOR)
		self.yt_plot_ui.canvas.ax.axhline(self.peak[0], color=colors.PEAK_SELECTION_COLOR)
		self.yt_plot_ui.canvas.ax.axhline(self.peak[1], color=colors.PEAK_SELECTION_COLOR)
		
		if self.backFlag:
			self.yt_plot_ui.canvas.ax.axhline(self.back[0], color=colors.BACK_SELECTION_COLOR)
			self.yt_plot_ui.canvas.ax.axhline(self.back[1], color=colors.BACK_SELECTION_COLOR)
		
		if self.activeData.all_plot_axis.is_yt_ylog:
			self.yt_plot_ui.canvas.ax.set_yscale('log')
		else:
			self.yt_plot_ui.canvas.ax.set_yscale('linear')
		
		if self.activeData.all_plot_axis.yt_data_interval is None:
			self.yt_plot_ui.canvas.ax.set_ylim(0,self.ylim)
			self.yt_plot_ui.canvas.draw()
			[xmin,xmax] = self.yt_plot_ui.canvas.ax.xaxis.get_view_interval()
			[ymin,ymax] = self.yt_plot_ui.canvas.ax.yaxis.get_view_interval()
			self.activeData.all_plot_axis.yt_data_interval = [xmin, xmax, ymin, ymax]
			self.activeData.all_plot_axis.yt_view_interval = [xmin, xmax, ymin, ymax]
			self.yt_plot_ui.toolbar.home_settings = [xmin, xmax, ymin, ymax]
		else:
			[xmin,xmax,ymin,ymax] = self.activeData.all_plot_axis.yt_view_interval
			self.yt_plot_ui.canvas.ax.set_xlim([xmin,xmax])
			self.yt_plot_ui.canvas.ax.set_ylim([ymin,ymax])
			self.yt_plot_ui.canvas.draw()
		
	def displayTOFrange(self, tmin, tmax, units):
		parent = self.parent
	  
		_tmin = float(tmin)
		_tmax = float(tmax)
		
		stmin = str("%.2f" % _tmin)
		stmax = str("%.2f" % _tmax)
		
		parent.ui.TOFmanualFromValue.setText(stmin)
		parent.ui.TOFmanualToValue.setText(stmax)
		
	def workWithNorm(self):
		parent = self.parent
		
		parent.ui.useNormalizationFlag.setChecked(self.useItFlag)
		
		[peak1, peak2] = self.peak
		parent.ui.normPeakFromValue.setValue(peak1)
		parent.ui.normPeakToValue.setValue(peak2)
		
		[back1, back2] = self.back
		parent.ui.normBackFromValue.setValue(back1)
		parent.ui.normBackToValue.setValue(back2)
		parent.ui.normBackgroundFlag.setChecked(self.backFlag)
		
		[lowRes1, lowRes2] = self.lowRes
		parent.ui.normLowResFromValue.setValue(lowRes1)
		parent.ui.normLowResToValue.setValue(lowRes2)
		parent.ui.normLowResFlag.setChecked(self.lowResFlag)
		
		self.yt_plot_ui = parent.ui.norm_yt_plot
		self.yi_plot_ui = parent.ui.norm_yi_plot
		self.it_plot_ui = parent.ui.norm_it_plot
		self.ix_plot_ui = parent.ui.norm_ix_plot
			
	def workWithData(self):
		parent = self.parent
		
		[peak1, peak2] = self.peak	
		parent.ui.dataPeakFromValue.setValue(peak1)
		parent.ui.dataPeakToValue.setValue(peak2)

		[back1, back2] = self.back
		parent.ui.dataBackFromValue.setValue(back1)
		parent.ui.dataBackToValue.setValue(back2)
		parent.ui.dataBackgroundFlag.setChecked(self.backFlag)
		
		[lowRes1, lowRes2] = self.lowRes
		parent.ui.dataLowResFromValue.setValue(lowRes1)
		parent.ui.dataLowResToValue.setValue(lowRes2)
		parent.ui.dataLowResFlag.setChecked(self.lowResFlag)
		
		self.yt_plot_ui = parent.ui.data_yt_plot
		self.yi_plot_ui = parent.ui.data_yi_plot
		self.it_plot_ui = parent.ui.data_it_plot
		self.ix_plot_ui = parent.ui.data_ix_plot
		
		[qmin, qmax] = self.qRange
		_item_min = QtGui.QTableWidgetItem(str(qmin))
		_item_min.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      
		_item_max = QtGui.QTableWidgetItem(str(qmax))
		_item_max.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      

		[lmin, lmax] = self.lambdaRange
		_item_lmin = QtGui.QTableWidgetItem(str(lmin))
		_item_lmin.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      
		_item_lmax = QtGui.QTableWidgetItem(str(lmax))
		_item_lmax.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      

		incident_angle = self.incidentAngle
		_item_incident = QtGui.QTableWidgetItem(str(incident_angle))
		_item_incident.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)      

		[row, col] = self.rowColSelected
		parent.ui.reductionTable.setItem(row, 4, _item_min)
		parent.ui.reductionTable.setItem(row, 5, _item_max)
		parent.ui.reductionTable.setItem(row, 2, _item_lmin)
		parent.ui.reductionTable.setItem(row, 3, _item_lmax)
		parent.ui.reductionTable.setItem(row, 1, _item_incident)
		
	def isDataSelected(self):
		if self.parent.ui.dataNormTabWidget.currentIndex() == 0:
			return True
		else:
			return False
		
	def sortIntArray(self, _array):
		[_element1, _element2] = _array
		_element1 = int(_element1)
		_element2 = int(_element2)
		_element_min = min([_element1, _element2])
		_element_max = max([_element1, _element2])
		return [_element_min, _element_max]

	def getTOFrangeInMs(self, tof_axis):
		if tof_axis[-1] > 1000:
			coeff = 1e-3
		else:
			coeff = 1
		return [tof_axis[0] * coeff, tof_axis[-1]*coeff]
		
	def getFullTOFinMs(self, tof_axis):
		if tof_axis[-1] > 1000:
			return tof_axis / float(1000)
		else:
			return tof_axis