import time
from RefRed.sf_calculator.plot_sf_dialog_refl import PlotSFDialogREFL
from RefRed.sf_calculator.plot2d_sf_dialog_refl import Plot2dSFDialogREFL
import RefRed.constants

class SFSinglePlotClick(object):
	
	parent = None
	nxsdata = None
	
	def __init__(self, parent, plot_type, is_pan_or_zoom_activated=False):
		self.parent = parent
		
		row = parent.current_table_row_selected
		list_nxsdata_sorted = parent.list_nxsdata_sorted
		self.nxsdata = list_nxsdata_sorted[row]
		
		if plot_type == 'yi':
			self.singleYIPlotClick()
		
		if plot_type == 'yt':
			self.singleYTIPlotClick()
		
	def singleYIPlotClick(self):
		parent = self.parent

		if parent.time_click1 == -1:
			parent.time_click1 = time.time()
			return
		elif abs(parent.time_click1 - time.time()) >0.5:
			parent.time_click1 = time.time()
			return
		else:
			_time_click2 = time.time()
	    
		if (_time_click2 - parent.time_click1) <= RefRed.constants.double_click_if_within_time:			
			data = self.nxsdata
			dialog_refl = PlotSFDialogREFL(parent, data)
			dialog_refl.show()
			
		parent.time_click1 = -1
	
	def singleYTIPlotClick(self):
		parent = self.parent

		if parent.time_click1 == -1:
			parent.time_click1 = time.time()
			return
		elif abs(parent.time_click1 - time.time()) > 0.5:
			parent.time_click1 = time.time()
			return
		else:
			_time_click2 = time.time()
	      
		if (_time_click2 - parent.time_click1) <= RefRed.constants.double_click_if_within_time:
			data = self.nxsdata
			dialog_refl2d = Plot2dSFDialogREFL(parent, data)
			dialog_refl2d.show()
			
		parent.time_click1 = -1