import time

import RefRed.constants
from RefRed.plot.popup_plot_1d import PopupPlot1d
from RefRed.plot.popup_plot_2d import PopupPlot2d
from RefRed.gui_handling.gui_utility import GuiUtility


class SingleClickPlot(object):
	
	parent = None
	data = None
	row = 0
	
	def __init__(self, parent, 
	             data_type = 'data', 
	             plot_type = 'yi', 
	             is_pan_or_zoom_activated = False,
	             is_manual_zoom_requested = False,
	             is_x_axis_manual_zoom_requested = False):
		
		self.parent = parent
		o_gui_utility = GuiUtility(parent = self.parent)
		row = o_gui_utility.get_current_table_reduction_check_box_checked()
		if row == -1:
			return
		self.row = row
		col = o_gui_utility.get_data_norm_tab_selected()


		self.data = parent.big_table_data[row, col]
		
		if plot_type == 'ix':
			return
		
		if plot_type == 'it':
			return
		
		if plot_type == 'stitching':
			return
		
		if plot_type == 'yi':
			self.single_yi_plot_click(data_type = data_type)
			                          
		
		if plot_type == 'yt':
			self.single_yt_plot_click(data_type = data_type)
		
	def single_yi_plot_click(self, data_type = 'data'):
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
			popup_plot = PopupPlot1d(parent = self.parent, 
			                         data_type = data_type,
			                         data = self.data,
			                         row = self.row)
			popup_plot.show()
			
		parent.time_click1 = -1
	
	def single_yt_plot_click(self, data_type = 'data'):
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
			popup_plot = PopupPlot2d(parent = self.parent,
			                         data_type = data_type,
			                         data = self.data,
			                         row = self.row)
			popup_plot.show()
			